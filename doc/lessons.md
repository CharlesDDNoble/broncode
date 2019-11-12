
# Base Representations 

Objective: Discuss numerical representations and how numbers are stored in C. 

## Decimal and Binary Systems

In school, we are taught to represent numbers and do math using the decimal (base-10) system. In the decimal system each digit can be one of ten values, i.e {0,1,2,3,4,5,6,7,8,9}. Contrary to this, computers generally store and operate on data in binary (base-2). In binary there are only two states {0,1}; when used in logical operations, **0** is usually defined as false with any nonzero value true.

## Place-Value Notation (Decimal)

To represent multi-digit numbers, we use place-value notation. Each base-10 number can be expanded as so,
> base-10(127) = 100 + 20 + 7 = 1 \* 10^2 + 2 \* 10^1 + 7 \* 10^0

From now on, assume that all numbers are given in decimal unless otherwise stated. Notice that each digit in the number above is the coefficient of 10^*i* where *i* is the place of the digit with *i* = **0** for the ones (10^0) place, *i*= 1 for the tens (10^1) place, *i* = 2 for the hundreds (10^2) place, etc. The value of *i* may also be negative,  which we will discuss later on.

## Place-Value Notation (Binary)

Similarly, in binary we may represent numbers other than 0 and 1
using place-value notation. Observe that,
>   127 = 64 + 32 + 16 + 8 + 4 + 2 + 1<br>
>   127 = 1 \* 2^7 + 1 \* 2^6 + 1 \* 2^5 + 1 \* 2^4 + 1 \* 2^3 + 1 \* 2^2 + 1 \* 2^1 + 1 \* 2^0<br>
>   127 = base-2(1111111)<br>

## Binary in Computing

In reference to a binary number, we generally call a single digit a **bit** with 8 consecutive bits to a **byte**. Binary numbers, like decimal numbers, are generally written in order of most signicant digit to least significant digit, i.e. the leftmost bit in a bit string is the coefficent of the greatest exponent while the rightmost bit is the coefficient of the least.

In the C programming language, there exist many different data types to store the value of numbers. Numbers with no fractional component are generally stored as integers (char/short/int/long), while numbers with or without fractional components (real numbers) are can be as floating point values (float/double). In the next sections we will delve deeper into C's integer and real number storage, starting with integers. 


# Integers in C

Objective: Discuss what an integer is and how they are stored in C. 

## Definition of Integer

An integer is defined as a number that can be written without a fractional component, i.e. the positive whole numbers {1,2,3,...}, the negative whole numbers  {...,-3,-2,-1}, and zero (**0**). In C, integers can be both unsigned and signed. Unsigned integers can represent zero (**0**) and the positive whole numbers, while signed integers can zero and both the positive and negative whole numbers.

## Unsigned Integers
In C, if we have an integer variable *i* ≥ **0**, i.e. we expect *i* to always be greater than or equal to **0**, then we may store it as an unsigned integer. Unsigned integers are represented by a string of bits, the length of which depends on the specific data type. 

Let's assume an unsigned integer *u* is stored as a string of 8 bits (1 byte). If *u* = 20, then *u* would be stored like so,
> 0001 0100

Notice that,
> base-2(00010100) = 1\*(16) + 1\*(4)
> base-2(00010100) = 0\*(128) + 0\*(64) + 0\*(32) + 1\*(16) + 0\*(8) + 1\*(4) + 0\*(2) + 0\*(1)
> base-2(00010100) = 0 \* 2^7 + 0 \* 2^6 + 0 \* 2^5  + 1 \* 2^4  + 0 \* 2^3   + 1 \* 2^2  + 0 \* 2^1 + 0 \* 2^0 

One important thing to note here is the fixed range of our example 8 bit unsigned integer. We can only represent so many unique values using 8-bits, in fact we can determine that number fairly easily. Observe that,
> For a bitstring of size **1**:<br>
> &nbsp;&nbsp;&nbsp;&nbsp;The unique strings are "**0**" and "**1**"<br>
> &nbsp;&nbsp;&nbsp;----> **2** unique values.<br><br>
> For a bitstring of size **2**:<br>
> &nbsp;&nbsp;&nbsp;The unique strings are "**00**", "**01**", "**10**", and "**11**"<br>
> &nbsp;&nbsp;&nbsp;----> **4** unique values.<br>

Thus, the maximum number of unique values a bit string of size *n* ≥ 1 can have is
> 2^*n*

So an 8-bit unsigned integer can represent a total of 2^8 = **256** unique values. 

Consequently, given a *n*-bit unsigned integer, its range can be expressed as [0, (2^*n*)-1]. So the maximum value of a 8-bit unsigned integer is (2^8) - 1 = 256-1 = 255, and the minimum value is **0**. The inclusion of zero and exclusion of the value 2^*n* is out of convention. We could just as easily say make the range [1,2^n], but computer scientists have collectively recognized the value and importance of representing **0**. Now what about representing negative integers? That's where signed integers come into play.

## Signed Integers and Two's Complement
To represent both negative and positive integers in binary we have **signed** integers. Signed integers are stored much like unsigned integers, except in two regards:

#### Difference 1 - The Sign Bit
One bit, called the **sign bit**, is set aside from the number to represent whether the number is positive of negative. The sign bit is generally the most significant bit, i.e. the farthest left bit, with a sign bit of **0** representing positive numbers, while **1** representing negatives. 
#### Difference 2 - Negatives and Two's Complement
Negative binary integers are stored as the **Two's Complement** of their positive counterparts. The Two's Complement of a binary value can be found by inverting every bit, i.e. turning **0**'s to **1**'s and vice versa, then adding **1** to the result. In essence, the Two's Complement of a binary value is its *additive inverse*. When a number and its additive inverse are summed, the result is **0**, likewise when a fixed length binary number and its **Two's Complement** are summed, the resulting bitstring will contain only zero's (although a special flag will be set, called the **carry** bit).

A 8-bit signed integer *i* would be stored like so (each character is a single bit),
> SBBB BBBB
> 
> S = Sign Bit
> B = Binary representation of *i*

Now let's say *i* = 21, then *i* would be stored as,
> 0001 0101<br>
> ^------------ Notice the sign bit is **0**

Now let's say *j* is a 8-bit signed integer where *j* = -21. Remember that a negative signed integer is the Two's complement its positive counterpart. Thus, to find the binary representation of *j*, we must first invert the bits of the binary representation of 21. In C bitwise inversion can be be done via the *bitwise not* operator (**~**).
> ~ (00010101) = 11101010

Next we simply add the binary number one to the result,
> 11101010 + 0000001 = 11101011 

Thus, for a 8-bit signed integer, base-2(11101011) = -21. Now, observe what happens when we add *i* and *j*.
> &nbsp;&nbsp;&nbsp;0001 0101<br>
> \+ 1110 1011 <br>
> \---------------<br>
> &nbsp;1&nbsp;0000 0000<br>
>&nbsp;^---- Notice that this bit exceeds our 8-bit storage size, therefore it is effectively **lost**, but as mentioned above the carry flag is set.

Thus *i* + *j* = base-2(00000000) = **0**!

Since we need to use one bit to represent the sign of integer, the range of a *n*-bit signed integer is [-2^(*n*-1), 2^(*n*-1)-1]. So the maximum value of a 8-bit signed integer is 2^(8-1) - 1 = (2^7) - 1 = 128-1 = 127, and the minimum value is -2^(8-1) = -2^7  = -128. Note that this is consistent with the maximum number of unique values that an *n* size bit string can have: the interval [-128,-1] has 128 values, the interval [1,127] has 127 values, and finally we have the value **0** for a total number of **256** unique values for a 8-bit signed integer!

Now that we have an understanding of how integers are stored and the difference between signed and unsigned integers, we'll examine some specific integer data types in C along with their properties. 
## Storage Size and Ranges

The maximum/minimum value that an integer can have depends on the data type of the integer. The integer data types are as follow in order of ascending size: char, short, int, long, long long. Again, each of these data types may be unsigned or signed with signed generally being the implicit representation, e.g. "short" vs. "unsigned short" and "int" vs. "unsigned int". The table below gives a detailed look at each data type and its properties. 

| Data Type        | Size (in bytes)\*| Typical Range\*                              |
| ---------------- |:----------------:|:-------------------------------------------- |
| char             | 1                | \*\*                                         |
| signed char      | 1                | [-128, 127]                                  |
| unsigned char    | 1                | [0, 255]                                     |
| short            | 2                | [-32767, 32766]                              |
| unsigned short   | 2                | [0, 65535]                                   |
| int              | 2 or 4           | [-32767, 32766] or [-2147483648, 2147483647] |
| unsigned int     | 2 or 4           | [0, 65535] or [0, 4294967295]                |
| long             | 8                | [-9223372036854775808, 9223372036854775807]  |
| unsigned long    | 8                | [0, 18446744073709551615]                    |

*\*Note: the actual size/range of the data type varies on implementation, but <br>
the data type is guaranteed to be >= size and contain the range given.* <br>
*\*\*Note: The signedness of char is implementation specific.*

# Real Numbers in C

Objective: Discuss real numbers, ways to represent them, and how they are stored in C. 

## Definition of a Real Number
Now that we can represent integers, we'll take a look at the interesting problems with representing non-integer real numbers. Real numbers include integers, rationals (1/2), and irrationals (√2). Storing these values can be a challenge, especially for repeating rationals like 1/3 = 0.33333... or irrationals, which contain an infinite sequence of non-repeating values (π). How can we store numbers that can be extremely large, like 2^200, and also store numbers that can have an exceedingly long sequence of digits (1/3)? Before we explore how computers tackle this, we should take a look at a way scientists commonly represent these values.

## Scientific Notation
Scientific-Notation is a way to represent very large and small numbers while making the significant digits
clearly recognizable. Significant digits are defined as all digits except: 
-   All [leading zeros](https://en.wikipedia.org/wiki/Leading_zeros "Leading zeros"). For example, "013" has 2 significant figures: 1 and 3
-   [Trailing zeros](https://en.wikipedia.org/wiki/Trailing_zeros "Trailing zeros") when they are merely placeholders to indicate the scale of the number (exact rules are explained at [identifying significant figures](https://en.wikipedia.org/wiki/Significant_figures#Identifying_significant_figures))
-   [Spurious](https://en.wiktionary.org/wiki/spurious "wikt:spurious") digits introduced, for example, by calculations carried out to greater precision than that of the original data, or measurements reported to a greater precision than the equipment supports.

Using Scientific-Notation we represent a number like so,
>    *m* \* 10^*n*

Where *m* (the mantissa) is the sequence of significant digits of the number and *n* is the number of decimal places to the left or right the mantissa begins. The following are a list of base-10 numbers expressed in Scientific-Notation:
> 1230000 = 1.23 * 10^6<br>
> 0.00007 = 7.00 * 10^(-5)<br>
> 1.50700 = 1.507 * 10^0<br>

Floating-point representation is very similar to Scientific-Notation. In computing, floating-point arithmetic is defined as arithmetic using formulaic representation of real numbers as an approximation to support a trade-off between range and precision [(more here)](https://en.wikipedia.org/wiki/Floating-point_arithmetic). 

## Range vs. Precision
**Range** refers to the set of values that can be represented by the system, we typically think of this as an interval from a smallest number to a largest number, e.g. [-100, 100]. 

**Precision** is the degree of accuracy of a representation, typically in number of digits. Precision goes hand and hand with the concept of significant digits, the more significant digits we use to approximate a number, the more precise our approximation. For example, we may say π ≈ 3, which is true although we may be more *precise* and say π ≈ 3.1415. On the other hand π ≈ 3.141500000 is no more precise than π ≈ 3.1415 or π ≈ 0003.1415.

As stated above, floating-point arithmetic standards try to maximize both of these properties given a finite number of bits to represent a single number. One such standard is **IEEE-754**, which is perhaps the most common computing standard for storing floating point values.

## Physical Storage and IEEE Standards

**IEEE-754** floats (4 bytes) or doubles (8 bytes) are composed of three parts: a sign bit to represent the whether the number is positive or negative, an exponent giving its order of magnitude, and a mantissa (the coefficient) which contains the significant digits of the number. An IEEE-754 float has a binary representation as follows (each character is a **bit**):
> SEEEEEEE EMMMMMMM MMMMMMMM MMMMMMMM<br>
> S = Sign bit<br>
> E = Exponent bit<br>
> M = Mantissa (coefficient/significand) bit<br>


## Normalized vs. Denormalized

## Overflow (INF/NAN)

## Equality

## Loss of Significance

## Storage Size and Ranges

<INSERT_WORDS>