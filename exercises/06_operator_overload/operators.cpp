/*
 * CS 330 — Exercise 6: Operator Overloading
 *
 * Topics: operator+, operator==, operator<<, operator[], operator*
 *         (unary and binary), const correctness.
 *
 * Build: g++ -Wall -g -o operators operators.cpp && ./operators
 */

#include <iostream>
#include <cmath>
using namespace std;

/* ── Exercise 6.1 ─────────────────────────────────────────────────────────────
 * Implement class Vec2 — a 2D vector.
 *
 * Members: double x, y  (public for simplicity)
 *
 * Overload:
 *   Vec2  operator+(const Vec2& b) const  — component-wise add
 *   Vec2  operator-(const Vec2& b) const  — component-wise subtract
 *   Vec2  operator*(double scalar) const  — scalar multiply
 *   bool  operator==(const Vec2& b) const — equal if both components match
 *   double dot(const Vec2& b) const       — dot product
 *   double magnitude() const              — sqrt(x*x + y*y)
 *
 * Also overload as FREE function (outside the class):
 *   friend ostream& operator<<(ostream& os, const Vec2& v)
 *     — prints "(x, y)" e.g. "(3.00, 4.00)"
 */
class Vec2 {
public:
    double x, y;

    Vec2(double x = 0, double y = 0) : x(x), y(y) {}

    Vec2 operator+(const Vec2& b) const {
        /* TODO */
        return Vec2{};
    }

    Vec2 operator-(const Vec2& b) const {
        /* TODO */
        return Vec2{};
    }

    Vec2 operator*(double scalar) const {
        /* TODO */
        return Vec2{};
    }

    bool operator==(const Vec2& b) const {
        /* TODO */
        return false;
    }

    double dot(const Vec2& b) const {
        /* TODO */
        return 0;
    }

    double magnitude() const {
        /* TODO */
        return 0;
    }

    friend ostream& operator<<(ostream& os, const Vec2& v) {
        /* TODO: print "(x, y)" with 2 decimal places */
        return os;
    }
};

/* ── Exercise 6.2 ─────────────────────────────────────────────────────────────
 * Implement class Pixel (from the CS 330 final exam).
 *
 * Members (private): unsigned char r, g, b
 *
 * Methods:
 *   Pixel(unsigned char r, unsigned char g, unsigned char b)
 *   ~Pixel()                    — no heap memory, empty body
 *
 *   unsigned char addSamples(unsigned char a, unsigned char b) const
 *     — returns average of a and b (cast to float to avoid truncation issues)
 *
 *   Pixel operator+(const Pixel& other) const
 *     — returns new Pixel with each channel = average of the two inputs
 *       Uses addSamples for each channel.
 *
 *   bool operator==(const Pixel& other) const
 *
 *   unsigned char getR() const, getG() const, getB() const
 */
class Pixel {
private:
    unsigned char r, g, b;

public:
    Pixel(unsigned char r, unsigned char g, unsigned char b) {
        /* TODO */
    }

    ~Pixel() { /* no heap memory */ }

    unsigned char addSamples(unsigned char a, unsigned char b) const {
        /* TODO: return (a + b) / 2, but cast carefully to avoid overflow */
        return 0;
    }

    Pixel operator+(const Pixel& other) const {
        /* TODO: use addSamples for each channel */
        return Pixel(0, 0, 0);
    }

    bool operator==(const Pixel& other) const {
        /* TODO */
        return false;
    }

    unsigned char getR() const { return r; }
    unsigned char getG() const { return g; }
    unsigned char getB() const { return b; }
};

/* ── Exercise 6.3 ─────────────────────────────────────────────────────────────
 * Implement class Matrix2x2 — a 2×2 matrix.
 *
 * Store as: double data[2][2]  (private)
 *
 * Methods:
 *   Matrix2x2(double a, double b, double c, double d)
 *     — fills [[a,b],[c,d]]
 *
 *   double& operator()(int i, int j)       — mutable access
 *   double  operator()(int i, int j) const — const access
 *
 *   Matrix2x2 operator+(const Matrix2x2& o) const  — element-wise add
 *   Matrix2x2 operator*(const Matrix2x2& o) const  — matrix multiply
 *   double det() const                              — determinant = ad - bc
 */
class Matrix2x2 {
private:
    double data[2][2];

public:
    Matrix2x2(double a, double b, double c, double d) {
        /* TODO */
    }

    double& operator()(int i, int j) {
        /* TODO */
        return data[0][0]; /* placeholder */
    }

    double operator()(int i, int j) const {
        /* TODO */
        return 0;
    }

    Matrix2x2 operator+(const Matrix2x2& o) const {
        /* TODO */
        return Matrix2x2(0,0,0,0);
    }

    Matrix2x2 operator*(const Matrix2x2& o) const {
        /* TODO: standard matrix multiply */
        return Matrix2x2(0,0,0,0);
    }

    double det() const {
        /* TODO: ad - bc */
        return 0;
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

    /* 6.1 Vec2 */
    Vec2 a(3, 4), b(1, 2);
    chk("Vec2 +", (a + b) == Vec2(4, 6));
    chk("Vec2 -", (a - b) == Vec2(2, 2));
    chk("Vec2 * scalar", (a * 2) == Vec2(6, 8));
    chk("Vec2 dot", a.dot(b) == 11.0);
    chk("Vec2 magnitude", abs(a.magnitude() - 5.0) < 1e-9);
    cout << "  Vec2 << : " << a << "\n";

    /* 6.2 Pixel */
    Pixel p1(100, 200, 50);
    Pixel p2(50, 100, 150);
    Pixel p3 = p1 + p2;
    chk("Pixel + R", p3.getR() == 75);
    chk("Pixel + G", p3.getG() == 150);
    chk("Pixel + B", p3.getB() == 100);
    chk("Pixel ==", p1 == Pixel(100, 200, 50));
    chk("Pixel != ", !(p1 == p2));

    /* 6.3 Matrix2x2 */
    Matrix2x2 m1(1,2,3,4);
    Matrix2x2 m2(5,6,7,8);
    chk("Matrix2x2 det", m1.det() == -2.0);   /* 1*4 - 2*3 = -2 */
    chk("Matrix2x2 (i,j)", m1(1,0) == 3.0);
    Matrix2x2 msum = m1 + m2;
    chk("Matrix2x2 + (0,0)", msum(0,0) == 6.0);
    Matrix2x2 mprod = m1 * m2;
    chk("Matrix2x2 * (0,0)", mprod(0,0) == 19.0);  /* 1*5+2*7 */
    chk("Matrix2x2 * (1,1)", mprod(1,1) == 50.0);  /* 3*6+4*8 */

    cout << "\n" << pass << " / " << total << " passed\n";
    return pass == total ? 0 : 1;
}
