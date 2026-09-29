# Regression suite

    cmake --preset dev && cmake --build --preset dev -j
    ctest --preset dev                          # or, directly:
    tests/regression/run.py                     # compare against golden.json
    tests/regression/run.py --status-only       # ignore clause counts
    tests/regression/run.py --record [-k substr]   # accept current behaviour

The binary is `$EPROVER`, else `build/dev/bin/eprover` (`--binary` overrides).

Entries in `problems.txt` are `<problem> [config,...]`; configs are defined in
`run.py`. `fixed` uses a fixed heuristic plus a processed-clause limit and
compares exact processed/generated clause counts; `auto` compares status only.

## Reproducibility notes

* Runs are wrapped in `setarch -R`: E's behaviour depends on pointer addresses,
  so counts differ between runs under ASLR.
* The counts also depend on the *layout of the binary* (E orders some data by
  pointer address). Adding 100 kB of padding to `.bss` changed the search on
  one problem. Counts therefore reproduce only for the same compiler and
  flags. The CMake build pins `__FILE__` to the bare file name, as the old
  Makefiles implicitly did, so it reproduces the old build exactly. On other
  toolchains use `--status-only`, or re-record `golden.json` for that toolchain.

Only FO problems are included; the HO examples in `EXAMPLE_PROBLEMS/LFHOL`
need the HO build (`cmake --preset ho`) and should get their own entries.
