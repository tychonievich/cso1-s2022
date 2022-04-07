When I was designing CSO1, many of the complaints of the committee about the outcomes of the courses it was replacing seemed to share a common theme: there's something shallow about students' understanding of code; they aren't able to tell the silicon is actually doing when running it, which causes them to have unrealistic expectations about what the computer can do.

I thus designed the course with one overarching goal: at the end, I should be able to point to code and discuss the assembly underneath it and have the students engage meaningfully in the discussion. To reach this goal, I see the following elements as key:

1. a rapid but orderly exposure to everything from electrons to an ISA. The details of this are quite flexible, as it's a prep for what follows rather than a key learning outcome itself, but should be detailed enough that later on the students don't waste time wondering "but couldn't the computer just do it differently?" I chose the following beats to tell this story:
    
    1. 0 and 1 are the easiest signals to build things with, but not magical or unique. Larger values are just groups of 0/1 signals.
    
    2. Transistors can make gates, gates can make muxes and adders (and other components of arithmetic expressions you'd write in code) and registers, and with more time you could understand all if Digital Logic Design in full.
    
    3. (durable outcome) Enough on 2's complement and IEEE float that their general structure and behavior will be remembered and can be used in later classes
    
    4. (durable outcome) Enough experience with hexadecimal and the 2^10 suffixes that later classes can use 256GiB and 2^38 B interchangeably without additional cognitive load and 0xE8 can be converted to 11101000 without noticeable effort.
    
    6. A PC register, memory, a register file, and some muxes can create a computer with an ISA consisting of moves, maths, and jumps.
    
    7. You can program real programs with an ISA with just a handful of move, math, and jump instructions in it. Memory serves all purposes here: the code, larger data like arrays, and register spilling.
    
    8. (durable outcome) x86-64 assembly is a fancier ISA, but still just moves, maths, and jumps. It's the dominant ISA today, and while you'll rarely write it by hand you'll need to read it often enough that you'll learn it here, including the stack and calling conventions.
    
    9. (durable outcome) All data lives in memory, and with very rare exceptions there are only four tools memory has to make data out of: enumerations (like unicode and machine code instructions), numbers, adjacency (like arrays and structs and instruction sequences), and pointers.
    
    10. We can define patterns in how to translate code into assembly. If we put those patterns in a program, we have a compiler.
    
    11. The C compiler is a pipeline of the following steps:
        
        1. the pre-processor, performing naive textual replacement
        2. the lexer, splitting "3.4" into a number but "x.y" into two identifiers and an operator
        3. the parser, matching things up into syntax trees
        4. the type checker, which catches bugs and infers things like implicit casts and is the main difference between different languages
        5. the compiler, which creates assembly, using calling conventions and operation sizes to discard notions of types and parameters 
        6. the assembler, which creates machine code
        7. the linker, which matches up labels between different files and libraries to create addresses and fails if that matching doesn't work
        
        There's also a loader, used to move the resulting program into memory and jump to it's main function
    
    12. (durable outcome) Quite a lot of C, notably pointers and the C standard library, always discussed with reference to the types and assembly underlying it.


CSO1 also has two minor threads:

1. Comfort with command line tools such that they can SSH into a Linux system without an X session and do useful things there. This has to be taught, practiced, and modeled in class.

2. Understanding that tech is part of human life. I use three major beats for this:

    1. Back doors can be added intentionally at every level and can be accidentally created by focusing on other aspects of design, and society has decided that we'll risk them being there in return for more features. This puts strange conflicting responsibilities on those of us building the tech.

    2. Notions of ownership of ideas and expression, as embodied in patent and copyright law, are (a) understandable, (b) important, and (c) not super clear when it comes to computing.

    3. The vastness of the command line is an example of a power-user interface, where those with the resources to spare to learn them gain the power to do more things more efficiently and thus acquire more resources in the future. This is a common, almost universal feature of the world: it is easier to give more power to the already powerful and inequity naturally increases. It takes effort to also help the less powerful, effort every software developer can chose to make or not.

