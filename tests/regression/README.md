# Regression suite

    ./configure && make          # build PROVER/eprover first
    tests/regression/run.py      # compare against golden.json
    tests/regression/run.py --record [-k substr]   # accept current behaviour

Entries in `problems.txt` are `<problem> [config,...]`; configs are defined in
`run.py`. `fixed` uses a fixed heuristic plus a processed-clause limit and
compares exact processed/generated clause counts; `auto` compares status only.

Runs are wrapped in `setarch -R`: E's behaviour depends on pointer addresses,
so counts differ between runs under ASLR.

Only FO problems are included; the HO examples in `EXAMPLE_PROBLEMS/LFHOL`
need an HO build (`--enable-ho`) and should get their own entries later.
