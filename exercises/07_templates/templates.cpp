/*
 * CS 330 — Exercise 7: Templates
 *
 * Topics: function templates, class templates, template inheritance,
 *         template specialization basics.
 *
 * Build: g++ -Wall -g -o templates templates.cpp && ./templates
 */

#include <iostream>
#include <string>
#include <cassert>
using namespace std;

/* ── Exercise 7.1 ─────────────────────────────────────────────────────────────
 * Write a function template max2<T> that returns the larger of two values.
 * Must work for int, double, string (uses operator<).
 */
template<typename T>
T max2(T a, T b) {
    /* TODO */
    return a;
}

/* ── Exercise 7.2 ─────────────────────────────────────────────────────────────
 * Write a function template find_index<T> that returns the index of the
 * first occurrence of target in arr (length n), or -1 if not found.
 */
template<typename T>
int find_index(T* arr, int n, T target) {
    /* TODO */
    return -1;
}

/* ── Exercise 7.3 ─────────────────────────────────────────────────────────────
 * Implement the templated class Stack<T> using a dynamically-resizing array.
 *
 * Members (private):
 *   T*  data      — heap array
 *   int capacity  — current array size
 *   int top       — index of top element (-1 if empty)
 *
 * Methods:
 *   Stack()           — default capacity 4, top = -1
 *   ~Stack()          — free data
 *   void push(T val)  — push onto stack; double capacity if full
 *   T    pop()        — remove and return top (assume non-empty)
 *   T    peek() const — return top without removing (assume non-empty)
 *   bool empty() const
 *   int  size()  const — number of elements
 *
 * Hint for resize: allocate new array of 2x capacity, copy elements, free old.
 */
template<typename T>
class Stack {
private:
    T*  data;
    int capacity;
    int top;

    void resize() {
        /* TODO: double capacity, copy elements */
    }

public:
    Stack() {
        /* TODO */
    }

    ~Stack() {
        /* TODO */
    }

    void push(T val) {
        /* TODO: resize if needed, then push */
    }

    T pop() {
        /* TODO */
        return T{};
    }

    T peek() const {
        /* TODO */
        return T{};
    }

    bool empty() const {
        /* TODO */
        return true;
    }

    int size() const {
        /* TODO */
        return 0;
    }
};

/* ── Exercise 7.4 ─────────────────────────────────────────────────────────────
 * This mirrors the CS 330 final exam: implement the Vect<T> class and
 * a derived Mat<T> class that stores a 2D matrix as a flat 1D array.
 *
 * Vect<T>:
 *   T*           arr   (protected, so Mat can access it)
 *   unsigned int sz    (protected)
 *
 *   Vect(unsigned int n)          — allocate n T's (use new), zero-init
 *   Vect(unsigned int n, T* src)  — take ownership of src (don't copy, don't allocate)
 *   virtual ~Vect()               — delete[] arr
 *   unsigned int get_size() const
 *   T*           get_elem(unsigned int i) const   — pointer to element at i
 *   virtual void print() const                    — print all elements space-separated + newline
 *
 * Mat<T> : public Vect<T>:
 *   unsigned int rows
 *
 *   Mat(unsigned int m, unsigned int n, T* src)  — calls Vect(m*n, src), stores rows=m
 *   T*   get_elem(unsigned int I, unsigned int J) — pointer to element at (I,J)
 *   void print() const override — print each row on its own line using Vect::print()
 */
template<typename T>
class Vect {
protected:
    T*           arr;
    unsigned int sz;

public:
    Vect(unsigned int n) {
        /* TODO: allocate n T's with new, zero-init */
    }

    Vect(unsigned int n, T* src) {
        /* TODO: take ownership of src (just store the pointer, don't allocate) */
    }

    virtual ~Vect() {
        /* TODO */
    }

    unsigned int get_size() const {
        /* TODO */
        return 0;
    }

    T* get_elem(unsigned int i) const {
        /* TODO */
        return nullptr;
    }

    virtual void print() const {
        /* TODO: print all elements separated by spaces, then '\n' */
    }
};

template<typename T>
class Mat : public Vect<T> {
    unsigned int rows;

public:
    Mat(unsigned int m, unsigned int n, T* src) : Vect<T>(m * n, src) {
        /* TODO: store rows */
    }

    T* get_elem(unsigned int I, unsigned int J) {
        /* TODO: compute flat index and delegate to Vect::get_elem */
        return nullptr;
    }

    void print() const override {
        /* TODO: for each row, create a temporary Vect<T> pointing to that row and call its print() */
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

    /* 7.1 max2 */
    chk("max2 int",    max2(3, 7) == 7);
    chk("max2 double", max2(3.14, 2.71) == 3.14);
    chk("max2 string", max2(string("banana"), string("apple")) == "banana");

    /* 7.2 find_index */
    int arr[] = {5, 3, 8, 1, 9};
    chk("find_index found",     find_index(arr, 5, 8) == 2);
    chk("find_index not found", find_index(arr, 5, 7) == -1);
    chk("find_index first",     find_index(arr, 5, 5) == 0);

    /* 7.3 Stack */
    {
        Stack<int> s;
        chk("Stack empty initially", s.empty());
        s.push(1); s.push(2); s.push(3);
        chk("Stack size 3",   s.size() == 3);
        chk("Stack peek",     s.peek() == 3);
        chk("Stack pop",      s.pop() == 3);
        chk("Stack size 2",   s.size() == 2);
        /* Force a resize by pushing many elements */
        for (int i = 0; i < 20; i++) s.push(i);
        chk("Stack large size", s.size() == 22);
        chk("Stack large peek", s.peek() == 19);
    }

    /* 7.4 Vect / Mat */
    {
        Vect<int> v(4);
        *v.get_elem(0) = 10;
        *v.get_elem(3) = 40;
        chk("Vect get_size", v.get_size() == 4);
        chk("Vect get_elem", *v.get_elem(0) == 10);
        chk("Vect zero init", *v.get_elem(1) == 0);
        cout << "  Vect print: "; v.print();

        /* Mat: 2x3 matrix: [1,2,3 / 4,5,6] */
        int* flat = new int[6]{1,2,3,4,5,6};
        Mat<int> m(2, 3, flat);
        chk("Mat get_elem(0,0)", *m.get_elem(0, 0) == 1);
        chk("Mat get_elem(0,2)", *m.get_elem(0, 2) == 3);
        chk("Mat get_elem(1,0)", *m.get_elem(1, 0) == 4);
        chk("Mat get_elem(1,2)", *m.get_elem(1, 2) == 6);
        cout << "  Mat print:\n"; m.print();
    }

    cout << "\n" << pass << " / " << total << " passed\n";
    return pass == total ? 0 : 1;
}
