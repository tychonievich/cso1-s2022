---
title: Input and Arguments
...

The goal of this lab is to give some practice working with the string.h stdio.h and varargs.

# Outline
You will write a program that will do the following: 

1. Read 2 string from standard-in and concatenate them and print the result to the console. 
2. Read 2 intergers from standard-in add them and print the result to the console. 
3. Read 2 floats from standard-in add them and print the result to the console.  
4. Read command line argument that is supplied when you run your program. 


# Helpful functions. 
Let's begin by looking at some function that you'll find helpful in this lab. 

## printf
The `printf` functiona allows you to print to the console. Below is the function prototype for `printf`.  
```
int printf(const char *format, ...) 
```
The first parameter is a pointer to string.  This parameter provides a template of the values that follow and expects some key values.  


1.  c         **Character            **
2.  d or i    **Signed decimal integer **
3.  e or E    **Scientific notation     **
4.  f         **Decimal floating point  **

So if wanted to print a char we would pass `"%c"` as the first parameter. 
 
The second parameter `...` represents a variable number of parameters.  This means that we can one or more parameters in it's spot.  For example, the following code snippet prints out the value 3. 

```
 printf("%d", 3); 
```

We could also print multiple values by adding more parameters and updating the first parameter that represents the format string. Look at the next example> 

``` 
print(" Number 1 %d , and the other number %d", 3, 7) 
```

Notice that the string act as template. Printf will search for the specifier and remplace them, with values for parameters that follow.

## scanf 
The `scanf` method allows you to read user input from the console. And has a simpilar prototype to `printf`. 

```
int scanf(const char *format, ...)
```

You will begin by writing a program that prompts the user to enter two strings, concatenates them, and prints the result:

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

int main(){
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
To see this, try typing a hundred-character word when prompted.
What happens?

`scanf` and `printf` both allow some additional information between the `%` and the `s` (or other letter that specifies a type).
Of note here is the length limit:

```c
scanf("%10s", string1); // reads at most 10 characters
```

Note you need padding for the null byte: `scanf("%10s", string1)` can put 11 bytes into `string1`.

`strcat` also has a stack buffer overflow error, as it modified the buffer associated with first parameter.  Try entering 2 strings that are 10 charaters each. 

# Task 1.
Modify the program so that only reads the 10 chars for the strings. 
Modify the string1 array (buffer) so that has enough space to hold the concantinated result. 

### Check in with your TA
Demo an example to your TA showing a program that reads two 10 char words (examples 0123456789) and prints the concantinated result. 



# Task 2
Let’s extend the program so that it reads also reads integers and floats. We begin by adding a prompt that asks the user to the type of values they want to enter.  Users should enter “I” for integers, “F” for floats and “S” for Strings. Note your program shouold be case sentive.   


<pre> 
    What types of values do you want to add: <ins>F</ins>
    Enter your first value: <ins>0.2</ins>
    Enter your second value: <ins>0.5</ins> 
</pre> 

Once you’ve entered your values, The program should print

<pre> 
    The results is : 0.7 
</pre> 



### Check in with your TA
Demo the following to your TA 

1. Adding two integers. 
2. Adding two floats
3. Concating two strings. 

# Task 3 

Command line arguments are values passed in after the executiable. Consider the following example
```
./a.out a b c 
```
Here `a`, `b` and `c` are all command line arguments. So you might be wonderign how you would write a program that reads 


```
#include <stdio.h>

int main(int argc, char** argv)
{
 for(int i = 0; i < argc; i++){
   printf("Argument [%d] : %s \n", i, argv[i]); 
 }
 return 0;
}

```
Notice that we you run the program, with the command line parameters you get the following output.

```
$ ./a.out a b c
Argument [0] : ./a.out 
Argument [1] : a 
Argument [2] : b 
Argument [3] : c
``` 
***Notice the first Argument (Argument [0]) is the name of the program itself. *** 

Now let's extend your your program so that you can pass in command-line arguments that spefic the type values that you want to enter. For simplisity will only support one type integers. 


So if user want to enter intergers the run the program like this: 
``
a.out -i 
``
Since we know from the command line argument that we enter integers, your program should skip the step of prompting the user for the type. If another type of flag is supplied your program should print `` invalid flag supplied.``

##Check in with TA 

Demo your program to the TA with the following test cases: 

    1. No flag supplied. 
    2. -i flag supplied. 
    3.  -h flag supplied (This is the valid flag option. 



