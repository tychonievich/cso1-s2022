---
title: Input and Arguments
...

The goal of this lab is to give some practice working with the string.h stdio.h and varargs.

#Outline
You will write a program that will do the following: 
1. Read 2 string from standard-in and concatenate them and print the result to the console. 
2. Read 2 intergers from standard-in add them and print the result to the console. 
3. Read 2 floats from standard-in add them and print the result to the console.  
4. Read command line argument that is supplied when you run your program. 


#Helpful functions. 
Let's begin by looking at some function that you'll find helpful in this lab. 

##printf
The `printf` functiona allows you to print to the console. Below is the function prototype for `printf`.  
```
int printf(const char *format, ...) 
```
The first parameter is a pointer to string.  This parameter provides a template of the values that follow and expects some key values.  


| specifier |  Representation         | 
--------------------------------------|
| c         |   Character             |
| d or i    |  Signed decimal integer |
| e or E    | Scientific notation     |
| f         | Decimal floating point  |

The second parameter `...` represents a variable number of parameters.  This means that we can one or more parameters in it's spot.  For example, the following code snippet prints out the value 3. 

```
 printf("%d", 3); 
 
```

We could also print multiple values by adding more parameters and updating the first parameter that represents the format string. Look at the next example> 

``` 
print(" Number 1 %d , and the other number %d", 3, 7) 
```

Notice that the string act as template. Printf will search for the specifier and remplace them, with values for parameters that follow.

##scanf 
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
    char string1[50];
    char string2[50];
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

`strcat` also has a stack buffer overflow error,
as it 
