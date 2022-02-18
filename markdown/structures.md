---
title: How to store data
...

Computers store almost all data types using a combination of three techniques:
enumerations, adjacency, and pointers.

# Enumerations

Given a finite set of values, I can enumerate them: that is, pick a different bit pattern for each.
Usually there's some effort to make the bit patterns meaningful, but not always.

:::example
The 8-bit value 0x54 could mean any of the following:

[Unsigned integer](bits.html#base-2-binary)
:   eighty-four

[Signed integer](bits.html#negative-numbers)
:   positive eighty-four

[Floating point number with 4-bit exponent](bits.html#on-non-integral-numbers)
:   twelve

[ASCII](lab02-hex-editor.html#ascii)
:   capital letter T: `T`

[Bitvector sets](bool.html#bit-sets-and-flags)
:   The set ${2,3,5}$

[Our example ISA](pa03-mult.html#the-instructions)
:   Flip the all bits of the value in r1

... and [as many other things as you want](bits.html#numbering-everything-else).
You simply have to pick what it means to your code in a given context.
:::

# Adjacency

Virtually all computers built since the 1970s have used **byte-addressable memory**,
meaning that there is a separate address for each [byte](bits.html#bytes-or-octets) of memory.

So how do we store a value too big to fit in one byte?
We store it in several adjacent bytes of memory, one after another.
Because it has several bytes, it technically has several addresses;
we call the smallest-such byte address the address of the entire multi-byte value.

:::example
To store a 4-byte value at address 0x1234
we put the information in the bytes at address address 0x1234, 0x1235, 0x1236, and 0x1237.
:::

If the value is made up of ordered parts, we put the first part in the smallest address, moving up from there

:::example
To store a list of four 1-byte values [2,1,3,0] at address 0x1234
we store 

 address   value
--------- -------
0x1234      2
0x1235      1
0x1236      3
0x1237      0
:::

If the value is not made up of ordered parts, or if the order of the parts is subject to interpretation, we break it up into bytes in some pre-determined but arbitrary way. The most famous example of this is the [endianness of multi-byte integers](bits.html#which-comes-first).

:::example
To store the 32-bit integer 0x12345678 at address 0x1234, there are two competing options in common use today:

 address   little-endian   big-endian
--------- --------------- ------------
0x1234      0x78            0x12
0x1235      0x56            0x34
0x1236      0x34            0x56
0x1237      0x12            0x78
:::

We apply these two rules (place parts adjacently in order, break big things up in a pre-arranged but arbitrary way) recursively.

:::example
Suppose I am writing a program that draws arrows with labels on them.
I define a structure with the following parts:

1. starting point of arrow
2. ending point of arrow
3. label on the arrow

Suppose I also decide that points are each a list of two 16-bit integers
and labels are each a list of eight 8-bit ASCII characters.

Let's store `(0x123,0x345), (0x1, 0x2), "example\0"` at address 0x1234
using a little-endian encoding

 address    value   meaning
---------  -------  ---------------
0x1234      0x23    low-order byte of x coordinate of starting point
0x1235      0x01    high-order byte of x coordinate of starting point
0x1236      0x45    low-order byte of y coordinate of starting point
0x1237      0x03    high-order byte of y coordinate of starting point
0x1238      0x01    low-order byte of x coordinate of ending point
0x1239      0x00    high-order byte of x coordinate of ending point
0x123A      0x02    low-order byte of y coordinate of ending point
0x123B      0x00    high-order byte of y coordinate of ending point
0x123C      0x65    `e`, first character of label
0x123D      0x78    `x`, second character of label
0x123E      0x61    `a`, third character of label
0x123F      0x6d    `m`, fourth character of label
0x1240      0x70    `p`, fifth character of label
0x1241      0x6c    `l`, sixth character of label
0x1242      0x65    `e`, seventh character of label
0x1243      0x00    `\0`, eighth character of label

The entire structure takes up 16 bytes.
:::

:::exercise
Suppose I have an array `x` of 32-bit integers, with the address of the array being 0x10000.

- The address of `x[0]` is <input /> ^[0x10000]
- The address of `x[1]` is <input /> ^[0x10004 -- one 4-byte integer past the start of the array]
- The address of `x[2]` is <input /> ^[0x10008 -- two 4-byte integers past the start of the array]
- The address of `x[i]` (as an expression including `i`) is <input /> ^[0x10000 + 4*i]
:::

:::aside
Padding

Many current memory systems can read 4 bytes into a register in one cycle if the address of the first byte is a multiple of 4, but need multiple cycles if it's not a multiple of 4. Some also have other alignment rules, doing 8-byte reads more easily if the address is a multiple of 8 and so on.

Because of this, most code will *align* the members of a structure or array, adding some unused bytes as *padding* between elements to make sure that each 4-byte integer has an address that is a multiple of 4. This padding does not change the underlying concept of adjacency as a data storage technique; it just tweaks what we mean by "adjacent".
:::


# Pointers

For various reasons, it is sometimes more convenient to build a data out of *references to* other data instead of *copies of* that data.
The memory representation of a reference is the address of the data being referred to.
Addresses of data are often referred to as pointers to that data.

:::aside
Jargon

Every field develops its own technical jargon: special words and terminology those in the field use to refer to topics that they often discuss.
The more discussion a topic gets, the more nuanced the jargon becomes.
Computing pulls most of its jargon from English, which can make you think you understand it because you know English even when you don't know the specific technical meanings being used.

Address
:   A number serving as an index into the big array of bytes called "memory" where (the first byte of) something can be found.

Pointer
:   An address that indicates the location of particular value.
    Or, a variable or other value-container that is expected to contain an address.

Both "address" and "pointer" are used the way we'd use data types like "`int`" or "`float`", and thus used to refer both to the type we expect ("`x` is a pointer variable") and the value we have ("`x` is a pointer to the string `"hi"`").
The two words are often used interchangeably, but they do have subtle differences.
An address is an address even if it's not a *useful* address: it can be the address of nothing, or the address of the second byte of a four-byte value, etc.
A pointer is an address that is properly set up to be used in code: it is either the address of the first byte of a value we can use, or it is the special value "null" meaning "I'm could point to something, but I'm no".

Null
:   A special pointer (usually represented as the address `0x0`) that intentionally doesn't point to anything at all.

We also see some other oddities between these in use; for example

- "the address of x" is something we can compute; the result is "a pointer to x"
- a region of memory only has one address, but many pointers can point to it
- the value of a pointer is an address
- you can say "take the address of" but almost never say "take a pointer to"

While it is common to have the high-level connotation of jargon defined in courses and text, the grammatically-correct usage of it is often left implicit to be picked up by repeated examples.
Because of that, there are dialects of jargon usage and other computer scientists might use "address" and "pointer" a little differently than I've outlined it above.
:::




# Telling them apart

It is hard to overstate the following fact:

<center style="font-size:150%"> <br/>It's all just bytes.<br/> </center>

There is nothing that distinguishes a float, int, character, instruction, array, etc. They're just bytes. We only tell them apart by how we use them.

If you jump to an address, the computer will try to read the byte there as code.
If you load an address into a 4-byte register, the computer will assume it's the first address of a 4-byte value.
If you put a register's value into a floating-point adder, the computer will assume it's a floating-point value.
And so on.

So, how do we keep it all straight when writing code?
There are two common solutions: static and dynamic typing.

## Static typing

In my code, I decide what type of value will go where.
When I make a variable `x`, I decide "this variable, and any register or memory location it is stored in, will always hold a 32-bit signed integer" and I make that explicit in my code by declaring the variable as `int x`.
I also *type-check* my code, asking my compiler to verify that I never tried to put a string into an integer variable or use an integer variable in an instruction that expected an array instead.

C, C++, C#, D, Fortran, Go, Haskell, Java, Kotlin, Objective-C, Rust, Scala, and Swift are all examples of relatively popular staticly-typed languages.

## Dynamic typing

In my code, I *never* store a value by itself.
Every value, from the humblest integer to the most complicated object,
is stored as exactly two pieces (adjacently):

1. An enumeration value telling me what type it is
2. A pointer to the actual value of that type

And my code doesn't blindly assumes it knows what type it found:
instead, it always checks the enumeration first and picks what to do based on what it found.
That "what to do" might be "crash with an error", but it will never be "pretend you have one data type even though you actually have a different data type."

JavaScript, Lua, MATLAB, Perl, PHP, Python, R, Ruby, and Visual Basic are all examples of relatively popular dynamically-typed languages.
