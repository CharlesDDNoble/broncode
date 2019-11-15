#include <stdio.h>
#include <float.h>

int main(int argc, char **argv)
{   
    // Base
    printf("Base for all floating-point types (float, double and long double): %d\n\n",FLT_RADIX);
    
    // Mantissa Digits
    printf("The number of digits (bits if base-2) that form the significand of floats: %d\n",FLT_MANT_DIG);
    printf("The number of digits (bits if base-2) that form the significand of doubles: %d\n",DBL_MANT_DIG);
    printf("The number of digits (bits if base-2) that form the significand of long doubles: %d\n\n",LDBL_MANT_DIG);
    
    // Decimal Digits
    printf("Maximum number of decimal digits that can be rounded to float and back without change: %d\n",FLT_DIG);
    printf("Maximum number of decimal digits that can be rounded to double and back without change: %d\n",DBL_DIG);
    printf("Maximum number of decimal digits that can be rounded to long double and back without change: %d\n\n",LDBL_DIG);

    // Minimum Exponent
    printf("Minimum negative integer value for the exponent that generates a normalized float number: %d\n",FLT_MIN_EXP);
    printf("Minimum negative integer value for the exponent that generates a normalized double number: %d\n",DBL_MIN_EXP);
    printf("Minimum negative integer value for the exponent that generates a normalized long double number: %d\n\n",LDBL_MIN_EXP);

    // Minimum base-10 Exponent
    printf("Minimum negative integer value for the exponent of a base-10 expression that would generate a normalized float number: %d\n",FLT_MIN_10_EXP);
    printf("Minimum negative integer value for the exponent of a base-10 expression that would generate a normalized double number: %d\n",DBL_MIN_10_EXP);
    printf("Minimum negative integer value for the exponent of a base-10 expression that would generate a normalized long double number: %d\n\n",LDBL_MIN_10_EXP);

    // Maximum Exponent
    printf("Maximum negative integer value for the exponent that generates a normalized float number: %d\n",FLT_MAX_EXP);
    printf("Maximum negative integer value for the exponent that generates a normalized double number: %d\n",DBL_MAX_EXP);
    printf("Maximum negative integer value for the exponent that generates a normalized long double number: %d\n\n",LDBL_MAX_EXP);

    // Maximum base-10 Exponent
    printf("Maximum integer value for the exponent of a base-10 expression that would generate a normalized float number: %d\n",FLT_MAX_10_EXP);
    printf("Maximum integer value for the exponent of a base-10 expression that would generate a normalized double number: %d\n",DBL_MAX_10_EXP);
    printf("Maximum integer value for the exponent of a base-10 expression that would generate a normalized long double number: %d\n\n",LDBL_MAX_10_EXP);

    // Maximum
    printf("Maximum finite representable float number: %e\n",FLT_MAX);
    printf("Maximum finite representable double number: %e\n",DBL_MAX);
    printf("Maximum finite representable long double number: %Le\n\n",LDBL_MAX);

    // Minimum 0
    printf("Minimum finite representable positive float number: %e\n",FLT_MIN);
    printf("Minimum finite representable positive double number: %e\n",DBL_MIN);
    printf("Minimum finite representable positive long double number: %Le\n\n",LDBL_MIN);

    // Epsilon
    printf("Difference between 1 and the least value greater than 1 that is representable for float: %e\n",FLT_EPSILON);
    printf("Difference between 1 and the least value greater than 1 that is representable for double: %e\n",DBL_EPSILON);
    printf("Difference between 1 and the least value greater than 1 that is representable for long double: %Le\n\n",LDBL_EPSILON);

    return 0;
}
