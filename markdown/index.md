---
title: Computer Systems and Organization 1
...

# Overview 

This is part of the foundational CS courses:
courses designed to cover content needed in later CS courses.

## Eligibility

You should take this course only if

1. You have credit (or passed the placement test) for at least one of CS 1110, CS 1111, CS 1112, CS 1113, or CS 1120
1. You have do **not** have credit for CS 2110 or beyond

More information about the transition from previous courses to the new foundation
may be found at <http://advising.uvacs.org/>.

## Scope and Content

In this course, we 

- Begin with how data can be stored as charges in silicon and work up
    - In hardware design, through gates and registers to general-purpose computers.
    - In data representation, through bits and bytes to records, arrays, and pointers.
    - In process representation, through circuits and assembly to C.
- Learn basic command-line tools and accessing command-line documentation.
- Practice quite a bit of C coding and using the C standard library.
- Discuss how security and social topics are related to these ideas.

For the sake of conversing with those familiar with our previous course offerings,
this course covers the assembly-and-C half of CS 2150 "Program and Data Representation";
the basics of ECE 2330 "Digital Logic Design";
and the first part of CS 3330 "Computer Architecture";
in addition to having several new topics we felt were under-represented in our
previous set of course offerings.

# Logistics, etc

See [the course policies page](policies.html).

# Writeups

The following are the main writeups created for this course:

- [Boolean Algebra and Gates](bool.html) including bit-fiddling
- [Bits and Beyond](bits.html) including number representations and a little information theory
- [Components of digital computers](parts.html), including voltage, registers, and HDLs
- [Designing a processor](isa.html), including von Neumann architecture, ISAs, condition codes, and RISC/CISC
- [x86-64 Summary](x86.html), including calling conventions
- [C, a guide and reference](c.html), including the C preprocessor
- [An overview of memory](memory.html), including garbage detection and common memory errors
- [C standard library manual pages](manpage.html), including a guide to using the `man` command
- [C++ Inheritance](vtable.html), including how vtables enable virtual functions

The following are additional references:

- [Using SSH](help-ssh.html), including how to set up passwordless authentication
- [Command-fu](command-fu.html), a few simple command-line examples (unfinished)
- [Debugger example](cmdadd.html), using `lldb` and `ghex`
- [Eduroam on Linux](//www.cs.virginia.edu/luther/tips/linux-at-uva.html), including how to connect to UVA's instantiation of eduroam and handling digital certificates.

The following are assignment writeups:

- [Bit fiddling](pa01-bit fiddling.html)
- [Gates](pa02-worksheet.html)
- [Binary coding 1: Mult](pa03-mult.html)
- [Binary coding 2: Fib](pa04-fib.html)
- [x86-64 Assembly](pa05-assembly.html)
- [Assembly Debugging](pa06-bomb.html)
- [Small C Functions](pa07-smallc.html)
- [Linked List in C](pa08-linkedlist.html)
- [Postfix Calculator](pa09-postfix.html)
- [Socket-based chat](pa10-schat.html)

The following are lab writeups:

- [SSH and Editors](lab00-ssh-ed.html)
- [Git & Information Theory](lab01-git-infotheory.html)
- [Hex Editor](lab02-hex-editor.html)
- [ISA Simulator](lab03-simulator.html)
- [Tools help](lab04-tools.html)
- [Debugger](lab05-debugger.html)
- [Assembly Debugging](lab06-bomb.html)
- [`char *` coding](lab07-char*.html)
- [File-based chat system](lab08-fchat.html)
- [Sockets](lab09-sockets.html)
- [From C to C++](lab10-cpp.html)
- [The C++ STL](lab11-stl.html)


