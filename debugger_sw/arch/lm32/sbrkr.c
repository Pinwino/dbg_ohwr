#include <stdio.h>
#include <stdlib.h>
#include <pp-printf.h>
#define GGC_MIN_HEAPSIZE_DEFAULT 32 



extern unsigned int _HEAP_START;
extern unsigned int _HEAP_END;
extern unsigned int aling;
extern unsigned int _endram;
extern unsigned int _fstack;
caddr_t heap = NULL;



caddr_t _sbrk ( int increment ) {

    caddr_t prevHeap;
    caddr_t nextHeap;

    if (heap == NULL) {
        heap = (caddr_t)&_HEAP_START; 
    }

    prevHeap = heap;

   /*
    * Although it is recommended to return data aligned to a 4 byte boundary,
    *
    * nextHeap = (caddr_t)(((unsigned int)(heap + increment) + aling) & ~aling)
    * 
    * in our case, we don't need to do it
    */

	nextHeap = (caddr_t)((unsigned int)(heap + increment));
	register caddr_t stackPtr asm ("sp");
    if ((((caddr_t)&_HEAP_START < stackPtr) && (nextHeap > stackPtr)) ||
         (nextHeap >= (caddr_t)&_HEAP_END)) {
		return NULL;
    } else {
        heap = nextHeap;
        return (caddr_t) prevHeap;
    }
}
