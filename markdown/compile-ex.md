---
title: Compilation example
...

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

:::exmaple
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
        1. 
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
<style>
.tree * {margin: 0; padding: 0;}
.tree ul { list-style: none; }
.tree ul > li {
  margin-left: 15px;
  position: relative;
  padding-left: 5px;
}
.tree ul > li::before {
  content: " ";
  position: absolute;
  width: 1px;
  background-color: #000;
  top: 5px;
  bottom: -12px;
  left: -10px;
}
.tree > ul > li:first-child::before {top: 12px;}
.tree ul > li:not(:first-child):last-child::before {display: none;}
.tree ul > li:only-child::before {
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
.tree ul > li::after {
  content: " ";
  position: absolute;
  left: -10px;
  width: 10px;
  height: 1px;
  background-color: #000;
  top: 12px;
}
</style>
:::

Parsers are related to, but generally not actually implemented as, pushdown automata, a topic you'll learn about in CS 3120. The actual design of parsers is discussed in CS 4610 and CS 4620.
