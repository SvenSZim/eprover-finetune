**NOTE**: The CASC ReadMe file with information for the CADE ATP
System Competition is in `docs/Readme`.
**NOTE**: The ultimate source is now README.md. Don't edit the plain
README!


Short Installation Instructions for the Impatient
=================================================

E is built with CMake (>= 3.16) and a C compiler; nothing else is needed.

```sh
  cmake --preset dev                  # configure into build/dev
  cmake --build --preset dev -j       # compile everything
  build/dev/bin/eprover -h | more
```

Install the executables (and the PicoSAT binary) somewhere:

```sh
  cmake --install build/dev --prefix /path/to/PREFIX    # binaries in PREFIX/bin
```

Read the rest of this file and the fine (if incomplete) manual if
anything fails. There should be a copy of the manual in
`docs/eprover.pdf`.

E 3.2 supports (monomorphic) higher-order logic. To build a binary
that supports higher-order reasoning, use the `ho` preset (the binary
is called `eprover-ho`):

```sh
  cmake --preset ho && cmake --build --preset ho -j
  build/ho/bin/eprover-ho -h | more
```

Other presets: `fast` (assertions off, as the old `make default_config`) and
`asan` (AddressSanitizer + UBSan). Individual options (`E_ENABLE_HO`,
`E_UNIX_COMMENTS`, `E_ASSERTIONS`, `E_MEMORY_DEBUG`, `E_SANITIZE`,
`E_OPT_FLAGS`, ...) are documented at the top of `CMakeLists.txt` and can be
set with `-D`, e.g. `cmake --preset dev -DE_UNIX_COMMENTS=ON`.

Code style: `tools/format.sh` formats the sources with the pinned clang-format
(`pip install clang-format==23.1.1`); CI runs `tools/format.sh --check`. To make
`git blame` skip the mechanical formatting commits:
`git config blame.ignoreRevsFile .git-blame-ignore-revs`.

The build writes `compile_commands.json` to the build directory; `.clangd`
points clangd at `build/dev`. Run the regression tests with `ctest --preset dev`.


The recommended command for running E on the file problem.p is

```
  eprover --auto --proof-object problem.p
```

If you want to try the usually stronger strategy scheduling mode
(particularly recommended for higher-order problems, use

```
  eprover --auto-schedule --proof-object problem.p
```

To use more than one CPU, use something like
```
  eprover --auto-schedule=8 --proof-object problem.p
```

Replace `eprover` by `eprover-ho` for the higher-order-enabled
version.
You can add a time limit of 300 seconds with the option
`--cpu-limit=300` and a memory limit of 2 GB with `--memory-limit=2048`
for all "automatic" modes. You can reduce output with `-s` (or
`--silent`). As of version 1.9.1, E will try to auto-detect the input
format and adjust the output format accordingly. You can still force
input and output formats via commandline options.



The Equational Theorem Prover E
===============================

This is the README file for version 3.5 "Countess Grey" of the E
equational theorem prover. This version of E is free software, see the
file COPYING for details about the license and the fact that THERE IS
NO WARRANTY!


What is E?
----------

E is an equational theorem prover. That means it is a program that you
can stuff a mathematical specification (in many-sorted first-order
logic with equality or in polymorphic higher-order logic) and a
hypothesisconjecture into, and which will then run forever, using up
all of your machines resources. Very occasionally it will find a proof
for the conjecture and tell you so ;-).

E has been created and is currently maintained by Stephan Schulz,
<schulz@eprover.org>, now with the help of several contributors (see
`docs/CONTRIBUTORS`). It is developed and distributed under the GNU
General Public License.

The E homepage can be found at <https://www.eprover.org>


Installation
------------

E can be installed anywhere in the file system, either by a normal
user or by the system administrator. By default, the prover will still
be compiled as a version that supports first-order logic only.

To install the package, unpack the distribution (if you are reading
this, you probably already did):

```sh
   gunzip -c E.tgz|tar -xvf -
```

or

```sh
   (g)tar -xzf E.tgz
```
(if you have GNU tar)

This should create a directory named E. Then:

```sh
   cd E
   cmake --preset dev
   cmake --build --preset dev -j
```

builds the libraries and all included programs in `build/dev`; run them from
there (`build/dev/bin/eprover`) or install them into a prefix:

```sh
   cmake --install build/dev --prefix PREFIX
```

You need write permission in PREFIX, so if you install E outside your own home
directory, you may need to become root or use sudo.

Changed options are picked up on the next `cmake` run; to start from scratch,
delete the build directory.

To translate the LaTeX documentation (requires LaTeX2e, pdflatex, and the
packages theorem, amssymb and epsfig, which are included in most current LaTeX
distributions), run

```sh
   cmake --build build/dev --target docs
```

The manual should also be included as a pre-compiled PDF. For an unusual
compiler or operating system, pass `-DCMAKE_C_COMPILER=...` and
`-DE_OPT_FLAGS=...`. If you have any problems, look into `docs/PORTING`.

After building, try

```sh
   build/dev/bin/eprover tests/problems/TPTP/BOO006-1.p
```

to see the prover in action. `build/dev/bin/eprover -h` gives you some
information and a list of options.

For impatient people who do not want to read anything:

```sh
   eprover --auto --memory-limit=<80%_of_your_main_memory> <problem-file>
```

should give a reasonable performance on a large class of problems
(unless your main memory is really small).

The auto mode will perform a heuristic pruning of the axiom set which
may result in incompleteness for very large problems (many thousands
of axioms). If you need completeness, use

```sh
  eprover --satauto --memory-limit=<80%_of_your_main_memory> <problem-file>
```

In general, different proof problems are easy for different
strategies. If you run

```sh
  eprover --auto-schedule --memory-limit=<80%_of_your_main_memory> <problem-file>
```

or

```sh
  eprover --satauto-schedule --memory-limit=<80%_of_your_main_memory> <problem-file>
```

the prover will try a series of strategies on the problem. It assumes
a 300 second run time - if you impose a different one externally, it
is important to let E know via the `--cpu-limit=XXX` option so that it
can adjust the schedule. You can also enable usage of multiple cores
with the variant `--auto-schedule=n` (where `n` is the number of
cores), or `--auto-schedule=Auto` to use all available cores.

One of the features of E is the ability to produce semi-readable
proofs. To use this, type

```sh
  eprover --proof-object <other-stuff>
```

By default, E will now automatically detect the input format (LOP,
TPTP-2 or TPTP-3), and will select the matching output format (PCL2
for LOP and TPTP-2 inputs, TPTP-3 for TPTP-3 inputs).

You can check the proof objects in PCL format for correctness using
the tool checkproof in the same directory. "checkproof -h" should give
you all necessary information. Note that checkproof cannot yet deal
with the full first order part, and will skip anything not
clausal. Also, support for independent provers in checkproof can be
subject to bit-rot, as other systems and interfaces change.



Bug reports and questions
=========================

We welcome bug reports and even reasonable questions. If the prover
behaves in an unexpected way, please include the following
information:

- What did you observe?
- What did you expect?
- The output of `eprover --version`
- The full commandline that lead to the unexpected behaviour
- The input file(s) that lead to the unexpected behaviour

Most bug reports should be send to <schulz@eprover.org>. Bug reports
with respect to the HO-version should also be send to
<jasmin.blanchette@gmail.com>. Please remember that this is an unpaid
volunteer service ;-).
