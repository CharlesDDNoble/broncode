#include <stdio.h>
#include <stdlib.h>

// Write each digit of value in the new base into digits[]
// ordered from least significant to most significant. 
// --> Returns the number of digits in the new base
int write_digits(int value, int base, int* digits) {
    // value = digits[0]*base^0 + digits[1]*base^1 + ... + digits[i]*base^i
    int i = 0;

    while (value > 0) {
        // Get the coefficent of the least 
        // significant digit in the new base
        digits[i++] = value % base;
        value /= base;
    }
    return i;
}

void print_to_base(int value, int base) {
    // value = digits[0]*base^0 + digits[1]*base^1 + ... + digits[i]*base^i
    int digits[256];
    int i = write_digits(value,base,digits);

    // Pretty formatted output
    printf("base_10(%d) = ",value);
    printf("[");
    while (i-- > 1) {
        printf("%d,", digits[i]);
    }
    printf("%d", digits[0]);
    printf("]");
    printf(" in base_%d\n",base);
}

void print_expansion(int value, int base) {
    int digits[256];
    int i = write_digits(value,base,digits);
    

    // Pretty formatted output
    // Note: digits[] is ordered from least significant
    //       to most significant. 
    printf("base_10(%d) = ",value);
    while (i-- > 1) {
        printf("%d*(%d^%d) + ", digits[i],base,i);
    }
    printf("%d*(%d^%d)\n", digits[0],base,0);
}


int main(int argc,char** argv) {
    int error = 0;
    if (argc != 3) {
        error = -1;
        printf("Usage: ./base_conv <INPUT> <BASE>\n");
    } else {
        int value = atoi(argv[1]);
        int base = atoi(argv[2]);
        print_to_base(value,base);
    }

    return error;
}
