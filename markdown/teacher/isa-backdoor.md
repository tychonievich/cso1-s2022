---
title: "Instructor notes: Backdoors in ISAs"
...


# Outcomes
The students should be able to

1. articulate how nefarious behaviors can be hidden in computer systems
2. appreciate the difficulty of bootstrapping trust
3. evaluate security claims of computer systems critically

# Scheduling
This lesson should follow the students' first exploration of how instructions can be coded into an ISA and parsed with muxes

# Flow
1. Show the instruction parsing code for an already-discussed ISA

2. Add in a chain of logic that checks successive memory reads for some special sequence of bytes

    <div class="example">
    One way to do this is to add a special hidden multi-bit register $R$.
    Use $R$ as the selection input to a mux with fixed constants as the value inputs, and use the output of that mux as the input to an equality comparison circuit.
    Set $R$'s new value to be 0 if the equality is false, or $R+1$ if it is true.

    ````c
    R = (icode != READ_MEMORY) ? R :
        (mem_out == 0x21) && (R == 0) ? 1 :
        (mem_out == 0x30) && (R == 1) ? 2 :
        (mem_out == 0xDE) && (R == 2) ? 3 :
        (mem_out == 0xAD) && (R == 3) ? 4 :
        // ...
        (mem_out == 0x07) && (R == 14) ? 15 :
        0;
    ````
    </div>

3. Add a mux with $R = 15$ (or however many bytes you used) as the selection and two inputs: "normal, documented behavior" and "special secret behavior"

4. Lead a discussion. Example questions to seed discussion include
    
    - Called a "back door": undocumented way to bypass usual rules
    - How could you know if the chip in your laptop had this kind of extra logic?
    - How might the military make use of this kind of technique? Who would have to be on board to do that?
    - If you ran a chip design company for a billion-transistor chip, how could you ensure some engineer somewhere didn't add this kind of back door?
    - If you were building a new smartphone, what *legitimate* practice might lead you to add a back door? What *illegitimate* business demands might be benefited by creating one?

5. Reference (or assign reading of and discuss) "On Trusting Trust"^[Ken Thompson, "Reflections on Trusting Trust", August 1984, *Communications of the ACM* 27(8), pp. 761--763. doi:[10.1145/358198.358210](https://doi.org/10.1145/358198.358210)] or any of the many related papers.

6. Leave a hook by telling students this topic will be revisited as they learn more.

