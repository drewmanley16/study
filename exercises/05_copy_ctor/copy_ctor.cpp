/*
 * CS 330 — Exercise 5: Copy Constructors & Deep Copy
 *
 * This is a core CS 330 final exam topic.
 *
 * Topics: shallow vs deep copy, copy constructor, copy assignment operator,
 *         Rule of Three, why default copy breaks heap members.
 *
 * Build: g++ -Wall -g -o copy_ctor copy_ctor.cpp && ./copy_ctor
 */

#include <iostream>
#include <cstring>
using namespace std;

/* ── Exercise 5.1 ─────────────────────────────────────────────────────────────
 * Implement Buffer — a heap-backed char array.
 *
 * The DEFAULT (shallow) copy would share the same heap pointer between
 * two Buffer objects — a disaster when one is destroyed.
 *
 * Implement a DEEP copy constructor and copy assignment operator.
 *
 * Members (private):
 *   char* data   — heap-allocated char array
 *   int   size   — number of chars
 *
 * Methods:
 *   Buffer(int n)                    — allocate n chars, zero-init
 *   Buffer(const Buffer& other)      — DEEP copy constructor
 *   Buffer& operator=(const Buffer& other) — DEEP copy assignment
 *   ~Buffer()                        — free heap memory
 *   char  get(int i) const
 *   void  set(int i, char c)
 *   int   getSize() const
 */
class Buffer {
private:
    char* data;
    int   size;

public:
    Buffer(int n) {
        /* TODO: allocate n chars on heap, zero-init */
    }

    /* Deep copy constructor */
    Buffer(const Buffer& other) {
        /* TODO: allocate NEW memory and copy contents from other */
    }

    /* Deep copy assignment operator */
    Buffer& operator=(const Buffer& other) {
        /* TODO:
         * 1. Handle self-assignment (if this == &other, return *this)
         * 2. Free existing data
         * 3. Allocate new data and copy from other
         * 4. Return *this
         */
        return *this;
    }

    ~Buffer() {
        /* TODO: free data */
    }

    char get(int i) const { return data ? data[i] : 0; }
    void set(int i, char c) { if (data) data[i] = c; }
    int  getSize() const { return size; }
};

/* ── Exercise 5.2 ─────────────────────────────────────────────────────────────
 * This is essentially the CS 330 final exam question.
 *
 * Implement class DynArray<T> with:
 *   T*  arr   (private)
 *   int n     (private)
 *
 *   DynArray(int n)               — allocate n T's, zero-init
 *   DynArray(const DynArray& in)  — deep copy
 *   ~DynArray()                   — free
 *   T&  operator[](int i)         — element access (returns reference!)
 *   int size() const
 *
 * NOTE: this function destroys its argument (on purpose, to test your copy ctor):
 */
template<typename T>
class DynArray {
private:
    T*  arr;
    int n;

public:
    DynArray(int size) {
        /* TODO */
    }

    DynArray(const DynArray& in) {
        /* TODO: deep copy */
    }

    ~DynArray() {
        /* TODO */
    }

    T& operator[](int i) {
        /* TODO */
        static T dummy{};
        return dummy;
    }

    int size() const {
        /* TODO */
        return 0;
    }
};

/* This function deletes its copy — if your copy ctor is correct, the original is untouched */
template<typename T>
void destroy_copy(DynArray<T> copy) {
    for (int i = 0; i < copy.size(); i++)
        copy[i] = T{};  /* zero out */
}   /* copy's destructor fires here */

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

    /* 5.1 Buffer */
    {
        Buffer b1(4);
        b1.set(0, 'H'); b1.set(1, 'i');

        /* Copy constructor */
        Buffer b2(b1);
        chk("copy ctor: b2 has same content", b2.get(0) == 'H' && b2.get(1) == 'i');

        /* Modifying b2 must NOT affect b1 (deep copy!) */
        b2.set(0, 'Z');
        chk("deep copy: b1 unaffected", b1.get(0) == 'H');
        chk("deep copy: b2 changed",    b2.get(0) == 'Z');

        /* Copy assignment */
        Buffer b3(4);
        b3 = b1;
        chk("assign: b3 has b1's content", b3.get(0) == 'H');
        b3.set(1, 'X');
        chk("assign deep: b1.get(1) still i", b1.get(1) == 'i');

        /* Self-assignment should not crash */
        b1 = b1;
        chk("self-assign no crash", b1.get(0) == 'H');
    }

    /* 5.2 DynArray */
    {
        DynArray<int> orig(5);
        for (int i = 0; i < 5; i++) orig[i] = i * 10;

        chk("DynArray[] read", orig[3] == 30);
        chk("DynArray size",   orig.size() == 5);

        /* Pass by value — destroy_copy zeroes its own copy */
        destroy_copy(orig);

        /* Original must be intact */
        chk("after destroy_copy: orig[0]", orig[0] == 0);
        chk("after destroy_copy: orig[4]", orig[4] == 40);

        /* Explicit copy */
        DynArray<int> copy2(orig);
        copy2[0] = 999;
        chk("copy2 independent: orig[0] unchanged", orig[0] == 0);
        chk("copy2 changed",                        copy2[0] == 999);
    }

    cout << "\n" << pass << " / " << total << " passed\n";
    return pass == total ? 0 : 1;
}
