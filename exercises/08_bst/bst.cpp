/*
 * CS 330 — Exercise 8: Binary Search Tree
 *
 * Topics: BST insert, search, in-order traversal (gives sorted order),
 *         min/max, height, deletion (3 cases).
 *
 * Build: g++ -Wall -g -o bst bst.cpp && ./bst
 */

#include <iostream>
#include <vector>
#include <climits>
using namespace std;

struct Node {
    int   val;
    Node* left;
    Node* right;
    Node(int v) : val(v), left(nullptr), right(nullptr) {}
};

/* ── Exercise 8.1 ─────────────────────────────────────────────────────────────
 * Insert val into the BST rooted at root. Return the (possibly new) root.
 * BST property: left subtree keys < node key < right subtree keys.
 * Duplicate values: ignore (don't insert).
 */
Node* insert(Node* root, int val) {
    /* TODO */
    return root;
}

/* ── Exercise 8.2 ─────────────────────────────────────────────────────────────
 * Return true if val is in the BST, false otherwise.
 */
bool search(Node* root, int val) {
    /* TODO */
    return false;
}

/* ── Exercise 8.3 ─────────────────────────────────────────────────────────────
 * Return the minimum value in the BST. Assume root != nullptr.
 * (Hint: it's the leftmost node.)
 */
int find_min(Node* root) {
    /* TODO */
    return INT_MIN;
}

/* ── Exercise 8.4 ─────────────────────────────────────────────────────────────
 * Return the maximum value in the BST. Assume root != nullptr.
 */
int find_max(Node* root) {
    /* TODO */
    return INT_MAX;
}

/* ── Exercise 8.5 ─────────────────────────────────────────────────────────────
 * In-order traversal: left → root → right.
 * Append each value to result in order.
 * In-order traversal of a BST yields sorted output.
 */
void inorder(Node* root, vector<int>& result) {
    /* TODO */
}

/* ── Exercise 8.6 ─────────────────────────────────────────────────────────────
 * Return the height of the BST.
 * Height of empty tree = -1.
 * Height of a single node = 0.
 * Height = 1 + max(height(left), height(right))
 */
int height(Node* root) {
    /* TODO */
    return -1;
}

/* ── Exercise 8.7 ─────────────────────────────────────────────────────────────
 * Delete the node with the given val. Return the (possibly new) root.
 *
 * Three cases:
 *   1. Node has no children  → just remove it
 *   2. Node has one child    → replace node with its child
 *   3. Node has two children → replace node's value with its IN-ORDER SUCCESSOR
 *      (smallest value in right subtree), then delete the successor.
 *
 * Free the deleted node!
 */
Node* remove(Node* root, int val) {
    /* TODO */
    return root;
}

/* ── Exercise 8.8 ─────────────────────────────────────────────────────────────
 * Free all nodes in the BST (post-order: free children before parent).
 */
void free_tree(Node* root) {
    /* TODO */
}

/* ── Exercise 8.9 ─────────────────────────────────────────────────────────────
 * Return true if the tree is a valid BST.
 * Hint: pass min/max bounds down the recursion.
 *   is_valid(node, min, max): node->val must be in (min, max)
 */
bool is_valid_bst(Node* root, int min_val = INT_MIN, int max_val = INT_MAX) {
    /* TODO */
    return true;
}

/* ─────────────────────────────────────────────────────────────────────────────
 * Tests
 */
int main() {
    int pass = 0, total = 0;
    auto chk = [&](const char* name, bool ok) {
        total++;
        if (ok) { pass++; cout << "  PASS  " << name << "\n"; }
        else         cout << "  FAIL  " << name << "\n";
    };

    /*
     * Build BST:       5
     *                /   \
     *               3     8
     *              / \   / \
     *             1   4 7   9
     */
    Node* root = nullptr;
    for (int v : {5, 3, 8, 1, 4, 7, 9})
        root = insert(root, v);

    /* 8.2 search */
    chk("search: found 7",      search(root, 7));
    chk("search: found 1",      search(root, 1));
    chk("search: not found 6",  !search(root, 6));

    /* 8.3 / 8.4 min / max */
    chk("find_min = 1", find_min(root) == 1);
    chk("find_max = 9", find_max(root) == 9);

    /* 8.5 in-order → sorted */
    vector<int> order;
    inorder(root, order);
    vector<int> expected = {1, 3, 4, 5, 7, 8, 9};
    chk("inorder size",   order.size() == expected.size());
    chk("inorder sorted", order == expected);

    /* 8.6 height */
    chk("height = 2", height(root) == 2);
    Node* single = new Node(42);
    chk("height single = 0", height(single) == 0);
    chk("height null = -1",  height(nullptr) == -1);
    delete single;

    /* 8.7 remove */
    /* Remove leaf */
    root = remove(root, 1);
    chk("remove leaf: 1 gone",   !search(root, 1));
    chk("remove leaf: 3 still",   search(root, 3));

    /* Remove node with one child */
    root = remove(root, 3);   /* 3 now only has right child 4 */
    chk("remove one-child: 3 gone", !search(root, 3));
    chk("remove one-child: 4 still", search(root, 4));

    /* Remove node with two children */
    root = remove(root, 8);   /* 8 has children 7 and 9 → successor is 9 */
    chk("remove two-child: 8 gone", !search(root, 8));
    chk("remove two-child: 9 still", search(root, 9));
    chk("remove two-child: 7 still", search(root, 7));

    /* 8.9 is_valid_bst */
    chk("valid BST after removes", is_valid_bst(root));
    /* Build an invalid tree manually */
    Node* bad = new Node(5);
    bad->left  = new Node(3);
    bad->right = new Node(4);  /* 4 < 5 but on right → invalid */
    chk("invalid BST detected", !is_valid_bst(bad));
    free_tree(bad);

    /* Duplicate insert (should be ignored) */
    int before = 0, after = 0;
    vector<int> tmp; inorder(root, tmp); before = tmp.size();
    root = insert(root, 9);  /* 9 already in tree */
    tmp.clear(); inorder(root, tmp); after = tmp.size();
    chk("no duplicate insert", before == after);

    free_tree(root);
    cout << "  PASS  free_tree (no crash)\n"; pass++; total++;

    cout << "\n" << pass << " / " << total << " passed\n";
    return pass == total ? 0 : 1;
}
