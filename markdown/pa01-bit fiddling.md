---
title: Bit fiddling
...


# Overview

This HW will give you a chance to practice using binary and bit-wise operators.
You'll likely find [Booleans §4](bool.html) a useful reference.

# Task

Visit <https://kytos.cs.virginia.edu/cso1/pa01.php>
and complete the four problems listed below.
The text boxes want lightweight code using just operators and assignments, like

````c
x = 0x20
y = b + x
````

The goal is to end up with one variable having a particular value,
based on other variables that are provided with new values in each test case.
Do not add conditionals, loops, subroutines, etc.

## The Tasks

We want you to do four of the problems. There are others puzzles on the site as well if you want more practice, but the only four we grade are:

subtract
:   Given `x` and `y`, set `z` to `x - y` without using `-` or multi-bit constants.

    For full credit, use ≤ 10 operations from {`!`, `~`, `+`, `<<`, `>>`, `&`, `^`, `|`}.

bottom
:   Given `b`, set the low-order `b` bits of `x` to 1; the others to 0. For example, if `b` is 3, `x` should be 7. Pay special attention to the edge cases: if `b` is 32 `x` should be &minus;1; if `b` is 0 `x` should be 0. Do not use `-` in your solution.

    For full credit, use ≤ 40 operations from {`!`, `~`, `+`, `<<`, `>>`, `&`, `^`, `|`}.

anybit
:   Given `x`, set `y` to `1` if any bit in `x` is `1`; set `y` to `0` if `x` is all `0`s.

    For full credit, use ≤ 40 operations from {`~`, `+`, `-`, `<<`, `>>`, `&`, `^`, `|`}.

bitcount
:   Given `x`, set `y` to the number of bits in `x` that are `1`.

    For full credit, use ≤ 40 operations from {`!`, `~`, `+`, `-`, `<<`, `>>`, `&`, `^`, `|`}.



# Collaboration

You may work with other students in this class on this assignment, but only in the following two ways:

1. You worked together from the beginning, solving the problem as a team, with each person contributing.
    
    Each teammate should cite this in each problem with a C-style comment at the top of each solution
    and also cite the originator of any single-person contributions where they appear, like
    
    ````c
    // Part of a team with mst3k and lat7h
    x = -y
    w = -x // lat7h came up with this line
    z = x + y
    ````
    

2. You helped someone with a task you'd already finished, helping them think through their incorrect solution and not giving them or trying to lead them to your solution.

    The helper should acknowledge they did this by returning to their previously-submitted solutions
    and re-submitting them with an added comment at the top, like
    
    ````c
    // I helped tj1a
    x = -y
    w = -x
    ````
    
    The helpee should acknowledge they got this by adding a comment at the top, like
    
    ````c
    // tj1a helped me
    x = -y
    w = -x
    ````
    
In all cases, include computing IDs in your citations to streamline our automated tools that assist with collaboration checking.



# Hints

If needed, we have some hints you can look at.

<style>
summary { font-weight: bold; }
details { padding: 1ex; margin: 1ex 0ex; }
details[open] { border-left: thin solid rgba(0,0,0,0.25); border-radius:1ex; }
</style>


<details><summary>subtract</summary>

Consider the definition of two's compliment.

</details>


<details><summary>bottom</summary>

The obvious solution `~(0xFFFFFFFF << b)`{.c} won't work.
Bit shifts always do a modulo on their right-hand operand, so `a << b` does the same thing as `a << (b % (8*sizeof(a))`.
Thus, `<< 32` and `<< 0` do the same thing.

</details>

<details><summary>anybit</summary>

The easy solution would be `y = !!x` but we don't allow `!`. Nor do we allow enough operations to do a loop-like solution.
    
You can divide and conquer.
Try defining `x1` where if any bit anywhere in `x` was `1`, some bit in the bottom 16 bits of `x1` is `1`.
The given task is "see if any `1` bit is in the 32 bits of `x`".
How could you reduce it to "see if any `1` bit is in the bottom 16 bits of `x1`"?

</details>


<details><summary>bitcount</summary>

The obvious solution would be something like

````c
ans = 0;
for(int i=0; i<32; i+=1) {
    a += x&1;
    x >>=1;
}    
````

We don't allow for loops, but even if you replace it with 32 copies that's still 96 operations, and we only allow 40 for this task.

The trick is to do things in parallel, treating a number like a vector of smaller numbers.
Suppose I wanted to count the bits of an 8-bit number with bits `abcdefgh`.
With a little shifting and masking I could make three numbers

    0b00e00h
    0a00d00g
    0000c00f

and add them to get `xx0yy0zz` where `xx = a+b`, `yy = c+d+e`, and `zz = f+g+h`.

Extending this trick to several rounds on 32 bits will solve this problem.

</details>




