---
title: Bomb lab
...

A Mad Programmer got really mad and created a slew of "binary bombs".
Each binary **bomb** is a program, running a sequence of phases.
Each **phase** expects you to type a particular string.
If you type the correct string, then the phase is defused and the bomb proceeds to the next phase.
Otherwise, the bomb **explodes** by printing "BOOM!!!", **telling us it did so**,
and then terminating.

# Work together

In lab, we strongly encourage you to work with one another.
Reading binary is much more fun and effective with someone else to talk to.

You should *not* work together on phase 2, as that is a PA.

# Grading

You'll use the same bomb for this lab and for [the following PA](pa06-bomb.html).

For lab, you need to *either* (a) have a TA record that you were part of a team that defused phase 1 *or* (b) defuse phase 1 on your bomb.

For the PA, you'll need to defuse additional phases on your own.

Each time your bomb explodes it notifies the bomblab server. If we're notified of your bomb exploding 20 times we’ll start removing points.


# How to proceed

1. On a Linux machine, download[^curl] a [binary bomb](http://kytos.cs.virginia.edu:15215/)
    - for credit, you must use your lower-case computing ID

    > Due to changes needed to fix several errors with the bomb server, bombs downloaded before Wednesday, 16 October 2019 at 6:00pm will not be graded for the PA. Please download a new bomb if yours is older than that.

2. Extract the bomb using `tar -xvf bomb#.tar`{.bash} where `#` is your bomb number.
3. `cd bomb#` (again, where `#` is your bomb number).
4. Read the `README`
5. You are welcome to look at `bomb.c` -- it isn't very interesting, though
6. Do whatever you need to to understand what the bomb is doing
7. Only run the bomb `./bomb` once you are confident you can defuse a phase (or at least avoid an explosion)
8. Once you pass a phase visit [the scoreboard](http://kytos.cs.virginia.edu:15215/scoreboard) to verify that we saw your success.

[^curl]: If you want, you can download on portal with the following two lines:
    ````bash
    curl "http://kytos.cs.virginia.edu:15215/?username=$USER&submit=Submit" > bomb.tar
    ````
    ````bash
    tar xvf bomb.tar
    ````

# Hints

If you run your bomb with a command line argument, for example, `./bomb psol.txt`, then it will read the input lines from `psol.txt` until it reaches EOF (end of file), and then switch over to the command line. This will keep you from having re-type solutions.

Because you want to avoid explosions, you'll want to set a breakpoint *before* you run the program so that you can stop the program before it gets to a the function that does the exploding.

You might find it useful to run, `objdump --syms bomb` to get a list of all symbols in the bomb file, including all function names, as a starting point on where you want your breakpoint.

The best way is to use your favorite debugger to step through the disassembled binary. **Almost no students succeed without using a debugger like lldb or gdb.** On the department Unix machines, `lldb` is the debugger that is available. By default GDB verison 7.3 is available, and you can use GDB version 8 by running `module load lldb-8.1` then running `lldb`. You will need to run this `module load` command in each new terminal (the setting will not persist).

To avoid accidentally detonating the bomb, you will need to learn how to single-step through the assembly code and how to set breakpoints. You will also need to learn how to inspect both the registers and the memory states.

It may be helpful to use various utilities for examining the bomb program outside a debugger, as described in "examining the executable" below.

## Bomb Usage

-   The bomb ignores blank input lines.

-   If you run your bomb with a command line argument, for example,

    ````
     linux> ./bomb psol.txt
    ````

    then it will read the input lines from `psol.txt` until it reaches EOF (end of file), and then switch over to `stdin`. This will keep you from having re-type solutions.

## Examining the Executable

-   `objdump -t` will print out the bomb's symbol table. The symbol table includes the names of all functions and global variables in the bomb, the names of all the functions the bomb calls, and their addresses. You may learn something by looking at the function names!

-   `objdump -d` will disassemble all of the code in the bomb. You can also just look at individual functions. Reading the assembler code can tell you how the bomb works.

    If you prefer to get Intel syntax disassembly from `objdump`, you can use `objdump -M intel -d`.

-   `strings` is a utility which will display the printable strings in your bomb.

## Using LLDB

-   If you are on a department Unix machine, `module load clang-llvm` first (this needs to be done once per terminal), so `lldb` is available.

-   Run bomb from a debugger like lldb instead of running it directly. The debugger will allow you to stop the bomb before it detonates.

    For example, if I ran

    ````
    linux> lldb bomb
    (lldb) b methodName
    (lldb) run
    (lldb) kill
    ````

    this will start `lldb`, set a **breakpoint** at `methodName`, and run the code. The code will halt *before* it runs `methodName`; calling `kill` will stop the bomb and exit the current debugging session without `methodName` running.

-   Walk through code using one of
    
    - `nexti` goes one assembly instruction at a time, skipping over function calls
    - `stepi` goes one assembly instruction at a time, entering function calls

    ````
    linux> lldb bomb
    (lldb) b lineNumberForPhase1Call
    (lldb) run
    ````

    *input test passphrase here*

    ````
    (lldb) stepi
    (lldb) register read
    (lldb) frame variable
    ````

    *Generally some parameters are local variables and some are stored in registers. You should see your test passphrase here. Note the hex value of your input*

    ````
    (lldb) disas
    (lldb) nexti
    ````

    *keep `nexti`ing until you see `strings_not_equal` method (a suspicious name that might be checking your passphrase)*

    ````
    (lldb) register read
    (lldb) frame variable
    ````

    *Which one holds your passphase? Try "examining" that and others...*

-   Some useful `lldb` commands:

    `(lldb) frame variable`
    :   prints out the name and value of local variables in scope at your current place in the code.

    `(lldb) register read`
    :   prints the values of all registers except floating-point and vector registers

    `(lldb) x/20bx 0x...`
    :   examine the values of the 20 bytes of memory stored at the specified memory address (0x...). Displays it in hexadecimal bytes.

    `(lldb) x/20bd 0x...`
    :   examine the values of the 20 bytes of memory stored at the specified memory address (0x...). Displays it in decimal bytes.

    `(lldb) x/gx 0x...`
    :   examine the value of the 8-byte integer stored at the specified memory address.

    `(lldb) x/s 0x...`
    :   examines the value stored at the specified memory address. Displays the value as a string.

    `(lldb) x/s $someRegister`
    :   examines the value at register someRegister. Displays the value as a string (assuming the register contains a pointer).

    `(lldb) print expr`
    :   evaluates and prints the value of the given expression

    `call (void) puts (0x...)`
    :   calls the built-in output method `puts` with the given `char *` (as a memory address). See `man puts` for more.

    `(lldb) disas methodName`
    :   gives you the to get the machine instruction translation of the method `methodName`. (If you see a `call` instruction in this output that does not indicate what function it refers to, if on the department machines, make sure you are using lldb version 8.1.)

    `(lldb) disas`
    :   gives you the to get the machine instruction translation of the currently executing method.

    `(lldb) x/6i 0x...`
    :   try to disassemble 6 instructions in memory starting at the memory address 0x...

    `(lldb) b *0x...`
    :   set a breakpoint at the specified memory address (0x...).

    `(lldb) b function_name.`
    :   set a breakpoint at the beginning of the specified function.

    `(lldb) nexti`
    :   step forward by one instruction, skipping any called function.

    `(lldb) stepi`
    :   step forward by one instruction, entering any called function.

    `(lldb) kill`
    :   termiante the program immediately

    `(lldb) help`
    :   brings up lldb's built-in help menu


## On interpreting the disassembly

-   Reviewing the x86-64 calling convention (Figure 3.28 in the textbook or [this reference you may remember from 2150](https://aaronbloomfield.github.io/pdr/book/x86-64bit-ccc-chapter.pdf)) may be helpful.

-   The C standard library function `sscanf` is called `__isoc99_sscanf` in the executable. Try `man sscanf` for more information about this library function.

-   `%fs:0x1234` refers to a value in a "[thread-local storage](https://en.wikipedia.org/wiki/Thread-local_storage)" region at offset `0x1234`. The bomb only has one thread (using multiple threads would allow the bomb to do multiple things at once, but that is not something the bomb needs), so this is effectively a region for extra global variables. In the bomb, this appears mostly to implement [stack canaries](https://en.wikipedia.org/wiki/Stack_buffer_overflow#Stack_canaries), a security feature designed to cause out-of-bounds accesses to arrays on the stack to more consistently trigger a crash.

-   Pay attention to the names of functions being called.

-   Disassembling a standard library function instead of reading the documentation for the function is probably a waste of time.

-   Some of the things later phases might be using include:

    -   calls to `scanf` (which is much like a backwards version of `printf`; try `man scanf` for more)
    -   linked data structure traversal
    -   recursion
    -   string literals
    -   `switch` statements

