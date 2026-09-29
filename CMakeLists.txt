cmake_minimum_required(VERSION 3.16)
project(E VERSION 3.5 LANGUAGES C)

# Replaces the recursive Makefiles (Makefile, Makefile.vars, */Makefile, configure).
# Out-of-tree build:   cmake --preset dev && cmake --build --preset dev
# See README.md ("Building with CMake") and CMakePresets.json.

# ---------------------------------------------------------------- options --
option(E_ENABLE_HO        "Build the higher-order version (binary: eprover-ho)" OFF)
option(E_UNIX_COMMENTS    "Use # instead of % as comment sign in the output"    OFF)
option(E_ASSERTIONS       "Keep assertions (off: -DNDEBUG -DFAST_EXIT)"         ON)
option(E_MEMORY_DEBUG     "Enable -DCLB_MEMORY_DEBUG (needs assertions)"        ON)
option(E_DETERMINISTIC_MEMORY "Serve E's small objects from a private arena so that the search does not depend on malloc's address layout" ON)
option(E_BUILD_EXTRA_APPS "Also build SIMPLE_APPS and EXTERNAL programs"        ON)
option(E_BUILD_TESTS      "Register the regression suite with ctest"            ON)
set(E_SANITIZE "" CACHE STRING "Sanitizers, e.g. address,undefined")
set(E_OPT_FLAGS "-O3;-g;-fno-common;-fomit-frame-pointer" CACHE STRING
    "Optimisation/debug flags (used instead of CMAKE_BUILD_TYPE, as in the old Makefile.vars)")

# The old build did not use CMAKE_BUILD_TYPE; neither do we.
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS ON)                       # -std=gnu99
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)            # for clangd
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

add_compile_options(-Wall ${E_OPT_FLAGS})
add_link_options(${E_OPT_FLAGS})

add_compile_definitions(
  STACK_SIZE=32768 CLAUSE_PERM_IDENT MEMORY_RESERVE_PARANOID
  PRINT_SOMEERRORS_STDOUT PRINT_TSTP_STATUS TAGGED_POINTERS)
if(E_ENABLE_HO)
  add_compile_definitions(ENABLE_LFHO)
  set(E_PROVER_NAME eprover-ho)
else()
  set(E_PROVER_NAME eprover)
endif()
if(E_DETERMINISTIC_MEMORY)
  add_compile_definitions(DETERMINISTIC_MEM)
endif()
if(E_UNIX_COMMENTS)
  add_compile_definitions(UNIX_COMMENTS)
endif()
if(E_ASSERTIONS)
  if(E_MEMORY_DEBUG)
    add_compile_definitions(CLB_MEMORY_DEBUG)
  endif()
else()
  add_compile_definitions(NDEBUG FAST_EXIT)
endif()
if(E_SANITIZE)
  add_compile_options(-fsanitize=${E_SANITIZE} -fno-omit-frame-pointer)
  add_link_options(-fsanitize=${E_SANITIZE})
  if(E_SANITIZE MATCHES "undefined")
    add_compile_options(-fno-sanitize-recover=undefined)
  endif()
endif()

find_library(MATH_LIB m)

# E's search depends (through pointer-ordered trees) on the memory layout of
# the binary: even a slightly different size of the string table changes
# heap addresses and hence, occasionally, the search. The old Makefiles compiled
# in each source directory, so __FILE__ (used by assert()) was the bare file
# name. Keep that, independent of source location, so builds stay comparable.
add_compile_options(-Wno-builtin-macro-redefined)
function(e_pin_file_macro)
  foreach(f IN LISTS ARGN)
    get_filename_component(n ${f} NAME)
    set_property(SOURCE ${f} APPEND PROPERTY COMPILE_DEFINITIONS "__FILE__=\"${n}\"")
  endforeach()
endfunction()

# -------------------------------------------------------------- libraries --
# One static library per directory src/<name>, with the target name in upper
# case as before (BASICS, TERMS, ... -> libBASICS.a). All *.c files of the
# directory are used except the listed dead ones.
function(e_library name)
  cmake_parse_arguments(A "" "" "EXCLUDE" ${ARGN})
  string(TOLOWER ${name} dir)
  file(GLOB srcs CONFIGURE_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/src/${dir}/*.c)
  foreach(x IN LISTS A_EXCLUDE)
    list(REMOVE_ITEM srcs ${CMAKE_CURRENT_SOURCE_DIR}/src/${dir}/${x}.c)
  endforeach()
  add_library(${name} STATIC ${srcs})
  e_pin_file_macro(${srcs})
  set_target_properties(${name} PROPERTIES OUTPUT_NAME ${name})
  target_include_directories(${name} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/src/${dir})
endfunction()

# Headers are included by bare name across directories (formerly via the
# include/ symlink farm), so every directory is on every target's include path.
set(E_LIBRARIES basics inout terms orderings clauses propositional learn pcl2
                heuristics control)
set(PICOSAT_DIR ${CMAKE_CURRENT_SOURCE_DIR}/third_party/picosat-965)
include_directories(${PICOSAT_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/apps)
foreach(d IN LISTS E_LIBRARIES)
  include_directories(${CMAKE_CURRENT_SOURCE_DIR}/src/${d})
endforeach()

e_library(BASICS     EXCLUDE clb_newmem)           # USE_NEWMEM experiment
e_library(INOUT)
e_library(TERMS      EXCLUDE cte_simplesorts)
e_library(ORDERINGS  EXCLUDE cto_lpo_debug)
e_library(CLAUSES)
e_library(PROPOSITIONAL)
e_library(LEARN)
e_library(PCL2)
e_library(HEURISTICS EXCLUDE che_normsubst)
e_library(CONTROL)

# PicoSAT (vendored): the old build ran its own configure.sh/makefile.
file(READ ${PICOSAT_DIR}/VERSION PICOSAT_VERSION)
string(STRIP "${PICOSAT_VERSION}" PICOSAT_VERSION)
set(PICOSAT_CFLAGS "-DTRACE -Wall -Wextra -Wno-unused-but-set-variable -DNDEBUG -O3")
file(WRITE ${CMAKE_BINARY_DIR}/picosat_config/config.h
  "#define PICOSAT_CC \"${CMAKE_C_COMPILER}\"\n"
  "#define PICOSAT_CFLAGS \"${PICOSAT_CFLAGS}\"\n"
  "#define PICOSAT_VERSION \"${PICOSAT_VERSION}\"\n")
add_library(CONTRIB STATIC ${PICOSAT_DIR}/picosat.c ${PICOSAT_DIR}/version.c)
target_include_directories(CONTRIB PRIVATE ${CMAKE_BINARY_DIR}/picosat_config)
target_include_directories(CONTRIB PUBLIC ${PICOSAT_DIR})
target_compile_definitions(CONTRIB PRIVATE TRACE NDEBUG)
target_compile_options(CONTRIB PRIVATE -Wextra -Wno-unused-but-set-variable -O3)
add_executable(picosat ${PICOSAT_DIR}/app.c ${PICOSAT_DIR}/main.c)
target_link_libraries(picosat CONTRIB)
target_compile_definitions(picosat PRIVATE NDEBUG)
target_include_directories(picosat PRIVATE ${CMAKE_BINARY_DIR}/picosat_config)

# --------------------------------------------------------------- programs --
# e_program(<binary> <source dir> <libs in link order...>)
# Link sets are copied from the old PROVER/Makefile (sources are in apps/).
function(e_program bin dir)
  add_executable(${bin} ${CMAKE_CURRENT_SOURCE_DIR}/${dir}/${ARGV2})
  e_pin_file_macro(${CMAKE_CURRENT_SOURCE_DIR}/${dir}/${ARGV2})
  list(SUBLIST ARGV 3 -1 libs)
  target_link_libraries(${bin} ${libs} ${MATH_LIB})
  install(TARGETS ${bin} RUNTIME DESTINATION bin)
endfunction()

set(CORE CLAUSES ORDERINGS TERMS INOUT BASICS CONTRIB)
e_program(${E_PROVER_NAME} apps eprover.c CONTROL HEURISTICS LEARN ${CORE})
foreach(p e_ltb_runner e_stratpar e_deduction_server e_axfilter e_client classify_problem)
  e_program(${p} apps ${p}.c CONTROL HEURISTICS ${CORE})
endforeach()
e_program(e_server apps e_server.c     CONTROL HEURISTICS CLAUSES ORDERINGS TERMS INOUT BASICS)
e_program(epatternize apps epatternize.c  CONTROL HEURISTICS LEARN ${CORE})
e_program(eground apps eground.c      HEURISTICS ${CORE})
e_program(enormalizer apps enormalizer.c  HEURISTICS ${CORE})
e_program(edpll apps edpll.c        PROPOSITIONAL ${CORE})
e_program(direct_examples apps direct_examples.c PCL2 ${CORE})
e_program(checkproof apps checkproof.c   PCL2 ${CORE})
foreach(p epclanalyse epcllemma epclextract)
  e_program(${p} apps ${p}.c PCL2 HEURISTICS ${CORE})
endforeach()
foreach(p ekb_create ekb_insert ekb_delete)
  e_program(${p} apps ${p}.c LEARN ${CORE})
endforeach()
e_program(ekb_ginsert apps ekb_ginsert.c  PCL2 LEARN ${CORE})
install(TARGETS picosat RUNTIME DESTINATION bin)

if(E_BUILD_EXTRA_APPS)
  e_program(term2dag        apps/simple term2dag.c TERMS CLAUSES ORDERINGS TERMS INOUT BASICS)
  e_program(ex_commandline  apps/simple ex_commandline.c INOUT BASICS)
  add_executable(CSSCPA_filter apps/external/CSSCPA_filter.c apps/external/cex_csscpa.c)
  e_pin_file_macro(${CMAKE_CURRENT_SOURCE_DIR}/apps/external/CSSCPA_filter.c
                   ${CMAKE_CURRENT_SOURCE_DIR}/apps/external/cex_csscpa.c)
  target_include_directories(CSSCPA_filter PRIVATE apps/external)
  target_link_libraries(CSSCPA_filter ${CORE} ${MATH_LIB})
endif()

# ------------------------------------------------------------------ tests --
if(E_BUILD_TESTS)
  enable_testing()
  find_package(Python3 COMPONENTS Interpreter)
  if(Python3_FOUND)
    add_test(NAME regression
             COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/tests/regression/run.py
                     --binary $<TARGET_FILE:${E_PROVER_NAME}>)
    add_test(NAME determinism
             COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/tests/regression/determinism.py
                     --binary $<TARGET_FILE:${E_PROVER_NAME}>)
  endif()
endif()

# Man pages are generated with help2man from the binaries (not checked in).
if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/docs/man)
  install(DIRECTORY docs/man/ DESTINATION share/man/man1 FILES_MATCHING PATTERN "*.1")
endif()

# Manual (replaces docs/Makefile): cmake --build <dir> --target docs
find_program(PDFLATEX pdflatex)
if(PDFLATEX)
  add_custom_target(docs
    COMMAND ${PDFLATEX} -interaction=nonstopmode eprover.tex
    COMMAND ${PDFLATEX} -interaction=nonstopmode eprover.tex
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/docs
    COMMENT "Building docs/eprover.pdf")
endif()
