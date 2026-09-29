/*-----------------------------------------------------------------------

File  : cte_termcellstore.h

Author: Stephan Schulz

Contents

  Abstract interface for storing term cells, implemented by a
  combination of a hashed array and term cell trees. Use
  (term->f_code^term->args[1])&TERM_STORE_HASH_MASK  as
  hash if args != NULL, otherwise use
  term->f_code&TERM_STORE_HASH_MASK.

  Copyright 1998, 1999 by the author.
  This code is released under the GNU General Public Licence and
  the GNU Lesser General Public License.
  See the file COPYING in the main E directory for details..
  Run "eprover -h" for contact information.

Changes

<1> Mon Oct  5 01:09:50 MEST 1998
    New
<2> Thu Apr 11 10:08:26 CEST 2002
    Support for mark-and-sweep garbage collection (the sweep pass) for
    term cells

-----------------------------------------------------------------------*/

#ifndef CTE_TERMCELLSTORE

#define CTE_TERMCELLSTORE

#include <cte_termtrees.h>

/*---------------------------------------------------------------------*/
/*                    Data type declarations                           */
/*---------------------------------------------------------------------*/

#define TERM_STORE_HASH_SIZE (8192 * 4)
#define TERM_STORE_HASH_MASK (TERM_STORE_HASH_SIZE - 1)

typedef struct termcellstore
{
   long entries;
   long arg_count;
   Term_p store[TERM_STORE_HASH_SIZE];
} TermCellStoreCell, *TermCellStore_p;


/*---------------------------------------------------------------------*/
/*                Exported Functions and Variables                     */
/*---------------------------------------------------------------------*/

/* The hash of a term is computed from f_code and the deterministic ids of
   the (already shared) arguments -- NOT from their addresses. Hashing
   addresses made the bucket order (and thereby every traversal of the term
   store) depend on the memory layout of the binary and on malloc's history,
   so the search could differ between otherwise identical builds and even
   between runs with different problem file names. Variables carry their
   f_code in entry_no, see TBCellIdent(). */
#define TCS_ARG_ID(term) ((unsigned long)((term)->entry_no))
#define TCS_MIX(id) (((id) * 0x9E3779B97F4A7C15UL) >> 40)

#define tcs_arity0hash(term) ((unsigned long)(term)->f_code)
#define tcs_arity1hash(term)                                                   \
   (tcs_arity0hash(term) ^ TCS_MIX(TCS_ARG_ID((term)->args[0])))
#define tcs_aritynhash(term)                                                   \
   (tcs_arity1hash(term) ^ (TCS_MIX(TCS_ARG_ID((term)->args[1])) << 1))

#define TermCellHash(term)                                                     \
   ((((term)->arity == 0) ? tcs_arity0hash(term)                               \
                          : (((term)->arity == 1) ? tcs_arity1hash(term)       \
                                                  : tcs_aritynhash(term))) &   \
    TERM_STORE_HASH_MASK)

void TermCellStoreInit(TermCellStore_p store);
void TermCellStoreExit(TermCellStore_p store);

Term_p TermCellStoreFind(TermCellStore_p store, Term_p term);
Term_p TermCellStoreInsert(TermCellStore_p store, Term_p term);
Term_p TermCellStoreExtract(TermCellStore_p store, Term_p term);
bool TermCellStoreDelete(TermCellStore_p store, Term_p term);

void TermCellStoreSetProp(TermCellStore_p store, TermProperties props);
void TermCellStoreDelProp(TermCellStore_p store, TermProperties props);

#define TermCellStoreNodes(store) ((store)->entries)
long TermCellStoreCountNodes(TermCellStore_p store);

long TermCellStoreGCSweep(TermCellStore_p store, TermProperties gc_state);

void TermCellStorePrintDistrib(FILE* out, TermCellStore_p store);

#endif

/*---------------------------------------------------------------------*/
/*                        End of File                                  */
/*---------------------------------------------------------------------*/



