/*
 * CS 330 — Exercise 1: Pointers & Pointer Arithmetic
 *
 * Topics: pointer declaration, dereferencing, pointer arithmetic,
 *         arrays as pointers, swap via pointers, 2D pointer indexing.
 *
 * Build: gcc -Wall -g -o pointers pointers.c && ./pointers
 */

#include <stdio.h>
#include <stdlib.h>

/* ── Exercise 1.1 ─────────────────────────────────────────────────────────────
 * Swap two integers using pointers.
 * After swap(a, b): *a and *b should have exchanged values.
 */
void swap(int* a, int* b) {
    /* TODO */
}

/* ── Exercise 1.2 ─────────────────────────────────────────────────────────────
 * Given int* arr of length n, return the sum using ONLY pointer arithmetic.
 * No array subscript notation (arr[i]) allowed — use *(arr + i) or move a pointer.
 */
int sum_array(int* arr, int n) {
    /* TODO */
    return 0;
}

/* ── Exercise 1.3 ─────────────────────────────────────────────────────────────
 * Reverse an array in-place using two pointers (one at start, one at end).
 */
void reverse(int* arr, int n) {
    /* TODO */
}

/* ── Exercise 1.4 ─────────────────────────────────────────────────────────────
 * Given a flat 1D array that represents an m×n matrix in row-major order,
 * return the element at row i, column j (0-indexed).
 * Formula: element at (i,j) = arr[i*n + j]
 */
int matrix_get(int* arr, int n, int i, int j) {
    /* TODO */
    return 0;
}

/* ── Exercise 1.5 ─────────────────────────────────────────────────────────────
 * Count how many elements in arr equal target.
 * Use a pointer (not an index variable) to iterate.
 */
int count_equal(int* arr, int n, int target) {
    /* TODO */
    return 0;
}

/* ─────────────────────────────────────────────────────────────────────────────
 * Tests — do not edit below this line
 */
int check(const char* name, int got, int expected) {
    if (got == expected) { printf("  PASS  %s\n", name); return 1; }
    printf("  FAIL  %s  got=%d  expected=%d\n", name, got, expected);
    return 0;
}

int main(void) {
    int pass = 0, total = 0;

    /* 1.1 swap */
    int x = 3, y = 7;
    swap(&x, &y);
    total++; pass += check("swap: x becomes 7", x, 7);
    total++; pass += check("swap: y becomes 3", y, 3);

    /* 1.2 sum */
    int a[] = {1, 2, 3, 4, 5};
    total++; pass += check("sum_array", sum_array(a, 5), 15);

    /* 1.3 reverse */
    int b[] = {1, 2, 3, 4, 5};
    reverse(b, 5);
    total++; pass += check("reverse[0]", b[0], 5);
    total++; pass += check("reverse[4]", b[4], 1);
    total++; pass += check("reverse[2]", b[2], 3);

    /* 1.4 matrix_get */
    int mat[] = {1,2,3, 4,5,6, 7,8,9}; /* 3x3 */
    total++; pass += check("matrix_get(0,0)", matrix_get(mat, 3, 0, 0), 1);
    total++; pass += check("matrix_get(1,2)", matrix_get(mat, 3, 1, 2), 6);
    total++; pass += check("matrix_get(2,1)", matrix_get(mat, 3, 2, 1), 8);

    /* 1.5 count_equal */
    int c[] = {1, 2, 2, 3, 2};
    total++; pass += check("count_equal 2", count_equal(c, 5, 2), 3);
    total++; pass += check("count_equal 9", count_equal(c, 5, 9), 0);

    printf("\n%d / %d passed\n", pass, total);
    return pass == total ? 0 : 1;
}
