/*
 * CS 330 — Exercise 4: C++ Classes, Constructors, Destructors
 *
 * Topics: class definition, constructor/destructor order,
 *         member initializer lists, heap allocation in a class,
 *         destructor cleanup.
 *
 * Build: g++ -Wall -g -o classes classes.cpp && ./classes
 */

#include <iostream>
#include <cassert>
using namespace std;

/* ── Exercise 4.1 ─────────────────────────────────────────────────────────────
 * Implement class IntArray — a simple heap-backed integer array.
 *
 * Members (private):
 *   int* data  — heap-allocated array
 *   int  size  — number of elements
 *
 * Methods to implement:
 *   IntArray(int n)          — allocate array of n ints, init all to 0
 *   ~IntArray()              — free heap memory
 *   int  get(int i) const    — return element at index i
 *   void set(int i, int val) — set element at index i to val
 *   int  getSize() const     — return size
 */
class IntArray {
private:
    /* TODO: declare members */

public:
    IntArray(int n) {
        /* TODO */
    }

    ~IntArray() {
        /* TODO */
    }

    int get(int i) const {
        /* TODO */
        return 0;
    }

    void set(int i, int val) {
        /* TODO */
    }

    int getSize() const {
        /* TODO */
        return 0;
    }
};

/* ── Exercise 4.2 ─────────────────────────────────────────────────────────────
 * Implement class Counter.
 *
 * A Counter starts at a given value and can be incremented or decremented.
 * It also tracks how many Counter objects currently exist (static member).
 *
 * Members:
 *   int value               — current count
 *   static int instanceCount — number of live Counter objects
 *
 * Methods:
 *   Counter(int start = 0)  — constructor, increments instanceCount
 *   ~Counter()              — destructor, decrements instanceCount
 *   void increment()        — value++
 *   void decrement()        — value--
 *   int  getValue() const
 *   static int getInstanceCount()
 */
class Counter {
private:
    /* TODO */

public:
    Counter(int start = 0) {
        /* TODO */
    }

    ~Counter() {
        /* TODO */
    }

    void increment() { /* TODO */ }
    void decrement() { /* TODO */ }
    int  getValue() const { /* TODO */ return 0; }
    static int getInstanceCount() { /* TODO */ return 0; }
};

/* Define the static member outside the class */
/* TODO: int Counter::instanceCount = 0; */


/* ── Exercise 4.3 ─────────────────────────────────────────────────────────────
 * Implement class Rectangle.
 *
 * Members: double width, height  (private)
 * Methods:
 *   Rectangle(double w, double h)
 *   double area() const
 *   double perimeter() const
 *   void scale(double factor)   — multiply both dimensions by factor
 *   bool isSquare() const       — true if width == height
 */
class Rectangle {
    /* TODO */
public:
    Rectangle(double w, double h) { /* TODO */ }
    double area() const { /* TODO */ return 0; }
    double perimeter() const { /* TODO */ return 0; }
    void scale(double factor) { /* TODO */ }
    bool isSquare() const { /* TODO */ return false; }
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

    /* 4.1 IntArray */
    {
        IntArray arr(5);
        chk("IntArray size", arr.getSize() == 5);
        chk("IntArray zero-init", arr.get(0) == 0 && arr.get(4) == 0);
        arr.set(2, 42);
        chk("IntArray set/get", arr.get(2) == 42);
        chk("IntArray others unchanged", arr.get(1) == 0);
    } /* destructor called here */

    /* 4.2 Counter + static */
    chk("Counter instanceCount starts 0", Counter::getInstanceCount() == 0);
    {
        Counter c1(10);
        chk("Counter instanceCount 1", Counter::getInstanceCount() == 1);
        Counter c2(5);
        chk("Counter instanceCount 2", Counter::getInstanceCount() == 2);
        c1.increment(); c1.increment();
        chk("Counter increment", c1.getValue() == 12);
        c2.decrement();
        chk("Counter decrement", c2.getValue() == 4);
    }
    chk("Counter instanceCount back to 0", Counter::getInstanceCount() == 0);

    /* 4.3 Rectangle */
    {
        Rectangle r(4.0, 3.0);
        chk("Rectangle area", r.area() == 12.0);
        chk("Rectangle perimeter", r.perimeter() == 14.0);
        chk("Rectangle not square", !r.isSquare());
        r.scale(2.0);
        chk("Rectangle scale area", r.area() == 48.0);
        Rectangle sq(5.0, 5.0);
        chk("Rectangle isSquare", sq.isSquare());
    }

    cout << "\n" << pass << " / " << total << " passed\n";
    return pass == total ? 0 : 1;
}
