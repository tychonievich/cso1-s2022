---
title: Compilation example
...

<style>
.tree * {margin: 0; padding: 0; list-style: none; }
.tree li {
  margin-left: 15px;
  position: relative;
  padding-left: 5px;
}
.tree li::before {
  content: " ";
  position: absolute;
  width: 1px;
  background-color: #000;
  top: 5px;
  bottom: -12px;
  left: -10px;
}
.tree > * > li:first-child::before {top: 12px;}
.tree li:not(:first-child):last-child::before {display: none;}
.tree li:only-child::before {
  display: list-item;
  content: " ";
  position: absolute;
  width: 1px;
  background-color: #000;
  top: 5px;
  bottom: 7px;
  height: 7px;
  left: -10px;
}
.tree li::after {
  content: " ";
  position: absolute;
  left: -10px;
  width: 10px;
  height: 1px;
  background-color: #000;
  top: 12px;
}
</style>


# Write code

C code uses curly braces, semi-colons, and type names before variable names during declarations

:::example
```c
#define three (1+2)

int printf(const char *format, ...);

int main() {
    // this is a comment
    double x;
    int y = three;
    /*
    this is also a comment
    */
    x = y>>1;
    printf("%g\n", x);
    return 0;
}
```
:::

# Preprocess

The C pre-processor removes comments, handles any lines that begin with `#`, and may change some other parts.

You can invoke the C pre-processor with the command `cpp`{.sh}. It will add a lot of lines beginning with `#` which are only to help subsequent error messages make sense and we can ignore.

:::example
```c
int printf(const char *format, ...);

int main() {
    double x;
    int y = (1+2);
    x = y>>1;
    printf("%g\n", x);
    return 0;
}
```
:::

The preprocessing can generate errors, such as for unmatched `/*` and `*/`
or invalid `#` lines.

# Lex

A lexer (also called a "tokenizer") identifies the "tokens" in the file.
For example, it knows that `int` is an "identifier"-type token,
`(` is a "left parenthesis"-type token,
`>>` is a "binary operator"-type token,
and so on.

Lexing disambiguates some things, such as deciding that `>>` is one shift token, not two greater-than tokens
and that `1.2` is a single token but `x.y` is three tokens.

Lexing also removes most non-semantic of style like spacing.

:::example
`int` `printf` `(` `const` `char` `*` `format` `,` `...` `)` `;` `int` `main` `(` `)` `{` `double` `x` `;` `int` `y` `=` `(` `1` `+` `2` `)` `;` `x` `=` `y` `>>` `1` `;` `printf` `(` `"%g\n"` `,` `x` `)` `;` `return` `0` `;` `}`
:::

Lexing can generate errors if you type some symbol that's not part of C

Lexers are generally built as an extension of a finite automata, a topic you'll learn about in CS 3120.

# Parse

A parser combines the tokens into a tree structure called an "abstract syntax tree" or AST.

:::example
There are several ways we could make an AST, but one of them is

:::tree
- function declaration
    - `int`
    - `printf`
    - arguments
        1. declaration
            - type
                - `const`
                - `char`
                - `*`
            - name
                - `format`
        1. `...`
- function definition
    - `int`
    - `main`
    - arguments
    - body
        1. definition
            - `double`
            - `x`
        1. initialization
            - `int`
            - `y`
            - `+`
                - `1`
                - `2`
        1. assignment
            - `x`
            - `>>`
                - `y`
                - `1`
        1. invocation
            - `printf`
            - arguments
                1. `"%g\n"`
                2. `x`
        1. return
            - `0`
:::

Note that not all tokens make it into the AST; some, like parentheses and semi-colons, help organize the tree but can then be abstracted away (hence the word "abstract" in "abstract syntax tree").
:::

Parsers can generate errors if you write something that doesn't look like C code.

Parsers are related to, but generally not actually implemented as, pushdown automata, a topic you'll learn about in CS 3120. The actual design of parsers is discussed in CS 4610 and CS 4620.

# Type Checking

A type checker annotates the AST with the type of each expression and variable,
adding implicit type-casts where needed.

:::example
:::tree
- function declaration
    - `int`
    - `printf`
    - arguments
        1. declaration
            - type
                - `const`
                - `char`
                - `*`
            - name
                - `format`
        1. `...`
- function definition
    - `int`
    - `main`
    - arguments
    - body
        1. definition
            - `double`
            - `x` (double)
        1. initialization
            - `int`
            - `y` (int)
            - `+` (int)
                - `1` (int)
                - `2` (int)
        1. assignment
            - `x` (double)
            - (cast to double)
                - `>>` (int)
                    - `y` (int)
                    - `1` (int)
        1. invocation
            - (int) `printf` (const char \*, ...)
            - arguments
                1. `"%g\n"` (const char \*)
                2. `x` (double)
        1. return
            - `0` (int)
:::
:::

Type checking can generate errors if the types of values and operators do not match,
if the declared type does not match usage,
or if you failed to declare something.

Type checking in C is done in a single pass, top to bottom, which means that declarations must precede usage.

:::example
This is valid C

```c
int f();
int g() {
    return f();
}
```

But this is not valid C; in particular, it will fail during type-checking with an "undefined identifier" error on the first use of `f`.

```
int g() {
    return f();
}
int f();
```
:::

After type checking, the declarations can all be removed from the AST as they've been copied to where they were used.


# Code Generation and Optimization

Code generation is the process of turning an annotated AST into assembly.
Typically, this is done with several intermediate steps, varying by compiler, but usually looking something like

1. Turn AST into an assembly-like language with infinite registers
1. Apply various optimizations, such as
    - removing code that doesn't have a lasting impact on the program
    - replacing variables that have a constant value with literals
    - re-ordering code to reduce the number of jumps
    - using the same "register" for different values
    - ISA-specific tricks like replacing `5*x` with `x + x*4` which can be implemented with a `lea` instruction
1. Allocate registers and memory locations
    - a simple (non-optimal) way places all variables in memory
    - optimizations try to find ways to have some variables only in registers
1. Assemble the results

Code generation never generates errors.

The level of optimization can be controlled with various flags to the compiler.
The most common are 

- `-O0` meaning no optimization at all: every variable is written to memory and every line of C code has one or more lines of machine code
- `-O1` meaning basic optimization: use registers where possible, but every line of C code has one or more lines of machine code
- `-O2` meaning normal optimizations: change code in ways that always make it faster
- `-O3` meaning aggressive optimizations: change code in ways that usually makes it faster, but might also make it bigger or slower in certain circumstances
- `-Os` meaning optimize for program size, not program speed

Each of those `-O` flags enables a group of optimizations which can be individually enabled or disabled with `-f...` flags like `-finline-functions` (which will replace some `call`s with the entire code of the called function) and `-fno-inline-functions` (which disables `-finline-functions`).

Code generation, together with all previous steps of compilation, are performed by running `clang -c myfile.c` (or `gcc -c myfile.c`).
To stop before assembling, use `-S` instead of `-c`.

:::example
The assembly generated by `clang -c -Os` on the file used above is

    50                   	push   %rax
    f2 0f 10 05 00 00 00 	movsd  0x0(%rip),%xmm0        # 9 <main+0x9>
    00 
    bf 00 00 00 00       	mov    $0x0,%edi
    b0 01                	mov    $0x1,%al
    e8 00 00 00 00       	callq  15 <main+0x15>
    31 c0                	xor    %eax,%eax
    59                   	pop    %rcx
    c3                   	retq   
:::


The output of code generation is *not* the finished assembly or machine code we'll run.
Rather, it is something called a "relocatable object file" that contains

- The machine code, with placeholders for addresses so that multiple files can be merged without address collision
- Constants and global variables
- The names of functions and variables that other programs can use
- If compiled with `-g`, a rough mapping between source code and the resulting machine code to aid in debugging


# Linking

Most code depends on code written by others.
There are two ways to connect code together; one is called "static linking" or often simply "linking".

Static linking combines several relocatable object files into a single executable.
It places each object file's assembly into memory,
updates all jump and call targets to those new locations,
and links up uses from one file with definitions in other files.

Static linking can generate errors if two of the object files both define the same name.

Dynamic linking is like a deferred static linking.
It has the same general goals: to connect multiple files.
But it picks some of those files and says "don't bundle it with the binary I'm creating now;
instead, load it from a separate file each time I run the program."
Dynamic linking is valuable in saving disk space and reducing memory usage;
it can support fixing a bug in a library for all programs without recompiling them;
but it cal also lead to errors where two programs expect different versions of the same library.

If you run `clang` or `gcc` without the `-c` or `-S` flags, it will perform linking.
You can also run the linker directly as `ld`, though we'll never have you do that.

:::example
The assembly generated by `clang -Os` on the file used above is about 150 assembly instructions
including a staticly-linked `printf` that invokes a dynamically-linked `printf@GLIBC_2.2.5`
where `GLIBC_2.2.5` is the name of a library file to be loaded at runtime.
It also changes addresses in main to resolve linkage, giving

    50                   	push   %rax
    f2 0f 10 05 d7 0e 00 	movsd  0xed7(%rip),%xmm0        # 402008 <_IO_stdin_used+0x8>
    00 
    bf 10 20 40 00       	mov    $0x402010,%edi
    b0 01                	mov    $0x1,%al
    e8 f3 fe ff ff       	callq  401030 <printf@plt>
    31 c0                	xor    %eax,%eax
    59                   	pop    %rcx
    c3                   	retq   
:::

# Loading

Loading takes a program in a file and puts it into memory so it can run.
It resolves dynamic links
and may move some memory around to reduce the chance that certain security vulnerabilities will work.

Loading is performed by the operating system, and most OSes provide several ways to do it, such as

- clicking on an icon in your operating system
- typing `./myprogram` in a terminal window
- if the directory containing `myprogram` is in "the path", typing `myprogram` in a terminal window
- using the `execve` library function or its relatives
