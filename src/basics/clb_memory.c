/*-----------------------------------------------------------------------

  File  : clb_memory.c

  Author: Stephan Schulz

  Memory management. The implemented routines are very simple, because
  they make use of the standard memory management for reorganization.

  Copyright 1998-2017 by the author.
  This code is released under the GNU General Public Licence and
  the GNU Lesser General Public License.
  See the file COPYING in the main E directory for details..
  Run "eprover -h" for contact information.

  Changes

  Created: Thu Aug 14 10:00:35 MET DST 1997

  -----------------------------------------------------------------------*/

#ifdef USE_NEWMEM
#include "clb_newmem.c"
#else

#include "clb_memory.h"


/*-----------------------------------------------------------------------*/
/*                         Globale Variable                              */
/*-----------------------------------------------------------------------*/

/* This global variable is set whenever malloc() failed and triggered
   a free memory reorganization. User programs may examine this
   variable to take certain measures (and may reset it if they think
   that they freed significant amounts of memory). However, this
   is somewhat discouraged - do you really want your program to depend
   in pretty complex ways on uncontrolable features like the amount of
   free memory available to your process? _I_ only used to use it for
   some measurements ;-)  StS */

bool MemIsLow = false;

Mem_p free_mem_list[MEM_ARR_SIZE] = { NULL };

#ifdef CLB_MEMORY_DEBUG
long size_malloc_mem = 0;
long size_malloc_count = 0;
long size_free_mem = 0;
long size_free_count = 0;
long clb_free_count = 0;
long secure_malloc_count = 0;
long secure_malloc_mem = 0;
long secure_realloc_count = 0;
long secure_realloc_m_count = 0;
long secure_realloc_f_count = 0;
#endif


/*---------------------------------------------------------------------*/
/*                         Internal Functions                          */
/*---------------------------------------------------------------------*/


#ifdef CLB_MEMORY_DEBUG

/*-----------------------------------------------------------------------
//
// Function: free_list_size()
//
//   Return the length if the list of MemCells.
//
// Global Variables: -
//
// Side Effects    : -
//
/----------------------------------------------------------------------*/

static long free_list_size(Mem_p list)
{
   long res = 0;
   while(list)
   {
      list = list->next;
      res++;
   }
   return res;
}

#endif


/*-----------------------------------------------------------------------*/
/*                  Exportierte Funktionen                               */
/*-----------------------------------------------------------------------*/


/*-----------------------------------------------------------------------
//
// Function: MemFlushFreeList()
//
//   Returns all memory kept in free_mem_list[] to the operation
//   system. This is useful if a very different memory access pattern
//   is expected (SizeFree() never reorganizes the memory
//   automatically).
//
// Global Variables: free_mem_list[]
//
// Side Effects    : Memory operations
//
/----------------------------------------------------------------------*/

void MemFlushFreeList(void)
{
   int f;
   void* handle;

#ifdef DETERMINISTIC_MEM
   /* The blocks on the free lists live in the private arena and cannot be
      returned to malloc individually; they are reclaimed at process exit. */
   (void)f;
   (void)handle;
   VERBOUT("MemFlushFreeList(): arena memory is not returned\n");
   return;
#endif

   VERBOUT("MemFlushFreeList() called for cleanup or reorganization\n");
   for(f = 0; f < MEM_ARR_SIZE; f++)
   {
      while(free_mem_list[f])
      {
         handle = (void*)free_mem_list[f];
         free_mem_list[f] = free_mem_list[f]->next;
         FREE(handle);
      }
   }
}


#ifdef DETERMINISTIC_MEM

#if defined(__unix__) || defined(__APPLE__)
#include <sys/mman.h>
#include <sys/resource.h>
#define ARENA_HAVE_MMAP 1
#endif

/*-----------------------------------------------------------------------
//
// Function: MemArenaAlloc()
//
//   Return a 16-byte aligned block of size bytes carved out of a
//   private arena (bump allocation, never freed individually; blocks are
//   recycled through free_mem_list[] by SizeFree()).
//
//   Why: E keeps sets of objects in trees ordered by address (PTree), so
//   the search depends on the relative addresses of objects. With
//   malloc those depend on its whole history (freed strings, other
//   libraries, the allocator implementation), on ASLR-independent
//   details such as the placement of large mappings, ... which made
//   results differ between otherwise identical builds and runs. Bump
//   allocation makes the order a function of E's own allocation sequence
//   only.
//
//   The arena is one contiguous address range, reserved up front
//   (untouched pages cost nothing; the size is reduced if a resource
//   limit does not allow it). If that fails, or when it is exhausted,
//   further memory comes in 48 MiB chunks from malloc: still correct, but
//   the order of blocks in different chunks then depends on the system.
//
// Global Variables: arena_*
//
// Side Effects    : Memory operations
//
/----------------------------------------------------------------------*/

#define ARENA_CHUNK_SIZE ((size_t)48 << 20)
#define ARENA_ALIGN 16
#define ARENA_MAX_CHUNKS 8192

static char* arena_base = NULL; /* Contiguous reserved range, or NULL */
static size_t arena_size = 0;
static size_t arena_used = 0;
static bool arena_init_done = false;
static char* arena_cur = NULL; /* Fallback chunks */
static char* arena_end = NULL;
static char* arena_chunks[ARENA_MAX_CHUNKS];
static int arena_chunk_count = 0;

static void arena_reserve(void)
{
   arena_init_done = true;
#ifdef ARENA_HAVE_MMAP
   size_t want = (size_t)1 << 38; /* 256 GiB of address space */
   struct rlimit rl;

   if(getrlimit(RLIMIT_AS, &rl) == 0 && rl.rlim_cur != RLIM_INFINITY)
   {
      /* Do not eat more than half of a limited address space. */
      while(want > (size_t)rl.rlim_cur / 2 && want > ((size_t)256 << 20))
      {
         want >>= 1;
      }
   }
   for(; want >= ((size_t)256 << 20); want >>= 1)
   {
      void* p = mmap(NULL, want, PROT_READ | PROT_WRITE,
                     MAP_PRIVATE | MAP_ANONYMOUS | MAP_NORESERVE, -1, 0);
      if(p != MAP_FAILED)
      {
         arena_base = p;
         arena_size = want;
         return;
      }
   }
#endif
}

void* MemArenaAlloc(size_t size)
{
   void* res;

   size = (size + (ARENA_ALIGN - 1)) & ~(size_t)(ARENA_ALIGN - 1);
   assert(size <= ARENA_CHUNK_SIZE);
   if(UNLIKELY(!arena_init_done))
   {
      arena_reserve();
   }
   if(LIKELY(arena_base && arena_size - arena_used >= size))
   {
      res = arena_base + arena_used;
      arena_used += size;
      return res;
   }
   /* Fallback: chunks from malloc */
   if(arena_cur == NULL || (size_t)(arena_end - arena_cur) < size)
   {
      if(arena_chunk_count == ARENA_MAX_CHUNKS)
      {
         return SecureMalloc(size); /* Out of bookkeeping slots */
      }
      arena_cur = SecureMalloc(ARENA_CHUNK_SIZE);
      arena_end = arena_cur + ARENA_CHUNK_SIZE;
      arena_chunks[arena_chunk_count++] = arena_cur;
   }
   res = arena_cur;
   arena_cur += size;
   return res;
}

/* Is ptr inside the arena? (Only used for debugging assertions.) */

bool MemInArena(const void* ptr)
{
   int i;
   const char* p = ptr;

   if(arena_base && p >= arena_base && p < arena_base + arena_size)
   {
      return true;
   }
   for(i = 0; i < arena_chunk_count; i++)
   {
      if(p >= arena_chunks[i] && p < arena_chunks[i] + ARENA_CHUNK_SIZE)
      {
         return true;
      }
   }
   return false;
}

#endif


/*-----------------------------------------------------------------------
//
// Function: SecureMalloc()
//
//  Returns a pointer to an unused memory block sized size. If
//  possible, a fresh block is allocated, if not, the
//  reorganization of free_mem_list is triggered, if still no memory
//  is available, an error will be produced. If the first malloc
//  fails, MemIsLow will be set.
//
// Global Variables: free_mem_list, MemIsLow
//
// Side Effects    : Memory operations, possibly error
//
/----------------------------------------------------------------------*/

void* SecureMalloc(size_t size)
{
   void* handle;

#ifdef CLB_MEMORY_DEBUG
   secure_malloc_count++;
   secure_malloc_mem += size;
#endif

   handle = (void*)malloc(size);

   if(UNLIKELY(!handle))
   { /* malloc has no memory left  */
      MemIsLow = true;
      MemFlushFreeList(); /* Return own freelist */

      handle = (void*)malloc(size);

      if(!handle)
      { /*  Still nothing...*/
#ifdef PRINT_SOMEERRORS_STDOUT
         SetMemoryLimit(RLIM_INFINITY);
         fprintf(stdout,
                 COMCHAR " Failure: Resource limit exceeded (memory)\n");
         TSTPOUT(stdout, "ResourceOut");
         fflush(stdout);
         PrintRusage(stdout);
#endif
         Error("Out of Memory", OUT_OF_MEMORY);
      }
   }
#ifdef CLB_MEMORY_DEBUG2
   printf("\nBlock %p M: %zd\n", handle, size);
#endif
   return handle;
}

/*-------------------------------------------------------------------------
//
// Function: SecureRealloc()
//
//   Imitates realloc, but reorganizes free_mem_list to get new memory
//   if the block has to be moved and no memory is available. Will
//   terminate with OUT_OF_MEMORY if no memory is found.
//
// Global Variables: -
//
// Side Effect     : Via SecureMalloc()
//
//-----------------------------------------------------------------------*/

void* SecureRealloc(void* ptr, size_t size)
{
   void* handle;

#ifdef CLB_MEMORY_DEBUG
   secure_realloc_count++;
   if(ptr && !size)
   {
      secure_realloc_f_count++;
   }
   else if(!ptr && size)
   {
      secure_realloc_m_count++;
   }
#endif
   /* SunOS realloc() is broken, so here is a stupid workaround...*/

   handle = ptr ? realloc(ptr, size) : malloc(size);
   if(UNLIKELY(!handle && size != 0))
   {
      MemIsLow = true;
      MemFlushFreeList();
      handle = ptr ? realloc(ptr, size) : malloc(size);
      if(!handle)
      { /*  Still nothing...*/
#ifdef PRINT_SOMEERRORS_STDOUT
         SetMemoryLimit(RLIM_INFINITY);
         fprintf(stdout,
                 COMCHAR " Failure: Resource limit exceeded (memory)\n");
         fflush(stdout);
         PrintRusage(stdout);
#endif
         Error("Out of Memory", OUT_OF_MEMORY);
      }
   }
#ifdef CLB_MEMORY_DEBUG2
   if(ptr != handle)
   {
      if(ptr)
      {
         printf("\nBlock %p F:\n", ptr);
      }
      printf("\nBlock %p R: %zd\n", handle, size);
   }
#endif

   return handle;
}

/*-----------------------------------------------------------------------
//
// Function: SecureStrdup()
//
//   Implements the functionality of strdup, but uses SecureMalloc()
/    for the memory handling.
//
// Global Variables: -
//
// Side Effects    : By SecureMalloc()
//
/----------------------------------------------------------------------*/

char* SecureStrdup(const char* source)
{
   char* handle;

   handle = SecureMalloc(strlen(source) + 1);
   strcpy(handle, source);

   return handle;
}

/*-----------------------------------------------------------------------
//
// Function: SecureStrndup()
//
//   Implements the functionality of GNU strndup, but uses
//   SecureMalloc() for the memory handling (creates a NULL-terminated
//   copy of the string or the first n bytes of it).
//
// Global Variables: -
//
// Side Effects    : By SecureMalloc()
//
/----------------------------------------------------------------------*/

char* SecureStrndup(const char* source, size_t n)
{
   char* handle;
   size_t len;

   assert(source);
   assert(n >= 0);

   len = strlen(source);

   if(len > n)
   {
      handle = SecureMalloc(n + 1);
      strncpy(handle, source, n);
      handle[n] = '\0';
   }
   else
   {
      handle = SecureStrdup(source);
   }
   return handle;
}



/*-----------------------------------------------------------------------
//
// Function: IntArrayAlloc()
//
//   Return a pointer to  a freshly allocated, 0-initialized block of
//   longs.
//
// Global Variables: -
//
// Side Effects    : Memory operations
//
/----------------------------------------------------------------------*/

long* IntArrayAlloc(int size)
{
   long* res;
   int i;

   res = SizeMalloc(size * sizeof(long));

   for(i = 0; i < size; i++)
   {
      res[i] = 0;
   }
   return res;
}



#ifdef CLB_MEMORY_DEBUG

/*-----------------------------------------------------------------------
//
// Function: MemDebugPrintStats()
//
//   Print information about allocated and deallocated memory.
//
// Global Variables: size_malloc_mem, size_malloc_count,
//                   size_free_mem, size_free_count
//
// Side Effects    : Output
//
/----------------------------------------------------------------------*/

void MemDebugPrintStats(FILE* out)
{
   fprintf(out,
           "\n" COMCHAR " -------------------------------------------------\n");
   fprintf(out,
           COMCHAR " Total SizeMalloc()ed memory: %ld Bytes (%ld requests)\n",
           size_malloc_mem, size_malloc_count);
   fprintf(out,
           COMCHAR " Total SizeFree()ed   memory: %ld Bytes (%ld requests)\n",
           size_free_mem, size_free_count);
   fprintf(
      out,
      COMCHAR
      " New requests: %6ld (%6ld by SecureMalloc(), %6ld by SecureRealloc())\n",
      secure_malloc_count + secure_realloc_m_count, secure_malloc_count,
      secure_realloc_m_count);
   fprintf(out, COMCHAR " Total SecureMalloc()ed memory: %ld Bytes\n",
           secure_malloc_mem);
   fprintf(
      out,
      COMCHAR
      " Returned:    %6ld (%6ld by FREE(),         %6ld by SecureRealloc())\n",
      clb_free_count + secure_realloc_f_count, clb_free_count,
      secure_realloc_f_count);
   fprintf(
      out,
      COMCHAR
      " SecureRealloc(ptr): %6ld (%6ld Allocs, %6ld Frees, %6ld Reallocs)\n",
      secure_realloc_count, secure_realloc_m_count, secure_realloc_f_count,
      secure_realloc_count - (secure_realloc_m_count + secure_realloc_f_count));
   fprintf(out,
           COMCHAR " -------------------------------------------------\n\n");
}


/*-----------------------------------------------------------------------
//
// Function: MemFreeListPrint()
//
//   Print the size of the free list for each size.
//
// Global Variables: -
//
// Side Effects    : -
//
/----------------------------------------------------------------------*/

void MemFreeListPrint(FILE* out)
{
   long i, sum = 0, count = 0, tmp;

   fprintf(out, COMCHAR " MemFreeListPrint()\n");
   fprintf(out, COMCHAR " ===============================\n");
   for(i = 0; i < MEM_ARR_SIZE; i++)
   {
      tmp = free_list_size(free_mem_list[i]);
      if(tmp)
      {
         fprintf(out, COMCHAR " %4ld: %ld\n", i, tmp);
         sum += tmp * (i);
         count += tmp;
      }
   }
   fprintf(out, COMCHAR " ===============================\n");
   fprintf(out, COMCHAR " %6ld blocks with %ld bytes \n", count, sum);
}


#endif
#endif

/*-----------------------------------------------------------------------*/
/*                       Ende des Files                                  */
/*-----------------------------------------------------------------------*/
