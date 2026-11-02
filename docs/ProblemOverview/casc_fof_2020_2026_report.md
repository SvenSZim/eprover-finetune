# E vs Vampire and hard problems in CASC FOF, 2020–2026

First-order theorem (FOF) division of seven CASC competitions: CASC-J10 (2020), CASC-28 (2021), CASC-J11 (2022), CASC-29 (2023), CASC-J12 (2024), CASC-30 (2025) and CASC-J13 (2026). Generated 2026-11-02.

## Summary

- **Data:** 3,400 problem slots (1,797 distinct problems) across 7 results tables. Every system's solved count I computed matches the page's own *Solved* row (106 of 106).
- **E's solve rate rose to a peak in 2023 and has fallen since:** 2020 70%, 2021 74%, 2022 77%, 2023 79%, 2024 74%, 2025 73%, 2026 66%. The gap to the best Vampire version narrowed from 91 problems (2020) to 74 (2022), then widened every year to 122 in 2026.
- **Most E failures are problems Vampire solves:** of 906 E failures over the seven years, 726 were solved by at least one Vampire version, 55 only by other systems, and 125 by nobody. Problems E solved that every Vampire version missed fell from 13 (2020) to 0 (2026).
- **Significant slowdowns** (E ≥ 10× and ≥ 10 s slower than the fastest Vampire version): 351 cases in total, 2020: 64, 2021: 67, 2022: 33, 2023: 43, 2024: 51, 2025: 60, 2026: 33. On easy problems E is close to Vampire (median under 0.7 s for both every year).
- **Hard problems:** 63 problems debuted in 2020–2026 and were solved by **no** system at that debut (21 of them brand-new problems). Of these, 19 were solved in a later CASC, 8 stayed unsolved when re-used, and 36 have not been re-used. A further 38 problems in the 2020–2026 tables had debuted unsolved in 2016–2019 (secondary list).
- **Who cracks hard problems later:** among hard problems first solved in 2020–2026, the first solvers were Vampire (37), E family (13), cvc51.0 (1), cvc51.1.3 (1), cvc51.3.0 (1), Twee2.4 (1) (a problem can have several first solvers; Vampire counts include SnakeForV, E family includes CSE_E/CSI_E/CSG_E/Enigma).

## Data and method

- **Source:** the per-problem FOF results tables on the official CASC results pages, e.g. [CASC-J13 results](https://tptp.org/CASC/J13/WWWFiles/Results.html#FOFProblems); the others are at the same path with J10, 28, J11, 29, J12 and 30. My workspace cannot reach tptp.org, so I loaded the pages in the built-in browser on your computer, extracted the tables with a script, and saved them as CSV. For the hard-problem lookback I also extracted the FOF problem lists of CASC-J8, 26, J9 and 27 (2016–2019).
- **Validation:** for every system in every year, my count of solved problems equals the page's *Solved* total (106/106), and the count of `+` cells equals the *Solutions* total. The 2026 values also match, cell for cell, the extract used in the earlier CASC-J13 report.
- **Problem descriptions:** taken from the problem headers in TPTP v9.3.1 ([distribution](https://tptp.org/TPTP/Distribution/)), streamed in the browser; found for 1797 of 1797 distinct problems. The TPTP rating is the current one (difficulty, 0 = easy, 1 = unsolved by current systems), not the rating at competition time. Links point to the new TPTP browser at seetptp.tptp.org (the old SeeTPTP links now redirect there).
- **Solved / failed:** a time in the cell means solved (with or without `+`, which marks that a proof was output, as CASC counts it). `TMO` = timeout, `UNK`/`GUP` = gave up, `ERR` = error. Older pages write these as `TMO-Non` etc.; I normalised them. CASC-30 (2025) has many solved cells without `+`.
- **Systems compared:** the E entry each year (E 2.5, 2.6, 3.0, 3.1, 3.2.0, 3.3.0, 3.5.1) against every system named *Vampire* that year (two versions each year). E-derived systems (CSE_E, CSI_E, CSG_E, Enigma) and the Vampire-derived SnakeForV (2022) are counted as "other systems", not as E or Vampire.
- **Significant slowdown:** E time ≥ 10× **and** ≥ 10 s more than the fastest Vampire version on that problem. *Moderate:* ≥ 3× and ≥ 5 s. The CSV also flags whether E was significantly slower than **every** Vampire version. Times are the values shown in the tables (seconds); I did not confirm whether these are wall-clock or CPU time.
- **Hard problem:** a problem that no entered system solved at its **first known appearance in the CASC FOF division**, looking back to 2016. *Primary list:* debut in 2020–2026. *Secondary list:* problems in the 2020–2026 tables whose debut was an unsolved 2016–2019 appearance. A problem "not marked new" may have been used before 2016, so its debut year is a lower bound. 2022–2024 had no new problems (the pages show *New Solved 0/0*).
- **Caveat:** each problem is one run per system per year, so single timings are noisy; system line-ups and problem sets change every year, so year-to-year rates are not strictly comparable.

## 1. E vs Vampire per year

| Year | Competition | E | Vampire versions | Problems | E solved | Best Vampire solved | E failures | …solved by Vampire | …only by others | …by nobody | E solved, all Vampire failed | Significant slowdowns | …vs every Vampire | Moderate | E faster by ≥1 s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2020 | CASC-J10 | E2.5 | Vampire4.5, Vampire4.4 | 500 | 351 (70%) | 442 | 149 | 104 | 12 | 33 | 13 | 64 | 40 | 23 | 24 |
| 2021 | CASC-28 | E2.6 | Vampire4.6, Vampire4.5 | 500 | 368 (74%) | 455 | 132 | 98 | 14 | 20 | 11 | 67 | 67 | 24 | 26 |
| 2022 | CASC-J11 | E3.0 | Vampire4.7, Vampire4.6 | 500 | 384 (77%) | 458 | 116 | 90 | 13 | 13 | 16 | 33 | 28 | 30 | 30 |
| 2023 | CASC-29 | E3.1 | Vampire4.8, Vampire4.7 | 500 | 393 (79%) | 475 | 107 | 87 | 5 | 15 | 5 | 43 | 23 | 28 | 40 |
| 2024 | CASC-J12 | E3.2.0 | Vampire4.9, Vampire4.8 | 500 | 370 (74%) | 476 | 130 | 108 | 4 | 18 | 2 | 51 | 37 | 21 | 17 |
| 2025 | CASC-30 | E3.3.0 | Vampire5.0, Vampire4.9 | 500 | 364 (73%) | 476 | 136 | 117 | 7 | 12 | 5 | 60 | 50 | 17 | 16 |
| 2026 | CASC-J13 | E3.5.1 | Vampire5.0.1, Vampire5.0 | 400 | 264 (66%) | 386 | 136 | 122 | 0 | 14 | 0 | 33 | 20 | 20 | 15 |

*Best Vampire solved* counts problems solved by at least one Vampire version. E failure status: 2020: TMO 146, UNK 3; 2021: TMO 132; 2022: TMO 116; 2023: TMO 107; 2024: TMO 130; 2025: TMO 136; 2026: TMO 136.

## 2. E failures

All 906 failures (one row per year and problem, with descriptions) are in `e_failures_2020_2026.csv`.

### By TPTP domain (all years)

| Domain | Name | E failures | Problem slots | Failure rate |
|---|---|---|---|---|
| GEO | Geometry | 129 | 407 | 32% |
| SWB | Semantic Web | 103 | 262 | 39% |
| NUM | Number Theory | 99 | 241 | 41% |
| LCL | Logic Calculi | 93 | 275 | 34% |
| ITP | Interactive Theorem Proving | 69 | 161 | 43% |
| CSR | Commonsense Reasoning | 37 | 344 | 11% |
| SCT | Social Choice Theory | 37 | 89 | 42% |
| SWW | Software Verification | 37 | 247 | 15% |
| SEV | Set Theory | 34 | 64 | 53% |
| SEU | Set Theory | 30 | 84 | 36% |
| LAT | Lattice Theory | 27 | 44 | 61% |
| AGT | Agents | 23 | 30 | 77% |
| HWV | Hardware Verification | 20 | 21 | 95% |
| ALG | Algebra | 16 | 49 | 33% |
| SET | Set Theory | 16 | 95 | 17% |

### Persistent failures: E failed in every appearance (at least 4 appearances)

| Problem | Domain | Appearances | Description | TPTP rating | Solved by Vampire in |
|---|---|---|---|---|---|
| [NUM695+4](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/NUM/NUM695+4.p) | NUM | 7 | Grundlagen problem satz24b | 0.91 | 2021, 2023, 2024, 2025, 2026 |
| [GEO167+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/GEO/GEO167+1.p) | GEO | 6 | Pappus1 implies Pappus2 | 0.00 | 2020, 2021, 2022, 2023, 2024, 2025 |
| [ITP018+5](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/ITP/ITP018+5.p) | ITP | 6 | HOL4 set theory export of thm_2Ebinary__ieee_2Eneg__ulp.p, chainy mode | 0.91 | 2020, 2021, 2022, 2023, 2024, 2026 |
| [LCL876+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/LCL/LCL876+1.p) | LCL | 6 | Prove Mv5 from MV1--MV4 | 0.80 | never |
| [GEO109+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/GEO/GEO109+1.p) | GEO | 5 | Every endpoint of an open curve is not between any other points | 0.91 | 2020, 2022, 2023, 2025 |
| [GEO337+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/GEO/GEO337+1.p) | GEO | 5 | conjunct2(397)-holds(conjunct2(397),1382,0) | 0.78 | 2020, 2023, 2024, 2025, 2026 |
| [GEO513+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/GEO/GEO513+1.p) | GEO | 5 | External same side | 0.78 | 2020, 2021, 2023, 2025, 2026 |
| [NUM671+4](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/NUM/NUM671+4.p) | NUM | 5 | Grundlagen problem satz19b | 0.91 | 2024, 2025, 2026 |
| [SWB020+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SWB/SWB020+1.p) | SWB | 5 | Logical Complications | 0.83 | 2020, 2022, 2024, 2025, 2026 |
| [SWB102+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SWB/SWB102+1.p) | SWB | 5 | Data-QCR As Object-QCR | 0.91 | 2024, 2025 |
| [SWW470+6](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SWW/SWW470+6.p) | SWW | 5 | Hoare's Logic with Procedures line 200, 500 axioms selected | 0.61 | 2021, 2022, 2023, 2024, 2025 |
| [AGT012+2](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/AGT/AGT012+2.p) | AGT | 4 | Problem for the CPlanT system | 0.65 | 2020, 2021, 2022, 2023 |
| [COM145+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/COM/COM145+1.p) | COM | 4 | T-Preservation-T-app step in progress/preservation proof | 0.87 | 2020, 2023, 2024 |
| [GEO321+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/GEO/GEO321+1.p) | GEO | 4 | 374-holds(374,1342,0) | 0.61 | 2020, 2024, 2025, 2026 |
| [GEO324+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/GEO/GEO324+1.p) | GEO | 4 | conjunct2(conjunct2(375))-holds(conjunct2(conjunct2(375)),1345,0) | 0.91 | 2020, 2022, 2023, 2024 |
| [GEO514+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/GEO/GEO514+1.p) | GEO | 4 | External same side | 0.74 | 2021, 2024, 2025, 2026 |
| [GEO520+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/GEO/GEO520+1.p) | GEO | 4 | Transitivity of samesideline, lemma g | 0.87 | 2022, 2025, 2026 |
| [ITP009+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/ITP/ITP009+1.p) | ITP | 4 | HOL4 syntactic export of thm_2Equotient_2EFUN__REL__EQ__REL.p, bushy… | 0.87 | 2024, 2025 |
| [NUM669+4](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/NUM/NUM669+4.p) | NUM | 4 | Grundlagen problem satz18b | 0.87 | 2023, 2026 |
| [NUM736+4](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/NUM/NUM736+4.p) | NUM | 4 | Grundlagen problem satz42 | 0.78 | 2020, 2021, 2024, 2025 |
| [NUM926+4](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/NUM/NUM926+4.p) | NUM | 4 | Sum of two squares line 258, 5000 axioms selected | 0.70 | 2022, 2023, 2024, 2025 |
| [SCT170+3](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SCT/SCT170+3.p) | SCT | 4 | Arrow's Impossibility Theorem line 204, 1000 axioms selected | 0.91 | 2024, 2026 |
| [SWB014+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SWB/SWB014+1.p) | SWB | 4 | Harry belongs to some Species | 0.74 | 2022, 2023, 2024, 2025 |
| [SWB025+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SWB/SWB025+1.p) | SWB | 4 | Cyclic Dependencies between Complex Properties | 0.70 | 2021, 2022, 2023, 2025 |
| [SWB050+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SWB/SWB050+1.p) | SWB | 4 | Symmetric Property Extensional | 0.74 | 2021, 2022, 2024, 2025 |
| [SWB091+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SWB/SWB091+1.p) | SWB | 4 | Max-1-QCR Extensional | 0.87 | 2021, 2022, 2024, 2026 |
| [SWB098+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SWB/SWB098+1.p) | SWB | 4 | Existential Restriction Comparison By Class | 0.87 | 2022, 2023, 2024, 2025 |
| [SWB099+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SWB/SWB099+1.p) | SWB | 4 | Existential Restriction Comparison By Property | 0.87 | 2022, 2024, 2025, 2026 |
| [SWB103+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SWB/SWB103+1.p) | SWB | 4 | Exact-QCR As Min-QCR Max-QCR Intersection | 0.87 | 2021, 2024, 2025, 2026 |
| [SWW098+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SWW/SWW098+1.p) | SWW | 4 | Equivalence of or1 and or2 | 0.78 | 2020, 2022, 2023, 2024 |
| [SYN076+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SYN/SYN076+1.p) | SYN | 4 | Pelletier Problem 53 | 0.74 | 2021, 2023, 2024, 2026 |

125 of the failures were problems no system solved that year; these overlap heavily with the hard-problem lists in section 4.

## 3. E significantly slower than Vampire

351 significant and 163 moderate cases; all are in `e_slower_than_vampire_2020_2026.csv`. Most affected domains: GEO (38), SWB (37), SWV (36), ITP (27), LCL (26), SWW (22), CSR (22), SCT (18).

### The 30 largest slowdowns (by extra seconds)

| Year | Problem | E | E time (s) | Fastest Vampire | Vampire time (s) | E / Vampire | Extra s | Description |
|---|---|---|---|---|---|---|---|---|
| 2025 | [SCT154+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SCT/SCT154+1.p) | E3.3.0 | 239.87 | Vampire4.9 | 0.39 | 615× | +239 | Arrow's Impossibility Theorem 433319, 500 axioms selected |
| 2025 | [NUN075+2](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/NUN/NUN075+2.p) | E3.3.0 | 221.03 | Vampire4.9 | 0.40 | 553× | +221 | Robinson arithmetic: 7 + 2 = 9 |
| 2025 | [LAT374+3](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/LAT/LAT374+3.p) | E3.3.0 | 198.28 | Vampire4.9 | 1.10 | 180× | +197 | Duality Based on Galois Connection - Part I T49 |
| 2025 | [SWB067+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SWB/SWB067+1.p) | E3.3.0 | 185.69 | Vampire5.0 | 0.36 | 516× | +185 | Double Inverse Property As Equivalence |
| 2024 | [SWW874+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SWW/SWW874+1.p) | E3.2.0 | 179.92 | Vampire4.9 | 0.57 | 316× | +179 | envRel__1__convert_append_decls__dep |
| 2024 | [MGT035+2](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/MGT/MGT035+2.p) | E3.2.0 | 179.91 | Vampire4.8 | 0.77 | 234× | +179 | EPs outcompete FMs in stable environments |
| 2024 | [SWB067+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SWB/SWB067+1.p) | E3.2.0 | 178.76 | Vampire4.9 | 0.33 | 542× | +178 | Double Inverse Property As Equivalence |
| 2025 | [SWV458+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SWV/SWV458+1.p) | E3.3.0 | 178.29 | Vampire4.9 | 0.32 | 557× | +178 | Establishing that there cannot be two leaders, part i31_p257 |
| 2023 | [LCL656+1.020](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/LCL/LCL656+1.020.p) | E3.1 | 178.13 | Vampire4.8 | 1.81 | 98× | +176 | In KT, the branching formula made provable, size 20 |
| 2023 | [GEO292+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/GEO/GEO292+1.p) | E3.1 | 178.46 | Vampire4.7 | 3.49 | 51× | +175 | 299-holds(299,1238,0) |
| 2025 | [SET098+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SET/SET098+1.p) | E3.3.0 | 175.25 | Vampire5.0 | 0.31 | 565× | +175 | Corollary 1 to a class contains 0, 1, or at least 2 members |
| 2024 | [SCT123+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SCT/SCT123+1.p) | E3.2.0 | 171.64 | Vampire4.9 | 0.37 | 464× | +171 | Arrow's Impossibility Theorem 433003, 500 axioms selected |
| 2026 | [SEU269+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SEU/SEU269+1.p) | E3.5.1 | 171.13 | Vampire5.0 | 0.50 | 342× | +171 | MPTP bushy problem t3_wellord2 |
| 2023 | [NUN075+2](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/NUN/NUN075+2.p) | E3.1 | 167.85 | Vampire4.7 | 0.29 | 579× | +168 | Robinson arithmetic: 7 + 2 = 9 |
| 2025 | [SCT123+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SCT/SCT123+1.p) | E3.3.0 | 164.07 | Vampire4.9 | 0.37 | 443× | +164 | Arrow's Impossibility Theorem 433003, 500 axioms selected |
| 2025 | [AGT023+2](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/AGT/AGT023+2.p) | E3.3.0 | 160.22 | Vampire5.0 | 0.39 | 411× | +160 | Problem for the CPlanT system |
| 2025 | [REL021+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/REL/REL021+1.p) | E3.3.0 | 163.41 | Vampire4.9 | 7.54 | 22× | +156 | Restriction of subidentities |
| 2025 | [KRS203+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/KRS/KRS203+1.p) | E3.3.0 | 153.40 | Vampire4.9 | 0.28 | 548× | +153 | SAT nota THM |
| 2025 | [KRS260+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/KRS/KRS260+1.p) | E3.3.0 | 153.37 | Vampire5.0 | 0.32 | 479× | +153 | WEC mighta THM |
| 2025 | [SET144+3](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SET/SET144+3.p) | E3.3.0 | 152.90 | Vampire5.0 | 0.35 | 437× | +153 | If X is a subset of Z, then X U Y ^ Z = (X U Y) ^ Z |
| 2023 | [SCT123+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SCT/SCT123+1.p) | E3.1 | 149.26 | Vampire4.8 | 0.77 | 194× | +148 | Arrow's Impossibility Theorem 433003, 500 axioms selected |
| 2025 | [NUN056+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/NUN/NUN056+1.p) | E3.3.0 | 148.77 | Vampire4.9 | 1.04 | 143× | +148 | Robinson arithmetic: 1+2=3 |
| 2025 | [SEU356+2](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SEU/SEU356+2.p) | E3.3.0 | 146.70 | Vampire5.0 | 0.46 | 319× | +146 | MPTP chainy problem t15_yellow_0 |
| 2025 | [GEO168+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/GEO/GEO168+1.p) | E3.3.0 | 149.69 | Vampire4.9 | 3.67 | 41× | +146 | Pappus2 implies Pappus1 |
| 2023 | [SWW470+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SWW/SWW470+1.p) | E3.1 | 145.56 | Vampire4.7 | 0.50 | 291× | +145 | Hoare's Logic with Procedures line 200, 100 axioms selected |
| 2023 | [GEO525+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/GEO/GEO525+1.p) | E3.1 | 145.86 | Vampire4.7 | 14.57 | 10× | +131 | Right triangle theorem (Euclid 4) |
| 2026 | [SEV655+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SEV/SEV655+1.p) | E3.5.1 | 133.57 | Vampire5.0.1 | 3.14 | 42× | +130 | CoqHammer - Maplists ad list Elems |
| 2025 | [REL035+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/REL/REL035+1.p) | E3.3.0 | 136.84 | Vampire4.9 | 7.66 | 18× | +129 | Propagation of vectors |
| 2025 | [SWB101+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SWB/SWB101+1.p) | E3.3.0 | 123.04 | Vampire4.9 | 0.54 | 228× | +122 | Cardinality Restriction As QCR |
| 2025 | [SWX070+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SWX/SWX070+1.p) | E3.3.0 | 130.76 | Vampire4.9 | 8.78 | 15× | +122 | If valid/1 fails then false/3 succeeds |

65 problems were significant slowdowns in two or more years: GEO295+1 (5×), NUN066+1 (5×), SWB097+1 (5×), ITP004+4 (4×), SCT117+1 (4×), SYN986+1.004 (4×), GEO292+1 (3×), LCL656+1.015 (3×), MED009+1 (3×), PUZ077+1 (3×), SCT120+1 (3×), SCT122+1 (3×), SCT123+1 (3×), SWB059+1 (3×), SWB067+1 (3×), SWB108+1 (3×), SWV459+1 (3×), SWV491+4 (3×), SWW470+1 (3×), SYO606+1 (3×), COM148+1 (2×), CSR027+2 (2×), CSR038+2 (2×), CSR044+2 (2×), GEO273+1 (2×), GEO281+1 (2×), GEO283+1 (2×), GEO286+1 (2×), GEO507+1 (2×), GEO521+1 (2×), GEO535+1 (2×), ITP004+1 (2×), ITP004+5 (2×), ITP006+1 (2×), ITP012+1 (2×), ITP012+4 (2×), ITP015+1 (2×), ITP015+2 (2×), ITP023+1 (2×), KLE169+1 (2×), LCL642+1.010 (2×), LCL652+1.015 (2×), MED007+1 (2×), NUM859+1 (2×), NUM926+2 (2×), NUM926+3 (2×), NUN055+1 (2×), NUN056+1 (2×), NUN058+2 (2×), NUN075+2 (2×), SCT115+1 (2×), SWB028+1 (2×), SWB056+1 (2×), SWB101+1 (2×), SWV234+1 (2×), SWV458+1 (2×), SWV460+1 (2×), SWV470+1 (2×), SWV471+1 (2×), SWV487+3 (2×), SWV492+1 (2×), SWW096+1 (2×), SWW470+2 (2×), SWW474+5 (2×), SWW474+7 (2×).

## 4. Hard problems (unsolved at first appearance)

### Primary list: debut in 2020–2026 (63)

`*` = new problem (not previously seen by the systems) at debut. *Later history* lists later CASC FOF appearances as solved/entered systems.

| Debut | Problem | Domain | Description | TPTP rating | Later history | First solved | Status |
|---|---|---|---|---|---|---|---|
| 2020 | [ITP003+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/ITP/ITP003+1.p)* | ITP | HOL4 syntactic export of thm_2Earithmetic_2EMOD__2.p, bushy mode | 0.87 | 2023: 1/13; 2025: 4/15 | 2023: E3.1 (1.94s) | solved in a later CASC |
| 2020 | [ITP007+2](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/ITP/ITP007+2.p)* | ITP | HOL4 set theory export of thm_2EpatternMatches_2EPMATCH__FLATTEN__FUN… | 1.00 | 2021: 0/17 | – | never solved in a later CASC |
| 2020 | [ITP007+5](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/ITP/ITP007+5.p)* | ITP | HOL4 set theory export of thm_2EpatternMatches_2EPMATCH__FLATTEN__FUN… | 1.00 | – | – | not re-used since |
| 2020 | [ITP009+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/ITP/ITP009+1.p)* | ITP | HOL4 syntactic export of thm_2Equotient_2EFUN__REL__EQ__REL.p, bushy… | 0.87 | 2021: 1/17; 2024: 2/14; 2025: 3/15 | 2021: cvc51.0 (48.66s) | solved in a later CASC |
| 2020 | [ITP013+5](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/ITP/ITP013+5.p)* | ITP | HOL4 set theory export of thm_2Ewords_2En2w__sub.p, chainy mode | 0.96 | – | – | not re-used since |
| 2020 | [ITP014+2](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/ITP/ITP014+2.p)* | ITP | HOL4 set theory export of thm_2Ebitstring_2Eword__1comp__v2w.p, bushy… | 1.00 | 2021: 0/17 | – | never solved in a later CASC |
| 2020 | [ITP016+2](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/ITP/ITP016+2.p)* | ITP | HOL4 set theory export of thm_2Ereal_2ESUP__EPSILON.p, bushy mode | 1.00 | – | – | not re-used since |
| 2020 | [ITP016+5](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/ITP/ITP016+5.p)* | ITP | HOL4 set theory export of thm_2Ereal_2ESUP__EPSILON.p, chainy mode | 1.00 | – | – | not re-used since |
| 2020 | [ITP017+5](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/ITP/ITP017+5.p)* | ITP | HOL4 set theory export of thm_2Eseq_2EBOLZANO__LEMMA.p, chainy mode | 1.00 | – | – | not re-used since |
| 2020 | [ITP022+5](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/ITP/ITP022+5.p)* | ITP | HOL4 set theory export of thm_2Ereal__topology_2EINDEPENDENT__STDBASI… | 1.00 | – | – | not re-used since |
| 2020 | [ITP023+5](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/ITP/ITP023+5.p)* | ITP | HOL4 set theory export of thm_2Ereal__topology_2EBOUNDED__BALL.p, cha… | 0.96 | 2021: 0/17 | – | never solved in a later CASC |
| 2020 | [ITP025+2](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/ITP/ITP025+2.p)* | ITP | HOL4 set theory export of thm_2Elebesgue_2Epos__fn__integral__cmul.p,… | 1.00 | – | – | not re-used since |
| 2020 | [ITP025+5](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/ITP/ITP025+5.p)* | ITP | HOL4 set theory export of thm_2Elebesgue_2Epos__fn__integral__cmul.p,… | 1.00 | – | – | not re-used since |
| 2020 | [LCL482+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/LCL/LCL482+1.p) | LCL | Prove Rosser's kn3 axiom from Lukasiewicz's axiomatization | 0.91 | – | – | not re-used since |
| 2020 | [LCL564+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/LCL/LCL564+1.p) | LCL | Prove axiom K from the S1-0M6S3M9B axiomatization of S5 | 0.96 | – | – | not re-used since |
| 2020 | [NUM671+4](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/NUM/NUM671+4.p) | NUM | Grundlagen problem satz19b | 0.91 | 2023: 0/13; 2024: 1/14; 2025: 3/15; 2026: 3/17 | 2024: Vampire4.9 (2.49s) | solved in a later CASC |
| 2020 | [NUM749+4](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/NUM/NUM749+4.p) | NUM | Grundlagen problem satz60a | 0.91 | 2024: 1/14 | 2024: Vampire4.9 (10.95s) | solved in a later CASC |
| 2020 | [NUM782+4](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/NUM/NUM782+4.p) | NUM | Grundlagen problem satz80 | 0.91 | 2024: 1/14; 2025: 1/15 | 2024: Vampire4.9 (5.34s) | solved in a later CASC |
| 2020 | [SEU339+2](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SEU/SEU339+2.p) | SEU | MPTP chainy problem t25_orders_2 | 0.74 | – | – | not re-used since |
| 2021 | [GEO350+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/GEO/GEO350+1.p) | GEO | conseq_conjunct1(422)-holds(conseq_conjunct1(422),1474,0) | 0.96 | 2025: 0/15 | – | never solved in a later CASC |
| 2021 | [ITP002+2](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/ITP/ITP002+2.p)* | ITP | HOL4 set theory export of thm_2Eoption_2EOPTION__MAP2__THM.p, bushy m… | 0.83 | 2024: 2/14; 2026: 2/17 | 2024: Vampire4.9 (7.05s), cvc51.1.3 (43.51s) | solved in a later CASC |
| 2021 | [ITP002+5](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/ITP/ITP002+5.p)* | ITP | HOL4 set theory export of thm_2Eoption_2EOPTION__MAP2__THM.p, chainy… | 1.00 | 2025: 1/15 | 2025: Vampire4.9 (3.33s) | solved in a later CASC |
| 2021 | [LAT349+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/LAT/LAT349+1.p) | LAT | Representation Theorem for Free Continuous Lattices T12 | 0.91 | – | – | not re-used since |
| 2021 | [LAT379+3](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/LAT/LAT379+3.p) | LAT | Duality Based on Galois Connection - Part I T65 | 0.91 | 2023: 1/13 | 2023: Vampire4.7 (5.40s) | solved in a later CASC |
| 2021 | [NUN075+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/NUN/NUN075+1.p) | NUN | Robinson arithmetic: 7 + 2 = 9 | 0.80 | 2022: 0/14; 2025: 3/15; 2026: 2/17 | 2025: Vampire5.0 (82.13s), E3.3.0 (153.22s), CSI_E… | solved in a later CASC |
| 2021 | [SCT170+6](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SCT/SCT170+6.p) | SCT | Arrow's Impossibility Theorem line 204, 500 axioms selected | 0.91 | 2025: 0/15 | – | never solved in a later CASC |
| 2022 | [CAT028+2](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/CAT/CAT028+2.p) | CAT | Some Isomorphisms Between Functor Categories T41 | 0.87 | – | – | not re-used since |
| 2022 | [GEO459+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/GEO/GEO459+1.p) | GEO | Flyspeck project step | 0.96 | – | – | not re-used since |
| 2022 | [KLE166+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/KLE/KLE166+1.p) | KLE | Strong iteration | 0.78 | – | – | not re-used since |
| 2022 | [LCL545+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/LCL/LCL545+1.p) | LCL | Prove axiom m5 from KM4B axiomatization of S5 | 1.00 | – | – | not re-used since |
| 2022 | [LCL662+1.020](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/LCL/LCL662+1.020.p) | LCL | In KT, in backward search find a way through box and dia, size 20 | 0.80 | 2026: 0/17 | – | never solved in a later CASC |
| 2023 | [NUM653+4](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/NUM/NUM653+4.p) | NUM | Grundlagen problem satz10d | 0.91 | 2024: 0/14; 2026: 1/17 | 2026: Vampire5.0.1 (2.14s) | solved in a later CASC |
| 2023 | [NUM655+4](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/NUM/NUM655+4.p) | NUM | Grundlagen problem satz10f | 0.91 | 2024: 1/14 | 2024: Vampire4.9 (1.26s) | solved in a later CASC |
| 2023 | [NUM657+4](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/NUM/NUM657+4.p) | NUM | Grundlagen problem satz10h | 0.91 | 2026: 2/17 | 2026: Vampire5.0.1 (3.19s), Vampire5.0 (2.70s) | solved in a later CASC |
| 2023 | [NUM703+4](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/NUM/NUM703+4.p) | NUM | Grundlagen problem satz26c | 0.91 | 2024: 0/14; 2025: 1/15 | 2025: Vampire5.0 (16.36s) | solved in a later CASC |
| 2023 | [NUM788+4](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/NUM/NUM788+4.p) | NUM | Grundlagen problem satz81g | 0.91 | 2025: 2/15 | 2025: Vampire5.0 (6.06s), Vampire4.9 (1.51s) | solved in a later CASC |
| 2023 | [SET998+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SET/SET998+1.p) | SET | Functions and their basic properties, theorem 20 | 0.87 | – | – | not re-used since |
| 2023 | [SWW881+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SWW/SWW881+1.p) | SWW | clos_relation__26__get_global_state_rel__dep | 0.96 | – | – | not re-used since |
| 2024 | [GEO527+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/GEO/GEO527+1.p) | GEO | Two right triangles with congruent legs have congruent hypotenuses | 1.00 | 2025: 0/15 | – | never solved in a later CASC |
| 2024 | [KLE049+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/KLE/KLE049+1.p) | KLE | Hoare rule while | 1.00 | – | – | not re-used since |
| 2024 | [LCL670+1.015](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/LCL/LCL670+1.015.p) | LCL | In KT, formula with T and A4, size 15 | 0.80 | – | – | not re-used since |
| 2024 | [NUM702+4](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/NUM/NUM702+4.p) | NUM | Grundlagen problem satz26b | 0.91 | – | – | not re-used since |
| 2024 | [NUM750+4](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/NUM/NUM750+4.p) | NUM | Grundlagen problem satz62b | 0.96 | 2026: 1/17 | 2026: Vampire5.0.1 (5.68s) | solved in a later CASC |
| 2024 | [NUM785+4](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/NUM/NUM785+4.p) | NUM | Grundlagen problem satz81d | 0.91 | 2025: 0/15; 2026: 1/17 | 2026: Vampire5.0.1 (3.25s) | solved in a later CASC |
| 2024 | [SEU440+2](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SEU/SEU440+2.p) | SEU | First and Second Order Cutting of Binary Relations T52 | 0.96 | – | – | not re-used since |
| 2024 | [SEV522+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SEV/SEV522+1.p) | SEV | Subfamily of a non-overlapping family is a non-overlapping family | 0.91 | 2025: 1/15; 2026: 1/17 | 2025: cvc51.3.0 (230.62s) | solved in a later CASC |
| 2024 | [SWW910+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SWW/SWW910+1.p) | SWW | word_to_stackProof__192__tactictoe_prove_191__dep | 0.91 | – | – | not re-used since |
| 2025 | [LCL109+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/LCL/LCL109+1.p)* | LCL | MV-4 depends on the Meredith system | 0.80 | 2026: 0/17 | – | never solved in a later CASC |
| 2025 | [NUM783+4](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/NUM/NUM783+4.p) | NUM | Grundlagen problem satz81a | 0.96 | 2026: 1/17 | 2026: Vampire5.0.1 (111.80s) | solved in a later CASC |
| 2025 | [NUM787+4](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/NUM/NUM787+4.p) | NUM | Grundlagen problem satz81f | 0.96 | 2026: 2/17 | 2026: Vampire5.0.1 (3.18s), Vampire5.0 (7.59s) | solved in a later CASC |
| 2025 | [NUN072+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/NUN/NUN072+1.p) | NUN | Robinson arithmetic: 1 * 2 = 2 | 1.00 | – | – | not re-used since |
| 2025 | [SEU258+2](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SEU/SEU258+2.p) | SEU | MPTP chainy problem t39_wellord1 | 0.96 | – | – | not re-used since |
| 2025 | [SEU447+2](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SEU/SEU447+2.p) | SEU | First and Second Order Cutting of Binary Relations T59 | 0.91 | – | – | not re-used since |
| 2026 | [GEO095+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/GEO/GEO095+1.p) | GEO | Endpoints of open sum are endpoints of curves | 0.96 | – | – | not re-used since |
| 2026 | [GEO501+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/GEO/GEO501+1.p) | GEO | Diagonals bisect | 0.96 | – | – | not re-used since |
| 2026 | [GRP652+2](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/GRP/GRP652+2.p) | GRP | On the Lattice of Subgroups of a Group T35 | 0.96 | – | – | not re-used since |
| 2026 | [SEU440+4](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SEU/SEU440+4.p) | SEU | First and Second Order Cutting of Binary Relations T52 | 0.96 | – | – | not re-used since |
| 2026 | [SEV618+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SEV/SEV618+1.p)* | SEV | CoqHammer - HahnEquational.pow seq | 0.96 | – | – | not re-used since |
| 2026 | [SEV650+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SEV/SEV650+1.p)* | SEV | CoqHammer - Mapc FSetInter Union r | 0.91 | – | – | not re-used since |
| 2026 | [SEV654+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SEV/SEV654+1.p)* | SEV | CoqHammer - Maplists ad in list app 1 | 0.96 | – | – | not re-used since |
| 2026 | [SWX189+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SWX/SWX189+1.p)* | SWX | Finding an antiderivative | 0.88 | – | – | not re-used since |
| 2026 | [SWX201+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SWX/SWX201+1.p)* | SWX | Faulty property about permutations | 0.96 | – | – | not re-used since |
| 2026 | [TOP020+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/TOP/TOP020+1.p) | TOP | Property of a Hausdorff topological space | 0.91 | – | – | not re-used since |

Primary hard problems by debut year: 2020: 19, 2021: 7, 2022: 5, 2023: 7, 2024: 9, 2025: 6, 2026: 10.
Of those later solved, the median time until a first solve was 2 years (range 1–4).

### Secondary list: debuted unsolved in 2016–2019 (38)

| Debut | Problem | Domain | Description | Later history | First solved | Status |
|---|---|---|---|---|---|---|
| 2016 | [COM124+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/COM/COM124+1.p)* | COM | T-Weak-FreeVar-abs-2 step in progress/preservation proof | 2017: 2/11; 2019: 4/16; 2021: 4/17; 2022: 7/14 | 2017 | solved in a later CASC |
| 2016 | [COM145+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/COM/COM145+1.p)* | COM | T-Preservation-T-app step in progress/preservation proof | 2017: 2/11; 2019: 0/16; 2020: 1/16; 2022: 0/14; 2023: 2/13; 2024: 1/14 | 2017 | solved in a later CASC |
| 2016 | [GEO167+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/GEO/GEO167+1.p) | GEO | Pappus1 implies Pappus2 | 2017: 3/11; 2018: 3/14; 2020: 3/16; 2021: 4/17; 2022: 5/14; 2023: 2/13; 2024: 3/14; 2025: 3/15 | 2017 | solved in a later CASC |
| 2016 | [LCL638+1.015](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/LCL/LCL638+1.015.p) | LCL | In K, D & A4 & B{~p0/p0} -> T, size 15 | 2018: 2/14; 2020: 2/16; 2022: 2/14; 2024: 2/14 | 2018 | solved in a later CASC |
| 2016 | [LCL682+1.020](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/LCL/LCL682+1.020.p) | LCL | In S4, path through a labyrinth, size 20 | 2017: 1/11; 2019: 0/16; 2020: 0/16; 2022: 4/14; 2025: 3/15 | 2017 | solved in a later CASC |
| 2016 | [LCL876+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/LCL/LCL876+1.p) | LCL | Prove Mv5 from MV1--MV4 | 2017: 0/11; 2018: 0/14; 2019: 0/16; 2020: 0/16; 2021: 0/17; 2022: 0/14; 2023: 0/13; 2024: 0/14; 2025: 0/15 | – | never solved in a later CASC |
| 2016 | [REL033+4](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/REL/REL033+4.p) | REL | Sequential composition distributes in each argument of meet | 2021: 1/17; 2025: 4/15 | 2021 | solved in a later CASC |
| 2016 | [SCT125+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SCT/SCT125+1.p) | SCT | Arrow's Impossibility Theorem 433097, 500 axioms selected | 2023: 2/13; 2026: 1/17 | 2023 | solved in a later CASC |
| 2016 | [SCT132+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SCT/SCT132+1.p) | SCT | Arrow's Impossibility Theorem 433149, 500 axioms selected | 2024: 2/14 | 2024 | solved in a later CASC |
| 2017 | [GEO325+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/GEO/GEO325+1.p) | GEO | conjunct2(376)-holds(conjunct2(376),1346,0) | 2019: 0/16; 2020: 0/16; 2022: 0/14; 2025: 0/15 | – | never solved in a later CASC |
| 2017 | [GEO441+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/GEO/GEO441+1.p)* | GEO | Flyspeck project step | 2024: 3/14 | 2024 | solved in a later CASC |
| 2017 | [GEO491+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/GEO/GEO491+1.p)* | GEO | Simple theorem on congruence and betweenness | 2019: 3/16; 2020: 0/16; 2025: 2/15; 2026: 4/17 | 2019 | solved in a later CASC |
| 2017 | [GEO520+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/GEO/GEO520+1.p)* | GEO | Transitivity of samesideline, lemma g | 2019: 1/16; 2022: 3/14; 2024: 0/14; 2025: 2/15; 2026: 2/17 | 2019 | solved in a later CASC |
| 2017 | [LCL636+1.010](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/LCL/LCL636+1.010.p) | LCL | In K, the branching formula made provable, size 10 | 2020: 1/16 | 2020 | solved in a later CASC |
| 2017 | [LCL638+1.020](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/LCL/LCL638+1.020.p) | LCL | In K, D & A4 & B{~p0/p0} -> T, size 20 | 2018: 2/14; 2021: 2/17; 2026: 1/17 | 2018 | solved in a later CASC |
| 2017 | [LCL662+1.010](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/LCL/LCL662+1.010.p) | LCL | In KT, in backward search find a way through box and dia, size 10 | 2019: 0/16; 2023: 0/13 | – | never solved in a later CASC |
| 2017 | [LCL688+1.005](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/LCL/LCL688+1.005.p) | LCL | In S4, formula with T and A4, size 5 | 2018: 2/14; 2025: 3/15 | 2018 | solved in a later CASC |
| 2017 | [LCL688+1.010](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/LCL/LCL688+1.010.p) | LCL | In S4, formula with T and A4, size 10 | 2018: 1/14; 2021: 0/17 | 2018 | solved in a later CASC |
| 2017 | [SWB102+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SWB/SWB102+1.p) | SWB | Data-QCR As Object-QCR | 2020: 0/16; 2021: 0/17; 2022: 1/14; 2024: 1/14; 2025: 2/15 | 2022 | solved in a later CASC |
| 2018 | [GEO302+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/GEO/GEO302+1.p) | GEO | conjunct1(conjunct2(338))-holds(conjunct1(conjunct2(338)),1269,0) | 2020: 2/16; 2023: 0/13 | 2020 | solved in a later CASC |
| 2018 | [GEO309+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/GEO/GEO309+1.p) | GEO | conjunct1(359)-holds(conjunct1(359),1318,0) | 2020: 0/16; 2022: 1/14; 2023: 1/13 | 2022 | solved in a later CASC |
| 2018 | [GEO324+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/GEO/GEO324+1.p) | GEO | conjunct2(conjunct2(375))-holds(conjunct2(conjunct2(375)),1345,0) | 2019: 1/16; 2020: 1/16; 2022: 2/14; 2023: 1/13; 2024: 1/14 | 2019 | solved in a later CASC |
| 2018 | [GRP664+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/GRP/GRP664+1.p) | GRP | Conjugacy closed with ab = 1 implies ba is in the nucleus - a | 2021: 2/17; 2022: 2/14; 2025: 3/15 | 2021 | solved in a later CASC |
| 2018 | [KLE121+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/KLE/KLE121+1.p) | KLE | Validity of composition rule | 2020: 3/16 | 2020 | solved in a later CASC |
| 2018 | [LCL646+1.010](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/LCL/LCL646+1.010.p) | LCL | In K, path through a labyrinth, size 10 | 2026: 2/17 | 2026 | solved in a later CASC |
| 2018 | [PUZ076+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/PUZ/PUZ076+1.p) | PUZ | Cell is not west of the other in the Wumpus world | 2019: 1/16; 2023: 1/13 | 2019 | solved in a later CASC |
| 2018 | [SCT169+3](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SCT/SCT169+3.p) | SCT | Arrow's Impossibility Theorem line 29, 1000 axioms selected | 2019: 0/16; 2020: 0/16; 2024: 2/14 | 2024 | solved in a later CASC |
| 2019 | [GEO313+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/GEO/GEO313+1.p) | GEO | 361-holds(361,1323,0) | 2021: 0/17 | – | never solved in a later CASC |
| 2019 | [GEO468+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/GEO/GEO468+1.p) | GEO | Flyspeck project step | 2020: 1/16 | 2020 | solved in a later CASC |
| 2019 | [HWV108+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/HWV/HWV108+1.p) | HWV | dmu_dmc property 18 cone of influence 5_b20 | 2021: 2/17; 2023: 2/13 | 2021 | solved in a later CASC |
| 2019 | [LCL688+1.015](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/LCL/LCL688+1.015.p) | LCL | In S4, formula with T and A4, size 15 | 2026: 2/17 | 2026 | solved in a later CASC |
| 2019 | [NUM695+4](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/NUM/NUM695+4.p)* | NUM | Grundlagen problem satz24b | 2020: 0/16; 2021: 1/17; 2022: 0/14; 2023: 2/13; 2024: 1/14; 2025: 2/15; 2026: 2/17 | 2021 | solved in a later CASC |
| 2019 | [NUM697+4](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/NUM/NUM697+4.p)* | NUM | Grundlagen problem satz25a | 2020: 0/16; 2022: 0/14; 2023: 0/13 | – | never solved in a later CASC |
| 2019 | [NUM701+4](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/NUM/NUM701+4.p)* | NUM | Grundlagen problem satz26a | 2020: 0/16; 2023: 0/13; 2025: 1/15 | 2025 | solved in a later CASC |
| 2019 | [NUM736+4](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/NUM/NUM736+4.p)* | NUM | Grundlagen problem satz42 | 2020: 1/16; 2021: 3/17; 2024: 3/14; 2025: 4/15 | 2020 | solved in a later CASC |
| 2019 | [NUM781+4](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/NUM/NUM781+4.p)* | NUM | Grundlagen problem satz79 | 2020: 0/16; 2023: 2/13; 2024: 2/14 | 2023 | solved in a later CASC |
| 2019 | [NUN074+2](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/NUN/NUN074+2.p)* | NUN | Robinson arithmetic: Primes exist | 2020: 0/16; 2021: 0/17; 2023: 0/13 | – | never solved in a later CASC |
| 2019 | [SWW249+1](https://seetptp.tptp.org/file/TPTPWorld/TPTP/Problems/SWW/SWW249+1.p) | SWW | Fundamental Theorem of Algebra 438050, 1000 axioms selected | 2021: 2/17 | 2021 | solved in a later CASC |

## Files

- `casc_fof_2020_2026_all_results.csv` — every problem in every year: E result, all Vampire results, best Vampire, systems solved, TPTP header fields.
- `e_failures_2020_2026.csv` — every E failure, who solved it, and how often E failed that problem.
- `e_slower_than_vampire_2020_2026.csv` — significant and moderate slowdowns with ratios.
- `hard_problems_2020_2026.csv` — primary and secondary hard-problem lists with later history and first solvers.
- `per_year_summary_2020_2026.csv` — the table in section 1.
- `casc_fof_long_2020_2026.csv` — the raw extract: one row per year, problem and system, with the cell exactly as shown on the page.

Sources: CASC results pages — [CASC-J10](https://tptp.org/CASC/J10/WWWFiles/Results.html#FOFProblems), [CASC-28](https://tptp.org/CASC/28/WWWFiles/Results.html#FOFProblems), [CASC-J11](https://tptp.org/CASC/J11/WWWFiles/Results.html#FOFProblems), [CASC-29](https://tptp.org/CASC/29/WWWFiles/Results.html#FOFProblems), [CASC-J12](https://tptp.org/CASC/J12/WWWFiles/Results.html#FOFProblems), [CASC-30](https://tptp.org/CASC/30/WWWFiles/Results.html#FOFProblems), [CASC-J13](https://tptp.org/CASC/J13/WWWFiles/Results.html#FOFProblems); 2016–2019 lookback: [CASC-J8](https://tptp.org/CASC/J8/WWWFiles/Results.html), [CASC-26](https://tptp.org/CASC/26/WWWFiles/Results.html), [CASC-J9](https://tptp.org/CASC/J9/WWWFiles/Results.html), [CASC-27](https://tptp.org/CASC/27/WWWFiles/Results.html); [TPTP v9.3.1 distribution](https://tptp.org/TPTP/Distribution/); [TPTP technical report (domains)](https://tptp.org/UserDocs/ProblemLibraryManual/TPTPTR.shtml).
