#include <stdio.h>
#include <limits.h>

int main(int argc, char **argv)
{   
    // Chars
    printf("Number of bits in a char object (byte): %d\n",CHAR_BIT);
    printf("Minimum value for an object of type signed char: %d\n",SCHAR_MIN);
    printf("Maximum value for an object of type signed char: %d\n",SCHAR_MAX);
    printf("Maximum value for an object of type unsigned char: %u\n",UCHAR_MAX);
    printf("Minimum value for an object of type char: %d\n",CHAR_MIN);
    printf("Maximum value for an object of type char: %d\n\n",CHAR_MAX);
    
    // Shorts
    printf("Size of short: %lu\n",sizeof(short));
    printf("Minimum value for an object of type short: %d\n",SHRT_MIN);
    printf("Maximum value for an object of type short: %u\n",SHRT_MAX);
    printf("Maximum value for an object of type unsigned short: %u\n\n",USHRT_MAX);
    
    // Ints
    printf("Size of int: %lu\n",sizeof(int));
    printf("Minimum value for an object of type int: %d\n",INT_MIN);
    printf("Maximum value for an object of type int: %d\n",INT_MAX);
    printf("Maximum value for an object of type unsigned int: %u\n\n",UINT_MAX);
    
    // Longs
    printf("Size of long: %lu\n",sizeof(long));
    printf("Minimum value for an object of type long int: %ld\n",LONG_MIN);
    printf("Maximum value for an object of type long int: %ld\n",LONG_MAX);
    printf("Maximum value for an object of type unsigned long int: %lu\n\n",ULONG_MAX);
    
    // Long Longs
    printf("Size of long long: %lu\n",sizeof(long long));
    printf("Minimum value for an object of type long long int: %lld\n",LLONG_MIN);
    printf("Maximum value for an object of type long long int: %lld\n",LLONG_MAX);
    printf("Maximum value for an object of type unsigned long long int: %llu\n\n",ULLONG_MAX);
    return 0;
}
