#!/usr/bin/env python3
"""Check that E's search does not depend on the memory layout.

E keeps sets of objects in trees ordered by address and hashes by pointer in
places. That once made results depend on ASLR, the length of the problem's file
name, malloc's history, and so on. This test reruns problems (fixed heuristic,
processed-clause limit) in deliberately perturbed environments and requires
identical processed/generated clause counts:

  * ASLR on and off,
  * a file name of very different length (via a temporary symlink),
  * glibc's MALLOC_PERTURB_ (fills fresh and freed memory with a pattern; finds
    dependence on uninitialised memory).

    tests/regression/determinism.py [--binary eprover] [--all]
"""
import argparse
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
import run as suite  # noqa: E402

ARGS = suite.CONFIGS["fixed"] + ["--print-statistics"]


def counts(binary, pdir, pname, env, noaslr):
    cmd = (["setarch", "-R"] if noaslr else []) + [binary, *ARGS, "--cpu-limit=120", pname]
    e = dict(os.environ)
    e.update(env)
    out = subprocess.run(cmd, cwd=pdir, capture_output=True, text=True, env=e).stdout
    g = re.search(r"Generated clauses\s*:\s*(\d+)", out)
    p = re.search(r"Processed clauses\s*:\s*(\d+)", out)
    return (p.group(1) if p else "?", g.group(1) if g else "?")


def check(binary, problem):
    pdir, pname = os.path.split(ROOT / problem)
    padded = "a_rather_long_file_name_to_shift_the_heap_" + pname
    link = Path(pdir) / padded
    os.symlink(pname, link)
    try:
        variants = {
            "baseline": counts(binary, pdir, pname, {}, False),
            "no-aslr": counts(binary, pdir, pname, {}, True),
            "long-name": counts(binary, pdir, padded, {}, False),
            "malloc-perturb": counts(binary, pdir, pname, {"MALLOC_PERTURB_": "165"}, False),
        }
    finally:
        link.unlink()
    return problem, variants


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--binary", default=os.environ.get("EPROVER") or suite.default_binary())
    ap.add_argument("--all", action="store_true", help="all fixed-config problems (slow)")
    ap.add_argument("-j", "--jobs", type=int, default=4)
    a = ap.parse_args()
    binary = str(Path(a.binary).resolve())

    problems = [p for p, c in suite.parse_problems(HERE / "problems.txt") if c == "fixed"]
    problems = sorted(set(problems))
    if not a.all:   # a representative, fast subset
        keep = ("SMOKETEST/LUSK3", "SMOKETEST/CNFTest", "TPTP/BOO006-1", "TPTP/SYN190-1",
                "TPTP/SET183-6", "TPTP/SEU027+1", "TPTP/GEO288+1", "TPTP/COL042-8",
                "TPTP/CSR036+2", "TPTP/HEN011-2")
        problems = [p for p in problems if any(k in p for k in keep)]
    bad = 0
    with ThreadPoolExecutor(a.jobs) as ex:
        for problem, v in ex.map(lambda p: check(binary, p), problems):
            if len(set(v.values())) > 1:
                bad += 1
                print(f"DEPENDS ON ENVIRONMENT  {problem}: {v}")
    print(f"{len(problems) - bad}/{len(problems)} problems independent of the environment")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
