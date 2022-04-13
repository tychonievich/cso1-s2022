---
title: Input and Arguments
...

The goal of this lab is to give you some practice working with the string.h and stdio.h libraries.

# Outline
You will write a program that will do the following: 

1. Read 2 string from standard-in, concatenate them and print the result to the console. 
2. Read 2 intergers from standard-in, add them and print the result to the console. 
3. Read 2 floats from standard-in, add them and print the result to the console.  
4. Read a command line argument that is supplied when you run your program. 


# Helpful functions. 
Let's begin by looking at some function that you'll find helpful in this lab. 

## printf
The `printf` function allows you to print to the console. Below is the function prototype for `printf`.  

```c
int printf(const char *format, ...) 
```

The first parameter is a pointer to a string.  This parameter provides a template of the values that follow. `printf` expects that this string to include some key specifies. Here as some example specifiers.   


1.  c         **Character**
2.  d or i    **base-10 `int`**
3.  e or E    **Scientific notation `float`**
4.  f         **#.######-notation `float`**

If you wanted to print a char we would pass `"%c"` as the first parameter.  You can ream more about the `printf` by searching the man page by running 

```
man 3 printf
```
We include the value 3 because there are several `printf`s and we are interested in the one in section 3 (the "Library calls" section).  

 
The second `printf` parameter `...` represents a variable number of parameters.  This means that we can place one or more parameters in it's spot.  For example, the following code snippet prints out the value 3. Here we only placing one parameter in the `...`'s position. 

```c
printf("%d", 3); 
```

We could also print multiple values by adding more parameters. Look at the next example. Notice that we also updated the first parameter to include additional format specifiers. 

```c
print(" Number 1 %d , and the other number %d", 3, 7) 
```

This string acts as template. The `printf` method will search for the specifiers and replace them with the values of the parameters that follow.

## scanf 
The `scanf` method allows you to read user input from the console, and has a simpilar prototype to `printf`. 

```c
int scanf(const char *format, ...)
```

You will begin by writing a program that prompts the user to enter two strings. The program then concatenates them, and prints the result:

<pre>
Enter First String: <ins>Hello</ins>
Enter Second String: <ins>Bot</ins>
HelloBot
</pre>

We'll do this using `scanf`, the formatted string entry library function from `stdio.h`,
and `strcat`, the string concatenation library function from `string.h`.

```c
#include <stdio.h>
#include <string.h>

int main() {
    char string1[10];
    char string2[10];
    printf("Enter First String: ");
    scanf("%s", string1);
    printf("Enter Second String: ");
    scanf("%s", string2);
    strcat(string1,string2);
    printf("%s\n", string1);
}
```

Both `scanf` and `printf` are varargs functions with a "format string" as their first argument.
The format string looks for special codes beginning `%s` to represent different data types to parse (`scanf`) or display (`printf`).
`%s` means "a string": a word for `scanf`, any `char *` for `printf`.
Hence

```c
scanf("%s", string1);
```

means "read input, discarding whitespace, until you find a word and store the word as a null-terminated string starting at the address `string1`, overwriting whatever was already there."

The above code has a stack buffer overflow vulnerability.
To see this, try typing a very long word when prompted.
What happens?

`scanf` and `printf` both allow some additional information between the `%` and the `s` (or other letter that specifies a type).
Of note here is the length limit:

```c
scanf("%10s", string1); // reads at most 10 characters
```

Note you need padding for the null byte: `scanf("%10s", string1)` can put 11 bytes into `string1`.

`strcat` also has a stack buffer overflow error, as it modified the buffer associated with first parameter.  Try entering 2 strings that are twelve-charaters each. 

# Task 1.
Modify the program so that it only reads the 10 chars for the strings. 
Modify the string1 array (buffer) so that has enough space to hold the concantinated result. 

## Check in with your TA
Demo an example to your TA showing a program that reads two 10 char words (example 0123456789) and prints the concatenated result. Your code should concatenate the strings with `strcat`, not simply print them next to one another.



# Task 2
Extend the program so that it also reads integers and floats. We begin by adding a prompt that ask the user to enter the value's type.  Users should enter “I” for integers, “F” for floats and “S” for Strings. Note your program should be case sensitive.

You'll likely need to check `man 3 scanf` to learn how to read the different datatypes in.


<pre>
What types of values do you want to add: <ins>F</ins>
Enter your first value: <ins>0.2</ins>
Enter your second value: <ins>0.5</ins> 
</pre> 

Once you’ve entered your values, add the numbers of concatenate the strings and print the result:

<pre>
The results is : 0.700000
</pre> 

:::aside
Try printing the sum of two very small numbers, like `0.0000000001` or `1e-8`.
Notice the error in the answer? That's an error in formatting, not arithmetic.
You could fix it with `%e` instead of `%f` in your `printf`, but then 1+2 would be displayed as `3.000000e+00`, which is rather ugly.

For extra kudos, look through the manual page for `printf` to find a formatting flag you can use that will show 1+2 without an `e` but also show numbers close to 0 with an `e`.
:::

## Check in with your TA
Demo the following to your TA 

1. Adding two integers. 
2. Adding two floats
3. Concatenating two strings. 

# Task 3 

Command line arguments are values passed in after the executiable. Consider the following example

```
./a.out a b c 
```
Here `a`, `b` and `c` are all command line arguments. Let's write a program that reads these values: 


```c
#include <stdio.h>

int main(int argc, const char* argv[]) {
    for(int i = 0; i < argc; i++){
        printf("Argument [%d]: %s\n", i, argv[i]); 
    }
    return 0;
}
```

When you run the program with the command line parameters above you should get the following output.

```
$ ./a.out a b c
Argument [0]: ./a.out 
Argument [1]: a 
Argument [2]: b 
Argument [3]: c
``` 

__Notice the first Argument (Argument `0`) is the name of the program itself.__

Let's extend your program so you can pass in a command-line argument that specifics the type values that you want to enter. For simplicity will only support one type, integers. 


So if a user wants to enter integers they'll run the program like this: 

```
a.out -i 
```

If a users start the program like this, your program should skip the step of prompting the user for the type. If another type of flag is supplied your program should print `invalid flag supplied.` If no flag is supplied your program should prompt the user to enter the type. 

You might may find the `strcmp` function useful. Read the manual page for `strcmp` by running the following command. 
```
man strcmp
```

## Check in with TA 

Demo your program to the TA with the following test cases: 

1. No flag supplied. Should ask for a type first, then two numbers or strings depending on the type given. 
2. `-i` flag supplied. Should ask for two integers.
3. `-h` flag supplied. Should say "invalid flag supplied" and return without doing anything else.



