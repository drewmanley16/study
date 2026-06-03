/*
 * CS 330 — Exercise 9: Red-Black Tree Insert
 *
 * This is the hardest CS 330 topic. Work through it carefully.
 *
 * RBT Properties (must hold after every operation):
 *   1. Every node is RED or BLACK.
 *   2. The root is BLACK.
 *   3. Every leaf (NIL sentinel) is BLACK.
 *   4. If a node is RED, both children are BLACK (no two consecutive reds).
 *   5. All paths from a node to its descendant NIL leaves have the same
 *      number of BLACK nodes (black-height is uniform).
 *
 * Build: g++ -Wall -g -o rbt rbt.cpp && ./rbt
 */

#include <iostream>
#include <vector>
#include <cassert>
using namespace std;

enum Color { RED, BLACK };

struct RBNode {
    int     val;
    Color   color;
    RBNode* left;
    RBNode* right;
    RBNode* parent;
    bool    is_nil;  /* true for the sentinel NIL node */

    RBNode(int v, Color c, RBNode* nil)
        : val(v), color(c), left(nil), right(nil), parent(nil), is_nil(false) {}

    /* Constructor for the NIL sentinel */
    RBNode() : val(0), color(BLACK), left(nullptr), right(nullptr), parent(nullptr), is_nil(true) {}
};

class RBTree {
public:
    RBNode* NIL;   /* sentinel — represents all NULL leaves */
    RBNode* root;

    RBTree() {
        NIL  = new RBNode();   /* black sentinel */
        root = NIL;
    }

    ~RBTree() {
        free_tree(root);
        delete NIL;
    }

    /* ── Exercise 9.1 ─────────────────────────────────────────────────────────
     * Left rotation around node x.
     *
     *      x                y
     *     / \              / \
     *    A   y    →       x   C
     *       / \          / \
     *      B   C        A   B
     *
     * Steps:
     *   1. y = x->right
     *   2. x->right = y->left  (B becomes x's right child)
     *   3. If y->left != NIL, update y->left->parent = x
     *   4. y->parent = x->parent  (link y to x's parent)
     *   5. Update x's parent to point to y instead of x
     *   6. y->left = x; x->parent = y
     */
    void left_rotate(RBNode* x) {
        /* TODO */
    }

    /* ── Exercise 9.2 ─────────────────────────────────────────────────────────
     * Right rotation around node y (mirror of left_rotate).
     *
     *        y            x
     *       / \          / \
     *      x   C   →    A   y
     *     / \              / \
     *    A   B            B   C
     */
    void right_rotate(RBNode* y) {
        /* TODO */
    }

    /* ── Exercise 9.3 ─────────────────────────────────────────────────────────
     * RBT Insert.
     *
     * Step 1: Standard BST insert, color new node RED.
     * Step 2: Call insert_fixup to restore RBT properties.
     */
    void insert(int val) {
        RBNode* z = new RBNode(val, RED, NIL);

        /* Step 1: BST insert */
        RBNode* y = NIL;
        RBNode* x = root;
        while (x != NIL) {
            y = x;
            if (z->val < x->val)      x = x->left;
            else if (z->val > x->val) x = x->right;
            else { delete z; return; }  /* duplicate — ignore */
        }
        z->parent = y;
        if (y == NIL)         root = z;
        else if (z->val < y->val) y->left = z;
        else                      y->right = z;

        /* Step 2: Fix-up */
        insert_fixup(z);
    }

    /* ── Exercise 9.4 ─────────────────────────────────────────────────────────
     * insert_fixup: restore RBT properties after inserting node z (colored RED).
     *
     * The only violation possible is property 4 (two consecutive reds):
     * z is red and z->parent is also red.
     *
     * Loop while z->parent is RED (violation exists):
     *
     * CASE: z's parent is a LEFT child of grandparent:
     *   Let uncle = grandparent->right
     *
     *   Case 1: uncle is RED
     *     → Recolor: parent = BLACK, uncle = BLACK, grandparent = RED
     *     → Move z up to grandparent and continue
     *
     *   Case 2: uncle is BLACK, z is a RIGHT child
     *     → Left-rotate around parent (makes z a left child)
     *     → Fall through to Case 3
     *
     *   Case 3: uncle is BLACK, z is a LEFT child
     *     → Recolor parent = BLACK, grandparent = RED
     *     → Right-rotate around grandparent
     *
     * MIRROR: z's parent is a RIGHT child of grandparent (swap left/right).
     *
     * After loop: color root BLACK.
     */
    void insert_fixup(RBNode* z) {
        /* TODO */
        root->color = BLACK;  /* always ensure root is black */
    }

    /* ── Exercise 9.5 ─────────────────────────────────────────────────────────
     * Verify all 5 RBT properties hold. Returns true if valid.
     * Used by the tests — implement the helpers below.
     */
    bool is_valid() {
        if (root == NIL) return true;
        if (root->color != BLACK) { cerr << "root not black\n"; return false; }
        int bh = -1;
        return check_node(root, 0, bh);
    }

    bool search(int val) {
        RBNode* cur = root;
        while (cur != NIL) {
            if (val == cur->val) return true;
            cur = val < cur->val ? cur->left : cur->right;
        }
        return false;
    }

    void inorder(RBNode* node, vector<int>& out) {
        if (node == NIL) return;
        inorder(node->left, out);
        out.push_back(node->val);
        inorder(node->right, out);
    }

private:
    /* Returns false if any property is violated.
     * black_count = number of BLACK nodes on the path so far (not counting NIL).
     * bh = expected black-height (-1 means not yet established).
     */
    bool check_node(RBNode* n, int black_count, int& bh) {
        if (n == NIL) {
            if (bh == -1) bh = black_count;
            if (bh != black_count) { cerr << "black-height violation\n"; return false; }
            return true;
        }
        if (n->color == BLACK) black_count++;
        if (n->color == RED) {
            if ((n->left  != NIL && n->left->color  == RED) ||
                (n->right != NIL && n->right->color == RED)) {
                cerr << "double-red at " << n->val << "\n";
                return false;
            }
        }
        return check_node(n->left, black_count, bh) &&
               check_node(n->right, black_count, bh);
    }

    void free_tree(RBNode* n) {
        if (!n || n == NIL) return;
        free_tree(n->left);
        free_tree(n->right);
        delete n;
    }
};

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

    RBTree t;

    /* Insert sequence that exercises all fix-up cases */
    vector<int> to_insert = {10, 20, 30, 15, 25, 5, 1, 35, 28, 12};
    for (int v : to_insert) {
        t.insert(v);
        chk(("valid after insert " + to_string(v)).c_str(), t.is_valid());
    }

    /* Search */
    chk("search: found 15",     t.search(15));
    chk("search: found 1",      t.search(1));
    chk("search: not found 99", !t.search(99));

    /* In-order gives sorted output */
    vector<int> order;
    t.inorder(t.root, order);
    bool sorted = true;
    for (int i = 1; i < (int)order.size(); i++)
        if (order[i] <= order[i-1]) { sorted = false; break; }
    chk("inorder is sorted", sorted);
    chk("inorder size", (int)order.size() == (int)to_insert.size());

    /* Root must be black */
    chk("root is black", t.root->color == BLACK);

    /* Duplicate insert should not change size */
    t.insert(10);
    order.clear(); t.inorder(t.root, order);
    chk("no duplicate", (int)order.size() == (int)to_insert.size());

    /* Insert more to stress rotations */
    for (int v : {2, 3, 4, 6, 7, 8, 9}) {
        t.insert(v);
        chk(("stress valid after " + to_string(v)).c_str(), t.is_valid());
    }

    cout << "\n" << pass << " / " << total << " passed\n";
    return pass == total ? 0 : 1;
}
