#!/usr/bin/env python3
"""Deterministic regression suite for eprover.

For every (problem, config) pair listed in problems.txt this runs eprover and
compares status, processed clauses and generated clauses against the golden
file golden.json. Clause counts are deterministic, so any unintended change to
search behaviour (e.g. from a refactoring) shows up as a diff.

    tests/regression/run.py             # compare against golden.json
    tests/regression/run.py --status-only   # ignore clause counts (see below)
    tests/regression/run.py --record    # (re)write golden.json
    tests/regression/run.py -k SMOKE    # only entries whose id contains SMOKE

The search is independent of the memory layout (see tests/regression/README.md
and determinism.py), so the clause counts reproduce across compilers, flags,
ASLR and file locations. If a new toolchain still disagrees (e.g. because of
floating-point differences in heuristic weights), use --status-only.
"""
import argparse
import json
import os
import re
import shlex
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
GOLDEN = HERE / "golden.json"

# Named prover configurations. Only step-count-based limits are used so that
# results do not depend on machine speed (cpu-limit is just a safety net).
CONFIGS = {
    "auto": ["--auto", "--proof-object"],
    "fixed": ["-tKBO6", "-WSelectMaxLComplexAvoidPosPred", "--proof-object",
              "-H(4*ConjectureRelativeSymbolWeight(ConstPrio,0.1,100,100,100,100,1.5,1.5,1.5),"
              "1*FIFOWeight(PreferProcessed))",
              "--processed-clauses-limit=3000"],
}
# --auto picks strategies from a time-dependent schedule and can hit its
# per-strategy cutoffs at slightly different points, so clause counts are only
# compared for configs listed here; the others compare the status only.
EXACT_COUNTS = {"fixed"}
SAFETY_CPU_LIMIT = 60


def default_binary():
    for cand in (ROOT / "build" / "dev" / "bin" / "eprover", ROOT / "PROVER" / "eprover"):
        if cand.exists():
            return str(cand)
    return str(ROOT / "build" / "dev" / "bin" / "eprover")


def parse_problems(path):
    """Lines: `<problem path rel. to repo root> [config,config,...]`."""
    entries = []
    for line in path.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        cfgs = parts[1].split(",") if len(parts) > 1 else ["auto"]
        for c in cfgs:
            entries.append((parts[0], c))
    return entries


def run_one(binary, problem, config, cpu_limit):
    # Run from the problem's own directory with just the file name (keeps the
    # output independent of where the repository lives).
    pdir, pname = os.path.split(ROOT / problem)
    cmd = [str(Path(binary).resolve()), *CONFIGS[config], f"--cpu-limit={cpu_limit}",
           "--print-statistics", pname]
    try:
        p = subprocess.run(cmd, cwd=pdir, capture_output=True, text=True,
                           timeout=cpu_limit * 3 + 10)
    except subprocess.TimeoutExpired:
        return {"status": "Hang"}
    out = p.stdout
    status = re.search(r"^# SZS status (\w+)|^% SZS status (\w+)", out, re.M)
    res = {"status": (status.group(1) or status.group(2)) if status else f"NoStatus(rc={p.returncode})"}
    for key, name in (("processed", "Processed clauses"),
                      ("generated", "Generated clauses")):
        m = re.search(rf"^[#%] {name}\s*:\s*(\d+)", out, re.M)
        if m:
            res[key] = int(m.group(1))
    if config not in EXACT_COUNTS:
        res.pop("processed", None)
        res.pop("generated", None)
    if res["status"] == "Unsatisfiable" and "SZS output start" not in out:
        res["status"] = "Unsatisfiable(no-proof-object)"
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--record", action="store_true", help="write golden.json")
    ap.add_argument("--binary", default=os.environ.get("EPROVER") or default_binary(),
                    help="default: $EPROVER, else build/dev/bin/eprover")
    ap.add_argument("--status-only", action="store_true",
                    help="compare only the SZS status, not the clause counts")
    ap.add_argument("-j", "--jobs", type=int, default=4)
    ap.add_argument("-k", default="", help="substring filter on entry ids")
    ap.add_argument("--problems", default=str(HERE / "problems.txt"))
    ap.add_argument("--golden", default=str(GOLDEN), help="golden results file")
    ap.add_argument("--cpu-limit", type=int, default=SAFETY_CPU_LIMIT)
    a = ap.parse_args()

    if not Path(a.binary).exists():
        sys.exit(f"eprover binary not found: {a.binary} (cmake --preset dev && cmake --build --preset dev)")
    entries = [(f"{p}::{c}", p, c) for p, c in parse_problems(Path(a.problems))]
    entries = [e for e in entries if a.k in e[0]]

    with ThreadPoolExecutor(a.jobs) as ex:
        results = list(ex.map(lambda e: run_one(a.binary, e[1], e[2], a.cpu_limit), entries))
    actual = {e[0]: r for e, r in zip(entries, results)}

    if a.record:
        old = json.loads(Path(a.golden).read_text()) if Path(a.golden).exists() else {}
        old.update(actual)
        Path(a.golden).write_text(json.dumps(old, indent=1, sort_keys=True) + "\n")
        print(f"recorded {len(actual)} entries in {a.golden}")
        return

    golden = json.loads(Path(a.golden).read_text()) if Path(a.golden).exists() else {}
    bad = 0
    for key, res in actual.items():
        exp = golden.get(key)
        if a.status_only and exp is not None:
            exp, res = {"status": exp["status"]}, {"status": res["status"]}
        if exp is None:
            print(f"NEW   {key}: {res}")
            bad += 1
        elif exp != res:
            print(f"DIFF  {key}\n        expected {exp}\n        got      {res}")
            bad += 1
    print(f"{len(actual) - bad}/{len(actual)} match")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
