#!/usr/bin/env python3
"""Translate upstream E history into this fork's layout.

Every upstream commit U becomes a commit U' on the port branch with the same
author, dates and message (plus an `Upstream-Commit: <sha>` trailer). The tree
of U' is the tree of U with the rules in port_upstream.toml applied (paths
dropped/renamed, blobs optionally formatted). Parents are mapped the same way,
so upstream's merge structure is preserved. Nothing is patched, so nothing can
fail to apply; the result is deterministic and the run is incremental (already
ported commits are recognised by their trailer).

The port branch is rooted on the fork point, so `git merge <port_branch>` into
master finds the fork point as merge-base.

Commands:
    init         create the port branch (one commit: translated fork point)
    sync         port all new commits of upstream_ref
    migrate      re-apply changed rules (drop/rename/format) as one commit
    verify       recompute trees from scratch and compare with the port branch
    check-base   compare translated fork point with a ref (default: HEAD)
    merge-check  trial-merge the port branch into a ref in a scratch worktree
"""
import argparse
import fnmatch
import os
import re
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
TRAILER = "Upstream-Commit"
ZERO = "0" * 40


class Git:
    def __init__(self, cwd):
        self.cwd = cwd

    def run(self, *args, input=None, env=None, check=True):
        e = dict(os.environ)
        if env:
            e.update(env)
        p = subprocess.run(["git", "-c", "commit.gpgsign=false", *args], cwd=self.cwd,
                           input=input, capture_output=True, env=e)
        if check and p.returncode:
            sys.exit(f"git {' '.join(args)} failed:\n{p.stderr.decode(errors='replace')}")
        return p

    def out(self, *args, **kw):
        return self.run(*args, **kw).stdout.decode("utf-8", "surrogateescape")

    def ok(self, *args):
        return self.run(*args, check=False).returncode == 0


class Rules:
    def __init__(self, cfg):
        self.drop = cfg.get("drop", [])
        self.rename = sorted(cfg.get("rename", []), key=lambda r: -len(r[0]))
        self.watch = cfg.get("watch", [])
        self.watch_ignore = cfg.get("watch_ignore", [])
        self.halt = cfg.get("halt_on", [])
        fmt = cfg.get("format", {})
        self.fmt_globs = fmt.get("globs", [])
        self.fmt_cmd = fmt.get("command", [])

    @staticmethod
    def _match(pat, path):
        return path.startswith(pat) if pat.endswith("/") else fnmatch.fnmatchcase(path, pat)

    def dropped(self, path):
        return any(self._match(p, path) for p in self.drop)

    def map_path(self, path):
        """New path, or None if the path is not carried over."""
        if self.dropped(path):
            return None
        for old, new in self.rename:
            if path.startswith(old):
                return new + path[len(old):]
        return path

    def watched(self, path):
        return (any(self._match(p, path) for p in self.watch)
                and not any(self._match(p, path) for p in self.watch_ignore))

    def halting(self, path):
        return any(self._match(p, path) for p in self.halt)

    def wants_format(self, newpath):
        return bool(self.fmt_cmd) and any(fnmatch.fnmatchcase(newpath, g) for g in self.fmt_globs)


class Porter:
    def __init__(self, git, cfg):
        self.git = git
        self.cfg = cfg
        self.rules = Rules(cfg)
        self.base = git.out("rev-parse", "--verify", cfg["base"] + "^{commit}").strip()
        self.branch = cfg["port_branch"]
        self._blob_cache = {}

    # -- blobs / trees -----------------------------------------------------
    def blob(self, sha, newpath):
        if not self.rules.wants_format(newpath):
            return sha
        key = (sha, newpath)
        if key not in self._blob_cache:
            src = self.git.run("cat-file", "blob", sha).stdout
            cmd = [c.replace("{path}", newpath) for c in self.rules.fmt_cmd]
            p = subprocess.run(cmd, input=src, capture_output=True)
            if p.returncode:
                sys.exit(f"formatter failed on {newpath}: {p.stderr.decode(errors='replace')}")
            self._blob_cache[key] = self.git.run("hash-object", "-w", "--stdin",
                                                 input=p.stdout).stdout.decode().strip()
        return self._blob_cache[key]

    def _write_tree(self, index_lines, from_tree=None):
        """Build a tree via a scratch index; returns tree sha."""
        with tempfile.TemporaryDirectory() as d:
            env = {"GIT_INDEX_FILE": os.path.join(d, "index")}
            if from_tree:
                self.git.run("read-tree", from_tree, env=env)
            if index_lines:
                self.git.run("update-index", "--index-info", env=env,
                             input="".join(index_lines).encode("utf-8", "surrogateescape"))
            return self.git.out("write-tree", env=env).strip()

    def full_tree(self, commit):
        lines = []
        for rec in self.git.out("ls-tree", "-r", "-z", commit).split("\0"):
            if not rec:
                continue
            meta, path = rec.split("\t", 1)
            mode, typ, sha = meta.split()
            if typ != "blob" and mode != "160000":
                continue
            new = self.rules.map_path(path)
            if new is not None:
                lines.append(f"{mode} {self.blob(sha, new) if typ == 'blob' else sha} 0\t{new}\n")
        return self._write_tree(lines)

    def incremental_tree(self, parent, commit, parent_port_tree):
        """Translated tree of `commit`, derived from the translated `parent`."""
        lines, touched = [], []
        raw = self.git.out("diff-tree", "-r", "-z", "--no-renames", "--raw", parent, commit)
        toks = raw.split("\0")
        i = 0
        while i + 1 < len(toks) and toks[i]:
            meta, path = toks[i], toks[i + 1]
            i += 2
            old_mode, new_mode, old_sha, new_sha, status = meta.lstrip(":").split()
            new = self.rules.map_path(path)
            touched.append(path)
            if new is None:
                continue
            if status == "D":
                lines.append(f"0 {ZERO} 0\t{new}\n")
            else:
                is_blob = new_mode != "160000"
                lines.append(f"{new_mode} {self.blob(new_sha, new) if is_blob else new_sha} 0\t{new}\n")
        return self._write_tree(lines, from_tree=parent_port_tree), touched

    # -- commits -------------------------------------------------------------
    def read_commit(self, sha):
        raw = self.git.run("cat-file", "commit", sha).stdout.decode("utf-8", "surrogateescape")
        head, _, msg = raw.partition("\n\n")
        info = {"parents": [], "msg": msg}
        for line in head.split("\n"):
            if line.startswith("tree "):
                info["tree"] = line[5:]
            elif line.startswith("parent "):
                info["parents"].append(line[7:])
            elif line.startswith("author "):
                info["author"] = line[7:]
            elif line.startswith("committer "):
                info["committer"] = line[10:]
        return info

    @staticmethod
    def _ident_env(kind, ident):
        m = re.match(r"(.*) <(.*)> (\d+ [+-]\d{4})$", ident)
        n, e, d = m.groups()
        return {f"GIT_{kind}_NAME": n, f"GIT_{kind}_EMAIL": e, f"GIT_{kind}_DATE": d}

    def make_commit(self, info, tree, parents, upstream_sha, notes=()):
        msg = info["msg"].rstrip("\n") + "\n\n"
        for n in notes:
            msg += n + "\n"
        msg += f"{TRAILER}: {upstream_sha}\n"
        env = {**self._ident_env("AUTHOR", info["author"]),
               **self._ident_env("COMMITTER", info["committer"])}
        args = ["commit-tree", tree]
        for p in parents:
            args += ["-p", p]
        return self.git.out(*args, input=msg.encode("utf-8", "surrogateescape"), env=env).strip()

    def port_map(self):
        """upstream sha -> port commit sha, from trailers on the port branch."""
        if not self.git.ok("rev-parse", "--verify", "-q", self.branch):
            return {}
        res = {}
        log = self.git.out("log", "--format=%H%x1f%B%x1e", f"{self.base}..{self.branch}")
        for entry in log.split("\x1e"):
            if not entry.strip():
                continue
            sha, _, body = entry.strip().partition("\x1f")
            for m in re.finditer(rf"^{TRAILER}: ([0-9a-f]{{40}})$", body, re.M):
                res.setdefault(m.group(1), sha)   # log is newest-first: newest wins
        return res

    # -- commands ------------------------------------------------------------
    def init(self):
        if self.git.ok("rev-parse", "--verify", "-q", self.branch):
            sys.exit(f"branch {self.branch} already exists")
        info = self.read_commit(self.base)
        tree = self.full_tree(self.base)
        c = self.make_commit(info, tree, [self.base], self.base,
                             notes=["Port-Base: translated fork point"])
        self.git.run("branch", self.branch, c)
        print(f"created {self.branch} at {c[:10]} (translated {self.base[:10]})")

    def migrate(self):
        """Re-translate the newest ported upstream commit with the current rules
        and commit the difference on top of the port branch (after editing
        `rename`/`drop`/`format` in the config)."""
        pm = self.port_map()
        tip = self.git.out("rev-parse", self.branch).strip()
        tip_info = self.read_commit(tip)
        m = re.search(rf"^{TRAILER}: ([0-9a-f]{{40}})$", tip_info["msg"], re.M)
        if not m:
            sys.exit("port branch tip has no Upstream-Commit trailer")
        u = m.group(1)
        tree = self.full_tree(u)
        if tree == tip_info["tree"]:
            print("port branch already matches the current rules")
            return
        info = self.read_commit(u)
        info["msg"] = "Apply updated port rules\n"
        c = self.make_commit(info, tree, [tip], u, notes=["Port-Migration: rules changed"])
        self.git.run("update-ref", f"refs/heads/{self.branch}", c)
        print(f"migration commit {c[:10]} on {self.branch}; merge it into master together with"
              " (or after) the matching change of the fork's layout")

    def sync(self, limit=None):
        pm = self.port_map()
        if self.base not in pm:
            sys.exit(f"port branch not initialised (run `init`)")
        todo = self.git.out("rev-list", "--reverse", "--topo-order",
                            self.cfg["upstream_ref"], "--not", self.base).split()
        todo = [c for c in todo if c not in pm]
        if limit:
            todo = todo[:limit]
        watched, done = [], 0
        base_anc = None
        for u in todo:
            info = self.read_commit(u)
            parents = []
            for p in info["parents"]:
                if p in pm:
                    parents.append(pm[p])
                elif self.git.ok("merge-base", "--is-ancestor", p, self.base):
                    parents.append(p)          # pre-fork history stays as is
                else:
                    sys.exit(f"parent {p[:10]} of {u[:10]} was not ported (unexpected)")
            first = info["parents"][0] if info["parents"] else None
            if first is not None and first in pm:
                ptree = self.read_commit(pm[first])["tree"]
                tree, touched = self.incremental_tree(first, u, ptree)
            else:
                tree = self.full_tree(u)
                touched = self.git.out("diff-tree", "-r", "--name-only", "--no-renames",
                                       "-z", first or "--root", u).split("\0")
                touched = [t for t in touched if t]
            halting = [t for t in touched if not self.rules.dropped(t) and self.rules.halting(t)]
            if halting:
                self._halt(u, halting, done)
            watch = sorted({t for t in touched if not self.rules.dropped(t) and self.rules.watched(t)})
            notes = [f"Port-Watch: {', '.join(watch)}"] if watch else []
            c = self.make_commit(info, tree, parents, u, notes)
            pm[u] = c
            # advance branch after every commit so an abort loses nothing
            self.git.run("update-ref", f"refs/heads/{self.branch}", c)
            done += 1
            if watch:
                subj = info["msg"].split("\n", 1)[0]
                watched.append((u, subj, watch))
        print(f"ported {done} commit(s) onto {self.branch}")
        if watched:
            print(f"\nNeeds manual attention: {len(watched)} commit(s) changed build files"
                  " (also marked with a Port-Watch trailer):")
            for u, subj, w in watched[:40]:
                print(f"  {u[:10]} {subj[:70]}\n      {', '.join(w)}")
            if len(watched) > 40:
                print(f"  ... and {len(watched) - 40} more")

    def _halt(self, u, paths, done):
        print(f"ported {done} commit(s), then HALTED before upstream commit {u}", file=sys.stderr)
        print("It touches files that cannot be translated mechanically:", file=sys.stderr)
        for p in paths:
            print(f"    {p}", file=sys.stderr)
        print("Port it by hand (see tools/UPSTREAM_SYNC.md, 'Manual ports'), commit it on\n"
              f"{self.branch} with the trailer `{TRAILER}: {u}`, then re-run sync.", file=sys.stderr)
        sys.exit(2)

    def verify(self, limit=None):
        pm = self.port_map()
        items = [(u, c) for u, c in pm.items()]
        mig = self.git.out("log", "-1", "--format=%H", "--grep=^Port-Migration:",
                           f"{self.base}..{self.branch}").strip()
        if mig:   # commits from before the last migration used older rules
            items = [(u, c) for u, c in items if c == mig or self.git.ok(
                "merge-base", "--is-ancestor", mig, c)]
        if limit:
            items = items[-limit:]
        bad = 0
        for u, c in items:
            want = self.full_tree(u)
            have = self.read_commit(c)["tree"]
            if want != have:
                bad += 1
                print(f"MISMATCH upstream {u[:10]} port {c[:10]}")
        print(f"verified {len(items)} commit(s): {len(items) - bad} ok, {bad} mismatching")
        return bad == 0

    def check_base(self, ref):
        tree = self.full_tree(self.base)
        out = self.git.out("diff-tree", "-r", "--name-status", "--no-renames", tree, ref + "^{tree}")
        print(f"differences between translated fork point and {ref}:")
        print(out or "  (none)")

    def merge_check(self, ref):
        if not self.git.ok("rev-parse", "--verify", "-q", self.branch):
            sys.exit(f"branch {self.branch} does not exist")
        with tempfile.TemporaryDirectory() as d:
            wt = os.path.join(d, "wt")
            self.git.run("worktree", "add", "-q", "--detach", wt, ref)
            try:
                g = Git(wt)
                p = g.run("merge", "--no-commit", "--no-ff", self.branch, check=False)
                conflicts = g.out("diff", "--name-only", "--diff-filter=U").split()
                if conflicts:
                    print("CONFLICTS:\n  " + "\n  ".join(conflicts))
                elif p.returncode == 0 or b"Already up to date" in p.stdout:
                    print(p.stdout.decode(errors="replace").strip().splitlines()[0] if p.stdout.strip() else "clean")
                    print("merge is clean")
                else:
                    print(p.stdout.decode(errors="replace") + p.stderr.decode(errors="replace"))
                g.run("merge", "--abort", check=False)
                return not conflicts
            finally:
                self.git.run("worktree", "remove", "--force", wt, check=False)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["init", "sync", "migrate", "verify", "check-base", "merge-check"])
    ap.add_argument("--config", default=str(HERE / "port_upstream.toml"))
    ap.add_argument("--base", help="override config `base` (testing)")
    ap.add_argument("--branch", help="override config `port_branch` (testing)")
    ap.add_argument("--upstream-ref", help="override config `upstream_ref`")
    ap.add_argument("--limit", type=int, help="sync/verify: only this many commits")
    ap.add_argument("--ref", default="HEAD", help="check-base/merge-check: ref to compare with")
    a = ap.parse_args()

    cfg = tomllib.loads(Path(a.config).read_text())
    for k, v in (("base", a.base), ("port_branch", a.branch), ("upstream_ref", a.upstream_ref)):
        if v:
            cfg[k] = v
    git = Git(HERE.parent)
    porter = Porter(git, cfg)
    if a.command == "init":
        porter.init()
    elif a.command == "sync":
        porter.sync(a.limit)
    elif a.command == "migrate":
        porter.migrate()
    elif a.command == "verify":
        sys.exit(0 if porter.verify(a.limit) else 1)
    elif a.command == "check-base":
        porter.check_base(a.ref)
    elif a.command == "merge-check":
        sys.exit(0 if porter.merge_check(a.ref) else 1)


if __name__ == "__main__":
    main()
