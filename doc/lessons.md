# Base Representations 

Objective: Discuss numerical representations and how numbers are stored in C. 

## Decimal and Binary Systems

In school, we are taught to represent numbers and do math using
the decimal (base-10) system. In the decimal system each digit can be one of 
ten values, i.e. {0,1,2,3,4,5,6,7,8,9}. Contrary to this, computers generally 
store and operate on data in binary (base-2). In binary there are only 
two states {0,1}; when used in logical operations, **0** is usually 
defined as false with any nonzero value true.

## Place-Value Notation (Decimal)

To represent multi-digit numbers, we use place-value notation. Each
base-10 number can be expanded as so,

    base-10(127) = 100 + 20 + 7 = 1 * 10^2 + 2 * 10^1 + 7 * 10^0

Notice that each digit in the number above is the coefficient of
10^*i* where *i* is the place of the digit with *i* = **0** for the 
ones (10^0) place, *i*= 1 for the tens (10^1) place, *i* = 2 for the 
hundreds (10^2) place, etc. The value of *i* may also be negative, 
which we will discuss later on.

## Place-Value Notation (Binary)

Similarly, in binary we may represent numbers other than 0 and 1
using place-value notation. Observe that,

    base-10(127) = 64 + 32 + 16 + 8 + 4 + 2 + 1
                 = 1 * 2^7 + 1 * 2^6 + 1 * 2^5 + 1 * 2^4 
                   + 1 * 2^3 + 1 * 2^2 + 1 * 2^1 + 1 * 2^0
                 = base-2(1111111)

## Binary in Computing

In reference to a binary number, we generally call a single digit a **bit** 
with 8 consecutive bits to a **byte**. 

In the C programming language, there exist many different data types to store the value 
of numbers. Numbers with no fractional component are generally 
stored as integers (char/short/int/long), while numbers with or without
fractional components (real numbers) are can be as floating point values 
(float/double). In the next sections we will delve deeper into C's 
integer and real number storage, starting with integers. 


# Integers in C

Objective: Discuss what an integer is and how they are stored in C. 

## Definition of Integer

An integer is defined as a number that can be written without a 
fractional component, i.e. the positive whole numbers {1,2,3,...}, 
the negative whole numbers  {...,-3,-2,-1}, and zero (**0**). In C,
integers can be both unsigned and signed. Unsigned integers can
represent zero (**0**) and the positive whole numbers, while signed
integers can zero and both the positive and negative whole numbers.

## Physical Storage and Two's Complement

<INSERT_WORDS>

## Storage Size and Ranges

The maximum/minimum value that an integer can have depends on the
data type of the integer. The integer data types are as follow in 
order of ascending size: char, short, int, long, long long. Again,
each of these data types may be unsigned or signed with signed
generally being the implicit representation, e.g. "short" vs. 
"unsigned short" and "int" vs. "unsigned int". The table below 
gives a detailed look at each data type and its properties. 

| Data Type        | Size (in bytes)\*| Range                                        |
| ---------------- |:----------------:|:-------------------------------------------- |
| char             | 1                | \*\*                                         |
| signed char      | 1                | [-128, 127]                                  |
| unsigned char    | 1                | [0, 255]                                     |
| short            | 2                | [-32767, 32767]                              |
| unsigned short   | 2                | [0, 65535]                                   |
| int              | 2 or 4           | [-32767, 32767] or [-2147483648, 2147483648] |
| unsigned int     | 2 or 4           | [0, 65535] or [0, 4294967295]                |
| long             | 8                | [-9223372036854775808 ,9223372036854775807]  |
| unsigned long    | 8                | [0, 18446744073709551615]                    |

*\*Note: the actual size of the data type varies on implementation, but <br>
the data type is guaranteed to be >= size and contain the range given.* <br>
*\*\*Note: The signedness of char is implementation specific.*

# Real Numbers in C

Objective: Discuss real numbers, ways to represent them, and how they are stored in C. 

## Definition of a Real Number
Now that we can represent integers, we'll take a look at the interesting problems
with representing non-integer real numbers. Real numbers include integers, rationals (1/2), 
and irrationals (√2). Storing these values can be a challenge, especially for repeating rationals 
like 1/3 = 0.33333... or irrationals, which contain an infinite sequence of non-repeating values (π).
How can we store numbers that can be extremely large, like 2^200, and also store numbers
that can have an exceedingly long sequence of digits (1/3)? Before we explore how
computers tackle this, we should take a look at a way scientists commonly represent 
these values.

## Scientific Notation
Scientific-Notation is a way to represent very large and small numbers while making the significant digits
clearly recognizable. Significant digits are defined as all digits except: 
-   All [leading zeros](https://en.wikipedia.org/wiki/Leading_zeros "Leading zeros"). For example, "013" has 2 significant figures: 1 and 3
-   [Trailing zeros](https://en.wikipedia.org/wiki/Trailing_zeros "Trailing zeros") when they are merely placeholders to indicate the scale of the number (exact rules are explained at [identifying significant figures](https://en.wikipedia.org/wiki/Significant_figures#Identifying_significant_figures))
-   [Spurious](https://en.wiktionary.org/wiki/spurious "wikt:spurious") digits introduced, for example, by calculations carried out to greater precision than that of the original data, or measurements reported to a greater precision than the equipment supports.

Using Scientific-Notation we represent a number like so,
>    *m* \* 10^*n*

Where *m* (the mantissa) is the sequence of significant digits of the number and *n* is the 
number of decimal places to the left or right the mantissa begins. The following are a list of 
base-10 numbers expressed in Scientific-Notation:
```
1230000 = 1.23 * 10^6
0.00007 = 7.00 * 10^(-5)
1.50700 = 1.507 * 10^0
```

Floating-point representation is very similar to Scientific-Notation.
In computing, floating-point arithmetic is defined as arithmetic using formulaic representation 
of real numbers as an approximation to support a trade-off between range and 
precision [(more here)](https://en.wikipedia.org/wiki/Floating-point_arithmetic). 

## Range vs. Precision
**Range** refers to the set of values that can be represented by the system, we typically think of 
this as an interval from a smallest number to a largest number, e.g. [-100, 100]. 

**Precision** is the degree of accuracy of a representation, typically in number of digits.
Precision goes hand and hand with the concept of significant digits, the more significant 
digits we use to approximate a number, the more precise our approximation. For example,
We may say π ≈ 3, which is true although we may be more *precise* and say π ≈ 3.1415. On the
other hand π ≈ 3.141500000 is no more precise than π ≈ 3.1415 or π ≈ 0003.1415.

As stated above, floating-point arithmetic standards try to maximize both of these properties
given a finite number of bits to represent a single number. One such standard is **IEEE-754**,
which is perhaps the most common computing standard for storing floating point values.

## Physical Storage and IEEE Standards

**IEEE-754** floats (4 bytes) or doubles (8 bytes) are composed of three parts: 
a sign bit to represent the whether the number is positive or negative, 
an exponent giving its order of magnitude, and a mantissa (the coefficient) 
which contains the significant digits of the number. An IEEE-754 float has a
binary representation as follows (each character is a **bit**):
```
SEEEEEEE EMMMMMMM MMMMMMMM MMMMMMMM

S = Sign
E = Exponent
M = Mantissa
```

## Storage Size and Ranges

<INSERT_WORDS>

## Equality

## Overflow (INF/NAN)

## Loss of Significance
