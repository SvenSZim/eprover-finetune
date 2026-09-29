# Syncing with upstream E

This fork tracks [`eprover/eprover`](https://github.com/eprover/eprover). Because
the fork is being reorganised (files deleted, later moved/renamed/reformatted),
a plain `git merge upstream/master` would drown in conflicts. Instead,
`tools/port_upstream.py` translates upstream's history into our layout first,
and we merge the *translated* history.

```
upstream/master ──(port_upstream.py)──▶ upstream-port ──(git merge)──▶ master
   pristine mirror                       same commits, our layout       our work
```

## How the translation works

For every upstream commit U the tool creates a commit U' on `upstream-port`:

* same author, committer, dates and message, plus a trailer
  `Upstream-Commit: <sha of U>`;
* tree = tree of U with the rules of `tools/port_upstream.toml` applied
  (`drop` paths, `rename` prefixes, optional formatter for `*.c`/`*.h`);
* parents = the translated parents, so upstream's merge structure survives.

Trees are translated, not patches applied, so **a commit cannot fail to apply**.
The result is deterministic (same rules => same hashes) and incremental (done
commits are found through their trailer). `upstream-port` is rooted on the fork
point (`base` in the config), so `git merge upstream-port` uses the fork point
as merge-base and only real overlaps (both sides edited the same lines) conflict.

The tool never touches `master`, the working tree or the remote.

## One-time setup (already done for this repo)

```sh
git remote add upstream https://github.com/eprover/eprover.git
git fetch upstream
tools/port_upstream.py check-base --ref master   # sanity check, see below
tools/port_upstream.py init                       # creates branch upstream-port
```

`check-base` lists the differences between the translated fork point and a ref.
For master it must show only changes we made *on purpose* (CI, tests, edited
Makefiles, ...). A deleted or moved file that shows up here means `drop`/`rename`
in the config do not match what we did -- fix the config first.

## Routine sync

```sh
git fetch upstream
tools/port_upstream.py sync            # translate all new upstream commits
tools/port_upstream.py verify --limit 50   # optional self-check (see below)
tools/port_upstream.py merge-check     # trial merge into HEAD in a scratch worktree
git checkout master && git merge upstream-port
tests/regression/run.py                # then re-record golden.json only if the
                                       # upstream change is meant to alter behaviour
```

Expected results of `sync`:

* `ported N commit(s)` -- done.
* A **"Needs manual attention"** list: upstream commits that touched build
  files (`watch` in the config: the Makefiles, `configure`, ...). The old
  build system is in `drop` (we build with CMake), so such a change is *not*
  carried over, but the commit message on `upstream-port` gets a `Port-Watch:`
  trailer and it is listed here. Mirror it by hand in `CMakeLists.txt` (new
  source file in a directory: nothing to do, sources are globbed; new
  program, library, define or link dependency: edit `CMakeLists.txt`).
  Find them again with `git log --grep Port-Watch upstream-port`.
* **HALTED** (exit code 2): the next commit touches a file listed in `halt_on`
  (see "Manual ports").

## Current layout

The mapping (`rename` in `port_upstream.toml`) is: `BASICS` ... `CONTROL` ->
`src/<lowercase>/`, `PROVER` -> `apps/`, `SIMPLE_APPS`/`EXTERNAL` ->
`apps/simple/`/`apps/external/`, `CONTRIB` -> `third_party/`, `EXAMPLE_PROBLEMS` ->
`tests/problems/`, `DOC` -> `docs/`, `development_tools`/`PYTHON` ->
`tools/development`/`tools/python`. The old Makefiles and `configure` are
dropped (reported via `Port-Watch`). The restructure was verified end to end
with a simulated upstream commit that edited, added and moved files across
these directories: the merge was clean and every change landed in the new location.

## Manual ports (files we split up)

If we split a file (e.g. `che_litselection.c` into several) the tool cannot
translate upstream edits to it. List the file under `halt_on`. When `sync`
halts before upstream commit `U`:

1. Temporarily remove the file(s) from `halt_on` and run
   `tools/port_upstream.py sync --limit 1`. This ports U with everything except
   the split files translated normally (they still exist in their old,
   unsplit form on `upstream-port`).
2. `git checkout upstream-port`, apply U's edit to the split files by hand
   (`git show U -- <path>`), and `git commit --amend` (keep the
   `Upstream-Commit: <U>` trailer in the message).
3. Restore `halt_on` and re-run `sync`; it resumes after U.

For a file that exists *only* in split form on master, keep the old file out of
master (drop it on the master side) so the merge does not resurrect it.

Keep splits few, and keep the original file name for one of the pieces, to make
this rare. (Nothing needs to happen for upstream changes in files we did *not*
split, even if they were moved or reformatted.)

## When the layout changes (moves, formatting, more deletions)

Rules must describe the current layout of `master`. To change the layout:

1. Do the change on master (`git mv ...`, formatting commit, deletions).
2. Add the matching `rename`/`drop`/`format` entries to `port_upstream.toml`.
3. `tools/port_upstream.py check-base --ref master` (compares against the fork
   point, so it lists all deliberate changes; renames appear as D + A pairs).
4. `tools/port_upstream.py migrate` -- adds one commit to `upstream-port` that
   applies the new rules to the newest ported upstream commit. Future `sync`s
   use the new rules. Old history on the branch is not rewritten.
5. **Immediately** `git merge upstream-port` into master, before any further
   upstream sync. The migration commit changes the files exactly as master did,
   so it merges cleanly, and afterwards the merge-base of master and
   `upstream-port` is a commit that already has the new layout/formatting. If
   you skip this, the next upstream edit is merged against the *old* fork point
   and every line that master reformatted or moved conflicts.

Do not edit the rules and then run `sync` without `migrate`: new commits would be
translated with rules that the branch tip does not follow.

## Self-checks

* End-to-end test (done for the current layout): merge `upstream-port` into a
  scratch branch, add a fake upstream commit with an unformatted edit inside a
  function, `sync`, merge again. The edit arrived formatted and the merge was
  clean.
* `verify [--limit N]` recomputes each ported commit's tree from scratch from
  upstream and compares it with the port branch (only commits after the last
  migration; earlier ones used older rules). It has passed on 784 real upstream
  commits. It checks the tool's own consistency, not that our merged code works;
  for that use `tests/regression/run.py`.
* `merge-check [--ref REF]` merges the port branch into REF in a scratch
  worktree, reports conflicts, and aborts. Nothing is changed.
* Test on old history without touching the real branch:
  `tools/port_upstream.py --base <older upstream commit> --branch port-test init`,
  then `sync`, `verify`, and delete the branch.

## Things to know

* The translated blobs under `src/` and `apps/` are formatted with
  `clang-format` (`[format]` in the config: pinned version, two passes), so the
  result is byte-identical to `tools/format.sh` on our side. The tool refuses to
  run with another clang-format version (`pip install clang-format==23.1.1`).
  Changing `.clang-format` or the pinned version is a rules change: re-run
  `tools/format.sh`, commit, then `migrate` and merge (below).
* `Makefile`-family changes are *not* translated to CMake; that is the manual
  step above.
* The regression suite's clause counts only reproduce for the same toolchain
  (see `tests/regression/README.md`); after merging upstream changes compare
  with `--status-only` unless you compare against a baseline built from the
  merge-base with the same compiler.
* Upstream force-pushes/rebases would leave orphan translated commits on the
  port branch; the tool assumes `upstream/master` only moves forward.
* Requires Python >= 3.11 (`tomllib`) and git; no other dependencies.
