/*
 * CS 330 — Exercise 2: Dynamic Memory Management
 *
 * Topics: malloc, calloc, free, memory leaks, 2D dynamic arrays,
 *         structs on the heap, sizeof.
 *
 * Build: gcc -Wall -g -o memory memory.c && ./memory
 * Check leaks: valgrind --leak-check=full ./memory
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* ── Exercise 2.1 ─────────────────────────────────────────────────────────────
 * Allocate an int array of length n on the heap, fill it with values
 * 0, 1, 2, ..., n-1, and return the pointer.
 * Caller is responsible for freeing.
 */
int* make_range(int n) {
    /* TODO */
    return NULL;
}

/* ── Exercise 2.2 ─────────────────────────────────────────────────────────────
 * Allocate an m×n 2D int array using malloc (array of pointers).
 * Initialize every element to 0.
 * Return int**.  Caller is responsible for freeing with free_2d().
 */
int** alloc_2d(int m, int n) {
    /* TODO */
    return NULL;
}

/* ── Exercise 2.3 ─────────────────────────────────────────────────────────────
 * Free the 2D array allocated by alloc_2d(). m rows were allocated.
 * Must free each row, then the array of pointers. No leaks!
 */
void free_2d(int** arr, int m) {
    /* TODO */
}

/* ── Exercise 2.4 ─────────────────────────────────────────────────────────────
 * Rotate an m×m 2D array 90 degrees COUNTER-CLOCKWISE.
 * This is a classic CS 330 final exam question.
 *
 * CCW rotation rule: new[m-1-j][i] = old[i][j]
 *
 * You may allocate a temporary 2D array. Don't forget to free it!
 */
void rotate_ccw(int** mat, int m) {
    /* TODO */
}

/* ── Exercise 2.5 ─────────────────────────────────────────────────────────────
 * Compute the prefix sum of arr in-place. No extra storage allowed.
 * After: arr[i] = original arr[0] + arr[1] + ... + arr[i]
 * Another classic CS 330 question.
 */
void prefix_sum(int* arr, int n) {
    /* TODO */
}

/* ── Exercise 2.6 ─────────────────────────────────────────────────────────────
 * Given an int array of length n, return a new heap-allocated array
 * containing only the even numbers (in order). Set *out_len to the count.
 * Return NULL and set *out_len=0 if no evens.
 * Caller must free the returned array.
 */
int* filter_evens(int* arr, int n, int* out_len) {
    /* TODO */
    return NULL;
}

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

    /* 2.1 make_range */
    int* r = make_range(5);
    if (r) {
        total++; pass += chk("make_range[0]", r[0], 0);
        total++; pass += chk("make_range[4]", r[4], 4);
        free(r);
    } else { printf("  FAIL  make_range returned NULL\n"); total += 2; }

    /* 2.2 / 2.3 alloc_2d + free_2d */
    int** m2 = alloc_2d(3, 4);
    if (m2) {
        total++; pass += chk("alloc_2d zero init", m2[2][3], 0);
        m2[1][2] = 99;
        total++; pass += chk("alloc_2d write", m2[1][2], 99);
        free_2d(m2, 3);
        printf("  PASS  free_2d (no crash)\n"); pass++; total++;
    } else { printf("  FAIL  alloc_2d returned NULL\n"); total += 3; }

    /* 2.4 rotate_ccw */
    int** mat = alloc_2d(3, 3);
    if (mat) {
        int vals[3][3] = {{1,2,3},{4,5,6},{7,8,9}};
        for (int i = 0; i < 3; i++)
            for (int j = 0; j < 3; j++)
                mat[i][j] = vals[i][j];
        rotate_ccw(mat, 3);
        /* Expected CCW:  3 6 9
                          2 5 8
                          1 4 7  */
        total++; pass += chk("rotate_ccw [0][0]", mat[0][0], 3);
        total++; pass += chk("rotate_ccw [0][2]", mat[0][2], 9);
        total++; pass += chk("rotate_ccw [2][0]", mat[2][0], 1);
        total++; pass += chk("rotate_ccw [1][1]", mat[1][1], 5);
        free_2d(mat, 3);
    } else { total += 4; }

    /* 2.5 prefix_sum */
    int ps[] = {1, 2, 3, 4, 5};
    prefix_sum(ps, 5);
    total++; pass += chk("prefix_sum[0]", ps[0], 1);
    total++; pass += chk("prefix_sum[2]", ps[2], 6);
    total++; pass += chk("prefix_sum[4]", ps[4], 15);

    /* 2.6 filter_evens */
    int src[] = {1, 2, 3, 4, 5, 6};
    int elen = 0;
    int* evens = filter_evens(src, 6, &elen);
    total++; pass += chk("filter_evens count", elen, 3);
    if (evens) {
        total++; pass += chk("filter_evens[0]", evens[0], 2);
        total++; pass += chk("filter_evens[2]", evens[2], 6);
        free(evens);
    } else { total += 2; }

    printf("\n%d / %d passed\n", pass, total);
    return pass == total ? 0 : 1;
}
