/*
 * CS 330 — Exercise 10: Mixed C Practice
 *
 * Topics: file I/O, string manipulation, recursion in C,
 *         function pointers, bitwise operations.
 *
 * Build: gcc -Wall -g -o misc misc.c && ./misc
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* ── Exercise 10.1 ────────────────────────────────────────────────────────────
 * Recursive: return n! (factorial).
 * n! = n * (n-1)!, 0! = 1.
 */
long factorial(int n) {
    /* TODO */
    return 0;
}

/* ── Exercise 10.2 ────────────────────────────────────────────────────────────
 * Recursive: return the nth Fibonacci number (0-indexed).
 * fib(0)=0, fib(1)=1, fib(n)=fib(n-1)+fib(n-2).
 */
int fibonacci(int n) {
    /* TODO */
    return 0;
}

/* ── Exercise 10.3 ────────────────────────────────────────────────────────────
 * Return 1 if s is a palindrome (reads same forwards and backwards), 0 otherwise.
 * Use only pointer arithmetic (no string library functions, no indexing).
 */
int is_palindrome(const char* s) {
    /* TODO */
    return 0;
}

/* ── Exercise 10.4 ────────────────────────────────────────────────────────────
 * Given a null-terminated string, reverse it in-place.
 * No extra allocation — use two pointers.
 */
void str_reverse(char* s) {
    /* TODO */
}

/* ── Exercise 10.5 ────────────────────────────────────────────────────────────
 * Return the number of set bits (1s) in x (Brian Kernighan's algorithm).
 * Each iteration: x = x & (x - 1) clears the lowest set bit.
 */
int count_bits(unsigned int x) {
    /* TODO */
    return 0;
}

/* ── Exercise 10.6 ────────────────────────────────────────────────────────────
 * Return 1 if x is a power of 2, 0 otherwise.
 * Use bitwise operations only (one expression, no loops).
 * Hint: a power of 2 has exactly one set bit.
 */
int is_power_of_two(unsigned int x) {
    /* TODO */
    return 0;
}

/* ── Exercise 10.7 ────────────────────────────────────────────────────────────
 * qsort uses a comparator with signature: int cmp(const void* a, const void* b)
 * Returning negative means *a < *b, 0 means equal, positive means *a > *b.
 *
 * Implement:
 *   cmp_int_asc  — compare ints ascending
 *   cmp_int_desc — compare ints descending
 */
int cmp_int_asc(const void* a, const void* b) {
    /* TODO */
    return 0;
}

int cmp_int_desc(const void* a, const void* b) {
    /* TODO */
    return 0;
}

/* ── Exercise 10.8 ────────────────────────────────────────────────────────────
 * Apply a function to every element of arr (like map in functional languages).
 * fn is a function pointer: takes an int, returns an int.
 * Modify arr in-place.
 */
void map_array(int* arr, int n, int (*fn)(int)) {
    /* TODO */
}

/* helper functions for testing map_array */
int double_it(int x) { return x * 2; }
int negate(int x)    { return -x; }

/* ─────────────────────────────────────────────────────────────────────────────
 * Tests
 */
int chk(const char* name, int got, int expected) {
    if (got == expected) { printf("  PASS  %s\n", name); return 1; }
    printf("  FAIL  %s  got=%d  expected=%d\n", name, got, expected);
    return 0;
}

int main(void) {
    int pass = 0, total = 0;

    /* 10.1 factorial */
    total++; pass += chk("factorial(0)", (int)factorial(0), 1);
    total++; pass += chk("factorial(5)", (int)factorial(5), 120);
    total++; pass += chk("factorial(10)", (int)factorial(10), 3628800);

    /* 10.2 fibonacci */
    total++; pass += chk("fib(0)", fibonacci(0), 0);
    total++; pass += chk("fib(1)", fibonacci(1), 1);
    total++; pass += chk("fib(7)", fibonacci(7), 13);
    total++; pass += chk("fib(10)", fibonacci(10), 55);

    /* 10.3 is_palindrome */
    total++; pass += chk("palindrome racecar",  is_palindrome("racecar"), 1);
    total++; pass += chk("palindrome a",        is_palindrome("a"), 1);
    total++; pass += chk("palindrome madam",    is_palindrome("madam"), 1);
    total++; pass += chk("not palindrome hello",is_palindrome("hello"), 0);

    /* 10.4 str_reverse */
    char s1[] = "hello";
    str_reverse(s1);
    total++; pass += chk("str_reverse hello→olleh", strcmp(s1,"olleh")==0, 1);
    char s2[] = "a";
    str_reverse(s2);
    total++; pass += chk("str_reverse single char", strcmp(s2,"a")==0, 1);

    /* 10.5 count_bits */
    total++; pass += chk("count_bits(0)",  count_bits(0),  0);
    total++; pass += chk("count_bits(7)",  count_bits(7),  3);  /* 0b111 */
    total++; pass += chk("count_bits(255)",count_bits(255),8);

    /* 10.6 is_power_of_two */
    total++; pass += chk("pow2(1)",  is_power_of_two(1),  1);
    total++; pass += chk("pow2(8)",  is_power_of_two(8),  1);
    total++; pass += chk("pow2(6)",  is_power_of_two(6),  0);
    total++; pass += chk("pow2(0)",  is_power_of_two(0),  0);

    /* 10.7 qsort with comparators */
    int arr[] = {5, 2, 8, 1, 9, 3};
    qsort(arr, 6, sizeof(int), cmp_int_asc);
    total++; pass += chk("qsort asc[0]", arr[0], 1);
    total++; pass += chk("qsort asc[5]", arr[5], 9);
    qsort(arr, 6, sizeof(int), cmp_int_desc);
    total++; pass += chk("qsort desc[0]", arr[0], 9);
    total++; pass += chk("qsort desc[5]", arr[5], 1);

    /* 10.8 map_array */
    int m[] = {1, 2, 3, 4, 5};
    map_array(m, 5, double_it);
    total++; pass += chk("map double[0]", m[0], 2);
    total++; pass += chk("map double[4]", m[4], 10);
    map_array(m, 5, negate);
    total++; pass += chk("map negate[0]", m[0], -2);
    total++; pass += chk("map negate[4]", m[4], -10);

    printf("\n%d / %d passed\n", pass, total);
    return pass == total ? 0 : 1;
}
