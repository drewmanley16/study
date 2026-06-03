/*
 * CS 330 — Exercise 3: C Structs & Linked Lists
 *
 * Topics: typedef struct, struct on heap, singly linked list
 *         (insert, search, delete, free).
 *
 * Build: gcc -Wall -g -o structs structs.c && ./structs
 */

#include <stdio.h>
#include <stdlib.h>

/* ── Data structure ──────────────────────────────────────────────────────────*/

typedef struct Node {
    int val;
    struct Node* next;
} Node;

/* ── Exercise 3.1 ─────────────────────────────────────────────────────────────
 * Allocate and return a new Node with the given val and next=NULL.
 */
Node* node_new(int val) {
    /* TODO */
    return NULL;
}

/* ── Exercise 3.2 ─────────────────────────────────────────────────────────────
 * Insert val at the FRONT of the list. Return the new head.
 * Example: insert(head=2->3, val=1) returns 1->2->3
 */
Node* insert_front(Node* head, int val) {
    /* TODO */
    return NULL;
}

/* ── Exercise 3.3 ─────────────────────────────────────────────────────────────
 * Append val at the END of the list. Return the (possibly new) head.
 * If head is NULL, the new node becomes the head.
 */
Node* insert_back(Node* head, int val) {
    /* TODO */
    return NULL;
}

/* ── Exercise 3.4 ─────────────────────────────────────────────────────────────
 * Return the length of the linked list.
 */
int list_length(Node* head) {
    /* TODO */
    return 0;
}

/* ── Exercise 3.5 ─────────────────────────────────────────────────────────────
 * Return 1 if val is in the list, 0 otherwise.
 */
int list_contains(Node* head, int val) {
    /* TODO */
    return 0;
}

/* ── Exercise 3.6 ─────────────────────────────────────────────────────────────
 * Delete the FIRST node whose val matches. Return the (possibly new) head.
 * If val not found, return head unchanged.
 * Free the deleted node!
 */
Node* list_delete(Node* head, int val) {
    /* TODO */
    return head;
}

/* ── Exercise 3.7 ─────────────────────────────────────────────────────────────
 * Free every node in the list. After this, the list is empty (NULL).
 */
void list_free(Node* head) {
    /* TODO */
}

/* ── Exercise 3.8 ─────────────────────────────────────────────────────────────
 * Reverse the linked list in-place (no new allocations).
 * Return the new head.
 * Hint: use three pointers: prev, curr, next.
 */
Node* list_reverse(Node* head) {
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

    /* Build list: 1 -> 2 -> 3 -> 4 -> 5 */
    Node* head = NULL;
    for (int i = 5; i >= 1; i--)
        head = insert_front(head, i);

    total++; pass += chk("length 5", list_length(head), 5);
    total++; pass += chk("contains 3", list_contains(head, 3), 1);
    total++; pass += chk("not contains 9", list_contains(head, 9), 0);
    if (head) { total++; pass += chk("front value", head->val, 1); }

    /* insert_back */
    head = insert_back(head, 6);
    total++; pass += chk("length after back insert", list_length(head), 6);

    /* delete middle */
    head = list_delete(head, 3);
    total++; pass += chk("length after delete", list_length(head), 5);
    total++; pass += chk("3 gone", list_contains(head, 3), 0);
    total++; pass += chk("2 still there", list_contains(head, 2), 1);

    /* delete head */
    head = list_delete(head, 1);
    total++; pass += chk("new head is 2", head ? head->val : -1, 2);

    /* reverse: 2->4->5->6 becomes 6->5->4->2 */
    head = list_reverse(head);
    total++; pass += chk("reverse: new head is 6", head ? head->val : -1, 6);
    /* walk to end */
    Node* tmp = head;
    while (tmp && tmp->next) tmp = tmp->next;
    total++; pass += chk("reverse: tail is 2", tmp ? tmp->val : -1, 2);

    list_free(head);
    printf("  PASS  list_free (no crash)\n"); pass++; total++;

    /* Edge: empty list */
    total++; pass += chk("length of NULL", list_length(NULL), 0);

    printf("\n%d / %d passed\n", pass, total);
    return pass == total ? 0 : 1;
}
