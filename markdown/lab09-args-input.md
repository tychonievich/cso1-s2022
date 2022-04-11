---
title: Input and Arguments
...

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
