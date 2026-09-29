# Regression suite

    cmake --preset dev && cmake --build --preset dev -j
    ctest --preset dev                          # regression + determinism
    tests/regression/run.py                     # compare against golden.json
    tests/regression/run.py --status-only       # ignore clause counts
    tests/regression/run.py --record [-k substr]   # accept current behaviour
    tests/regression/determinism.py             # environment-independence check

The binary is `$EPROVER`, else `build/dev/bin/eprover` (`--binary` overrides).

Entries in `problems.txt` are `<problem> [config,...]`; configs are defined in
`run.py`. `fixed` uses a fixed heuristic plus a processed-clause limit and
compares exact processed/generated clause counts; `auto` compares status only
(its strategy schedule is time-based).

## Why exact clause counts are a meaningful test

E keeps sets of objects in trees ordered by *address* and used to hash terms
by the addresses of their subterms. The search therefore used to depend on the
memory layout: ASLR, the length of the problem's file name, malloc's history,
the compiler. The same binary gave different clause counts on the same problem.
That has been removed:

* the term store and the type bank hash by deterministic ids (`entry_no`,
  `type_uid`), not addresses;
* the paramodulation index orders terms by `entry_no` and clauses by
  `perm_ident`;
* E's small objects come from a private arena (`E_DETERMINISTIC_MEMORY`, on by
  default; `src/basics/clb_memory.c`), so the relative addresses that the
  remaining pointer-ordered trees see follow E's own allocation sequence, not
  malloc's.

Consequently the counts in `golden.json` reproduce across ASLR settings, file
locations, `-O0`/`-O2 -march=native`/`-O3`, allocators (also a bump allocator
via `LD_PRELOAD`) and under ASan. `determinism.py` checks the environment part
directly (ASLR, file-name length, `MALLOC_PERTURB_`) and is part of `ctest`.

What remains: the counts still change when E's *own* behaviour changes,
which is the point. Pointer order still decides tie-breaks in a few places,
but it now follows allocation order. The `asan` preset builds without the arena
so that ASan sees every allocation; its counts may differ, so use
`--status-only` there. If a new toolchain disagrees on exact counts (e.g.
because of floating point in heuristic weights), that is worth investigating
first; `--status-only` is the fallback.

Only FO problems are included; the HO examples in `tests/problems/LFHOL`
need the HO build (`cmake --preset ho`) and should get their own entries.
