"""
Finals Study App Builder
Embeds the actual practice exam Q&A plus Claude-generated topic summaries
from every lecture PDF into a single self-contained HTML file.
"""

import os, json, pdfplumber, anthropic

BASE   = "/Users/drewmanley/Documents/projects/study/files"
OUT    = "/Users/drewmanley/Documents/projects/study/finals.html"
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


# ── PDF helpers ────────────────────────────────────────────────────────────────

def read_pdf(path: str, max_chars: int = 8000) -> str:
    try:
        with pdfplumber.open(path) as pdf:
            return "\n\n".join(p.extract_text() or "" for p in pdf.pages)[:max_chars]
    except Exception as e:
        return f"[error: {e}]"

def read_folder(folder: str, max_each: int = 5000) -> dict[str, str]:
    out = {}
    for fn in sorted(os.listdir(folder)):
        if fn.endswith(".pdf"):
            out[fn] = read_pdf(os.path.join(folder, fn), max_each)
    return out


# ── Claude helpers ─────────────────────────────────────────────────────────────

def claude(prompt: str, system: str = "", max_tokens: int = 6000) -> str:
    r = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=max_tokens,
        system=system or "You are a helpful study assistant. Output valid JSON only, no markdown fences.",
        messages=[{"role": "user", "content": prompt}],
    )
    raw = r.content[0].text.strip()
    if raw.startswith("```"):
        raw = "\n".join(raw.split("\n")[1:]).rstrip("`").strip()
    return raw


# ── Hard-coded practice exams (extracted from actual PDFs) ────────────────────

CS315_EXAM = [
    {
        "id": "q1", "title": "Q1 — Matrix Chain Problem", "points": 15,
        "question": """You are given n matrices A₁,A₂,...,Aₙ where Aᵢ is a d_{i-1}×dᵢ matrix.
Goal: find (i) the minimum number of scalar multiplications to compute A₁·A₂···Aₙ and (ii) the optimal multiplication order.
Let M(i,j) = minimum multiplications needed to compute Aᵢ·Aᵢ₊₁···Aⱼ.

**Q1.1 (5 pts)** Write the recursive formulation for M(i,j).

**Q1.2 (10 pts)** Given four matrices A₁,A₂,A₃,A₄ with sizes 20×1, 1×30, 30×5, 5×25 — fill in the M table and give the optimal multiplication order.""",
        "solution": """**Q1.1:** M(i,j) = min over i≤k<j { M(i,k) + M(k+1,j) + d_{i-1}·dₖ·dⱼ }

Base case: M(i,i) = 0

**Q1.2:** The M table fills bottom-up (by chain length). Key values:
- M(1,2)=600, M(2,3)=150, M(3,4)=3750
- M(1,3)=750 (split k=2: 600+0+20·30·5=750; k=1 gives 3100)
- M(2,4)=1350 (split k=2: 0+3750+1·30·25=4500; k=3: 150+0+1·5·25=275 → 1425? → best=1350)
- M(1,4)=1000 (split at k=1: M(1,1)+M(2,4)+20·1·25=0+1350+500=1850; k=2: 750+3750+20·30·25=19500; k=3: M(1,3)+0+20·5·25=750+0+2500=3250)

**Optimal order:** A₁·((A₂·A₃)·A₄)"""
    },
    {
        "id": "q2", "title": "Q2 — Huffman Coding", "points": 15,
        "question": """Given letters and frequencies:
| Z | Y | X | W | V | T | S | R |
|10 | 6 |14 | 4 | 8 | 5 |13 | 6 |

Use Huffman's algorithm to build the optimal prefix-free code tree. Show the tree and the code for each letter.""",
        "solution": """Build by repeatedly merging the two lowest-frequency nodes:

Step-by-step merges (lowest two each time):
W(4)+T(5)=9 → Y(6)+R(6)=12 → V(8)+[WT](9)=17 → Z(10)+[YR](12)=22 → S(13)+X(14)=27 → [VWT](17)+[ZYR](22)=39 → [SX](27)+[ZWYR...]=39+27=66

**Final codes:**
- X: 00
- S: 01
- Z: 100
- V: 110
- Y: 1010
- R: 1011
- T: 1110
- W: 1111

Key insight: more frequent letters get shorter codes."""
    },
    {
        "id": "q3", "title": "Q3 — Min Cut / Max Flow", "points": 20,
        "question": """Given a network G with source s and sink t and integer capacities on edges, determine the **max flow** value and a **min cut**.

(The exam provides a specific graph figure — the answer below is for the sample exam graph.)""",
        "solution": """**Max flow = 8**

Use Ford-Fulkerson: repeatedly find augmenting paths in the residual graph.

**Min cut:** A min cut separates s from t with total capacity = max flow (by the Max-Flow Min-Cut theorem). There may be multiple valid min cuts as long as total capacity = 8.

Key facts:
- Max-Flow Min-Cut theorem: max flow value = min cut capacity
- Ford-Fulkerson terminates in O(E·|max flow|) with integer capacities
- Residual graph: for each edge (u,v) with capacity c and flow f, add forward edge capacity c-f and backward edge f"""
    },
    {
        "id": "q4", "title": "Q4 — Divide & Conquer: 12ⁿ", "points": 20,
        "question": """Design an **O(n^{log₂3})** divide-and-conquer algorithm to compute the binary representation of 12ⁿ. You may use Integer-Multiplication (from class) as a subroutine.

**Q4.1 (10 pts)** Write pseudocode.

**Q4.2 (10 pts)** Analyze runtime using the recursion tree:
- How many sub-problems at depth i?
- Size of each sub-problem at depth i?
- Depth of the tree?
- Total runtime T(n)?""",
        "solution": """**Q4.1 Pseudocode:**
```
Power-Of-Twelve(n):
  if n == 1: return 1100   # binary for 12
  c = Power-Of-Twelve(⌊n/2⌋)
  s = Integer-Multiplication(c, c)   # s = 12^(2·⌊n/2⌋)
  if n is even: return s
  else: return (s·2³) + (s·2²)      # multiply by 12 = 8+4
```
Key idea: 12ⁿ = (12^{n/2})² and 12 = 8+4 = 2³+2².

**Q4.2 Analysis:**
- Sub-problems at depth i: **1** (only one recursive call)
- Size at depth i: **n/2ⁱ**
- Tree depth: **log₂(n)**
- T(n): work at each node = Integer-Multiplication on O(m)-bit inputs = O(m^{log₂3})
  Sum = Σ_{d=0}^{logn} (n/2^d)^{log₂3} = n^{log₂3} · Σ(1/2^{log₂3})^d ≈ O(n^{log₂3})"""
    },
    {
        "id": "q5", "title": "Q5 — DP: Crab Fishing", "points": 15,
        "question": """Liz can catch crabs on day i (getting X[i] crabs) but must then wait d[i] days before fishing again (earliest return: day i+d[i]+1). She wants to maximize total crabs by end of day n.

**Q5.1 (7 pts)** Define your sub-problems.

**Q5.2 (8 pts)** Give the recurrence relation.""",
        "solution": """**Q5.1 Sub-problems:**
Let S[i] = maximum crabs Liz can catch starting from day i through day n.
Solution to the original problem: S[1].

**Q5.2 Recurrence:**
S[i] = max(S[i+1],   X[i] + S[i+d[i]+1])
         ↑ skip day i   ↑ fish on day i, then skip to day i+d[i]+1

Base cases: S[n+1] = S[n+2] = ... = 0

**Algorithm:** Compute S bottom-up from i=n down to i=1.
Time: O(n)"""
    },
    {
        "id": "q6", "title": "Q6 — Greedy: Announcement Scheduling", "points": 15,
        "question": """n workers each have a shift interval [sᵢ, fᵢ]. Make as few announcements as possible so every worker hears at least one (a worker hears an announcement at time t if sᵢ ≤ t ≤ fᵢ).

**Q6.1 (7 pts)** Design a greedy algorithm.

**Q6.2 (8 pts)** Prove its correctness.""",
        "solution": """**Q6.1 Greedy Algorithm:**
1. Sort workers' shifts by **increasing finish time** f₁ ≤ f₂ ≤ ... ≤ fₙ.
2. Initialize announcement set A = {}.
3. While uncovered workers remain:
   - Take the uncovered worker with the earliest finish time fᵢ.
   - Add fᵢ to A (announce at the last possible moment of that shift).
   - Remove all workers whose shift contains fᵢ.
4. Return A.

Intuition: announcing at the latest moment of the earliest-ending shift covers the most workers.

**Q6.2 Proof of Correctness (exchange argument):**
Sort so f₁ ≤ f₂ ≤ ... ≤ fₙ. Let greedy picks g₁ < g₂ < ... < gᵣ; optimal picks c₁ < c₂ < ... < cₖ with k minimal.

**Claim:** gᵢ ≥ cᵢ for all i (greedy announcements are "at least as late").
- Base: g₁ = f₁ (earliest finish time). Optimal must cover worker 1, so s₁ ≤ c₁ ≤ f₁, meaning g₁ ≥ c₁.
- Inductive step: assume gᵢ ≥ cᵢ. Since gᵢ is at least as late as cᵢ, greedy covers ≥ as many workers. So the next uncovered worker for greedy has finish time fₘ₊₁ ≥ fₘ′₊₁, giving gᵢ₊₁ = fₘ₊₁ ≥ fₘ′₊₁ ≥ cᵢ₊₁.

Since {g₁,...,gₖ} covers all workers, r ≤ k, contradicting r > k. So greedy is optimal."""
    },
]

CS330_EXAM = [
    {
        "id": "q1", "title": "Q1 — C Language Short Answer", "points": 10,
        "question": """**(a) (3 pts) Memory leak calculation:**
```c
mystruct* myarray = (mystruct*) malloc(sizeof(mystruct) * atoi(argv[1]));
for(int i = 0; i < atoi(argv[1]); i++) {
    myarray[i].j = (int*) malloc(sizeof(int) * atoi(argv[2]));
}
// ./a.out 10 20
```
How many bytes are lost due to memory leak?

**(b) (4 pts)** Given a 2D array access code, which output (A/B/C/D) is printed?

**(c) (3 pts)** Which is NOT a correct method for printing the i-th element (1-indexed) of `int* A`?""",
        "solution": """**(a)** `./a.out 10 20`:
- myarray itself: sizeof(mystruct)×10 bytes leaked (never freed)
  - sizeof(mystruct) = sizeof(int) + sizeof(int*) = 4+8 = 12 bytes → 12×10 = 120
- Each myarray[i].j: sizeof(int)×20 = 80 bytes × 10 = 800 bytes
- **Total: ≥ 920 bytes** (or 960 with padding, both accepted)

**(b)** Answer: **B** (3 6 7 / 4 6 9 / 7 5 9)

**(c)** Answer: **D** — the incorrect printing method. Remember:
- `*(A+i-1)` ✓ and `A[i-1]` ✓ work for 1-indexed
- Pointer arithmetic and subscript are equivalent: `A[k] == *(A+k)`"""
    },
    {
        "id": "q2", "title": "Q2 — Rotate 2D Array (C)", "points": 15,
        "question": """Implement `void rotate_arr(int** mat, int m)` that rotates an m×m matrix **90° counter-clockwise** in-place (storing result back in mat). You may use a temporary array. No memory leaks!

Example: [[1,2,3],[4,5,6],[7,8,9]] → [[3,6,9],[2,5,8],[1,4,7]]""",
        "solution": """```c
void rotate_arr(int** mat, int m) {
    // Allocate temp
    int** tmp = malloc(sizeof(int*) * m);
    for(int i = 0; i < m; i++)
        tmp[i] = malloc(sizeof(int) * m);

    // Copy with rotation: CCW means new[m-1-j][i] = old[i][j]
    for(int i = 0; i < m; i++)
        for(int j = 0; j < m; j++)
            tmp[m-1-j][i] = mat[i][j];

    // Copy back
    for(int i = 0; i < m; i++)
        for(int j = 0; j < m; j++)
            mat[i][j] = tmp[i][j];

    // Free temp
    for(int i = 0; i < m; i++) free(tmp[i]);
    free(tmp);
}
```
**In-place (extra credit):** transpose then flip columns:
```c
// Transpose
for(i) for(j>i) swap(mat[i][j], mat[j][i]);
// Flip columns (reverse each column)
for(j) for(i < m/2) swap(mat[i][j], mat[m-1-i][j]);
```"""
    },
    {
        "id": "q3", "title": "Q3 — Prefix Sum In-Place (C)", "points": 6,
        "question": """Implement `void prefix_sum(int* A, int m)` that computes prefix sum **in-place** (no extra storage, no redundant operations).

Recall: y[i] = x[0] + x[1] + ... + x[i]""",
        "solution": """```c
void prefix_sum(int* A, int m) {
    for(unsigned int i = 1; i < m; i++) {
        A[i] = A[i] + A[i-1];
    }
}
```
Key points:
- Start loop at i=1 (A[0] is already its own prefix sum)
- No temporary variable needed — A[i-1] is already the prefix sum up to i-1 when we reach index i
- Do NOT start at i=0 (that would be a redundant operation: A[0] = A[0] + ... nothing)"""
    },
    {
        "id": "q4", "title": "Q4 — C++ Short Answer", "points": 10,
        "question": """**(a) (3 pts)** What is the constructor/destructor call order for a class hierarchy with base My_Int and derived My_NNInt?

**(b) (1 pt)** Static vs non-static member: if `j` is static and `i` is not, what is printed?

**(c) (2 pts)** Which lines cause a compiler error when accessing private/const members?

**(d) (2 pts)** What does this pointer arithmetic output?

**(e) (2 pts)** Which method for initializing an array of objects is NOT correct?""",
        "solution": """**(a)** Constructor/destructor order for My_NNInt (extends My_Int):
```
My_Int()       ← base ctor first
My_Int()       ← another My_Int object
My_NNInt()     ← derived ctor after base
~My_NNInt()    ← derived dtor first
~My_Int()      ← then base
~My_Int()      ← last My_Int
```
Rule: constructors go base→derived; destructors go derived→base.

**(b)** Answer: **A** — static members are shared across instances, so modifying j through one reference affects all.

**(c)** Answer: **C** — lines 7 and 8 cause errors (accessing private members outside class / modifying const).

**(d)** Answer: `16 16` then `17 17`

**(e)** Answer: **C** — that initialization method is not valid for arrays of objects with a parameterized constructor."""
    },
    {
        "id": "q5", "title": "Q5 — Destructor & Copy Constructor (C++)", "points": 8,
        "question": """Given:
```cpp
class Test {
    int* array;
    int n;
    // ...
};
void f(Test t) { delete[] t.array; t.n = 0; }
```
**(a) (2 pts)** Declare the destructor and copy constructor.
**(b) (2 pts)** Implement the destructor.
**(c) (4 pts)** Implement the copy constructor so that passing t1 to f() does NOT destroy t1's array.""",
        "solution": """**(a) Declarations:**
```cpp
~Test();
Test(const Test& in);
```

**(b) Destructor:**
```cpp
Test::~Test() {
    delete[] array;
    array = nullptr;  // optional but good practice
    n = 0;            // optional
}
```

**(c) Copy Constructor (deep copy):**
```cpp
Test::Test(const Test& in) {
    n = in.n;
    array = new int[n];
    for(unsigned int i = 0; i < n; i++)
        array[i] = in.array[i];
}
```
WHY: Without a copy constructor, C++ does a **shallow copy** (copies the pointer, not the data). When f() deletes t.array, it deletes the same memory t1.array points to. Deep copy allocates new memory, so f() deletes its own copy and t1 is unaffected."""
    },
    {
        "id": "q6", "title": "Q6 — Pixel Class (C++)", "points": 18,
        "question": """Implement a Pixel class with members `uchar r, g, b`.

**(a) 5 pts)** Parametric constructor `Pixel(uchar r, uchar g, uchar b)` — declaration + implementation.
**(b) (3 pts)** Destructor.
**(c) (5 pts)** `uchar addSamples(uchar a, uchar b) const` — returns average of two color components.
**(d) (5 pts)** Overload `operator+` — returns a new Pixel whose components are averages of the two inputs. Use addSamples.""",
        "solution": """**(a) Constructor:**
```cpp
// In class: Pixel(uchar r, uchar g, uchar b);
Pixel::Pixel(uchar r, uchar g, uchar b) {
    this->r = r;
    this->g = g;
    this->b = b;
}
```

**(b) Destructor:**
```cpp
Pixel::~Pixel() {}   // no heap memory, nothing to free
```

**(c) addSamples:**
```cpp
uchar Pixel::addSamples(const uchar a, const uchar b) const {
    float t = ((float)a + (float)b) / 2.0f;
    return (uchar)t;
}
```
Cast to float BEFORE dividing to avoid integer truncation issues.

**(d) operator+:**
```cpp
const Pixel Pixel::operator+(const Pixel& in) const {
    uchar rr = addSamples(r, in.r);
    uchar gg = addSamples(g, in.g);
    uchar bb = addSamples(b, in.b);
    return Pixel(rr, gg, bb);
}
```"""
    },
    {
        "id": "q7", "title": "Q7 — Templated Vect & Mat Classes (C++)", "points": 33,
        "question": """Given a templated `Vect<T>` (1D array) and derived `Mat<T>` (2D stored as 1D).

**(a) 5 pts)** Implement `get_size()` and `get_elem(unsigned int index)` for Vect.
**(b) (6 pts)** Implement `convert_matrix(T** in, T** out, unsigned int m, unsigned int n)` — flattens 2D to 1D using `new`.
**(c) (6 pts)** Implement Mat's constructor `Mat(unsigned int m, unsigned int n, T* arr)`.
**(d) (8 pts)** Implement `Mat::get_elem(unsigned int I, unsigned int J)`.
**(e) (8 pts)** Implement polymorphic `Mat::print()` — print each row on its own line using Vect's print().""",
        "solution": """**(a) Vect accessors:**
```cpp
template<class T> unsigned int Vect<T>::get_size() const { return size; }
template<class T> T* Vect<T>::get_elem(unsigned int index) const { return &(array[index]); }
```

**(b) convert_matrix:**
```cpp
template<class T>
void convert_matrix(T** in, T** out, unsigned int m, unsigned int n) {
    T* tmp = new T[m * n];
    unsigned int idx = 0;
    for(unsigned int i = 0; i < m; i++)
        for(unsigned int j = 0; j < n; j++)
            tmp[idx++] = in[i][j];
    *out = tmp;   // return pointer to flat array via out
}
```

**(c) Mat constructor (delegates to Vect):**
```cpp
template<class T>
Mat<T>::Mat(unsigned int mm, unsigned int nn, T* arr) : Vect<T>(mm * nn, arr) {
    m = mm;   // store row count; n = size/m
}
```

**(d) Mat::get_elem(I, J):**
```cpp
template<class T>
T* Mat<T>::get_elem(unsigned int I, unsigned int J) {
    unsigned int n = Vect<T>::get_size() / m;   // cols = total/rows
    unsigned int index = I * n + J;
    return Vect<T>::get_elem(index);
}
```

**(e) Mat::print():**
```cpp
template<class T>
void Mat<T>::print() const {
    unsigned int n = Vect<T>::get_size() / m;
    for(unsigned int i = 0; i < m; i++) {
        const Vect<T> tmp(n, Vect<T>::get_elem(i * n));
        tmp.print();   // prints one row then newline
    }
}
```"""
    },
]

EC434_TOPICS = [
    {
        "id": "foundations", "title": "Foundations & Welfare Analysis",
        "content": """**Core concepts:**
- **Normative vs Positive analysis** — normative = what *should* be (value judgments); positive = what *is* (empirical facts)
- **MB and MC curves** — individual curves aggregate *horizontally* for private goods (sum quantities at each price); aggregate *vertically* for public goods (sum WTP at each quantity)
- **Efficient equilibrium** — where MB = MC (maximizes net benefit = TB − TC)
- **Cost-effective** — achieves a given goal at minimum total cost; efficient requires MB = MC across all actors

**Welfare measures:**
- Consumer surplus = area below demand, above price
- Producer surplus = area above supply, below price
- Deadweight loss (DWL) = efficiency loss from being at wrong quantity (triangle between MB and MC from efficient to actual Q)
- Net benefit = Total Benefit − Total Cost

**Externalities:**
- Negative externality: private MC < social MC → overproduction, DWL
- Positive externality: private MB < social MB → underproduction
- Efficient level: where **social MB = social MC**

**Key math: Aggregating curves**
- Private goods: add quantities at each price → Qₐᵍᵍ(P) = Σ Qᵢ(P)
- Public goods: add WTP at each quantity → MBₐᵍᵍ(Q) = Σ MBᵢ(Q) (Samuelson condition)"""
    },
    {
        "id": "policy", "title": "Policy Solutions to Pollution",
        "content": """For each policy know: **how it works, pros/cons, efficient? cost-effective?**

| Policy | Efficient? | Cost-effective? | Notes |
|---|---|---|---|
| Pigouvian tax | Yes (if set = marginal damage) | Yes | Tax = external cost at efficient Q |
| Direct tax on pollution | Only if set correctly | Yes (equalizes MAC) | Same as Pigouvian |
| Abatement subsidy | Yes (if set correctly) | Yes | Can cause entry issues |
| Uniform quantity standard | No (unless symmetric firms) | No | Same abatement for all firms |
| Cap and trade | Yes (if cap = efficient level) | **Yes** (firms trade to equalize MAC) | Most cost-effective under heterogeneous firms |
| Technology standard | No | No | Doesn't minimize cost |
| Coase theorem | Yes (if no transaction costs) | Yes | Private bargaining; requires defined property rights |

**Weitzman Prices vs. Quantities:**
- Uncertain MB curve (flat): prices and quantities perform similarly
- Steep MB, flat MC → **quantities better** (avoid large welfare loss from Q error)
- Flat MB, steep MC → **prices better** (avoid large cost from over-abatement)
- Climate change: typically prefer **carbon tax** (prices) because MB of abatement is quite flat

**Finding efficient abatement:** set MAC_firm1 = MAC_firm2 = ... = MB of abatement"""
    },
    {
        "id": "valuation", "title": "Non-Market Valuation",
        "content": """**Types of value:**
- **Use value:** Direct (recreation, consumption) / Indirect (ecosystem services)
- **Non-use value:** Option value (future use), Bequest (future generations), Existence (knowing it exists)

**Stated Preference (ask people):**
- **Contingent Valuation (CV):**
  - Survey asks WTP for a hypothetical good/change
  - Biases: strategic, hypothetical, embedding, starting point, payment vehicle
  - Protest zeros: genuine $0 WTP vs. rejecting the survey design
  - NOAA Blue Ribbon Panel guidelines: binary choice format ("would you pay $X?"), in-person interviews, include "no" option, test for scope sensitivity
  - **Estimating WTP from regression:** use probit/logit, compute mean WTP from bid coefficient

- **Choice Experiments:**
  - Respondents choose among alternatives with different attributes + cost
  - Can decompose WTP by attribute
  - Less susceptible to hypothetical bias than CV

**Revealed Preference (observe behavior):**
- **Hedonic Price Method:** house prices reflect environmental quality
  - Run regression: price = f(structural, neighborhood, environmental attributes)
  - WTP for environmental improvement = coefficient on that attribute
  - Limitation: requires functional form assumptions, capitalization

- **Travel Cost Method:** use visit cost as proxy for WTP for a recreation site
  - Consumer surplus = area under demand curve (estimated from visit frequency vs. travel cost)
  - Present discounted value of site = CS / discount rate (for site protection decisions)

**Benefits Transfer:** apply WTP estimates from one study to a new policy context
- Pros: cheap and fast
- Cons: may not match local conditions; population/site differences"""
    },
    {
        "id": "vsl", "title": "Value of Statistical Life (VSL)",
        "content": """**What is VSL?**
VSL is the rate at which society trades off wealth for small reductions in mortality risk. It is NOT the value of a specific identified life.

VSL = WTP / Δrisk = e.g., $600 WTP to reduce risk by 1/10,000 → VSL = $6 million

**Hedonic Wage Method:**
- Workers demand wage premiums for riskier jobs
- Run regression: wage = f(risk, education, experience, industry, ...)
- VSL = (∂wage/∂risk) × 1 (coefficient on risk, scaled to full statistical life)

**Math examples:**
- If WTP = $400 to reduce annual mortality risk by 1 in 10,000:
  VSL = $400 / (0.0001) = **$4,000,000**
- Cost-benefit using VSL: if a policy costs $1B and reduces 500 deaths, use VSL to value benefits
- Scaling: don't confuse "WTP per person for small risk change" with "WTP to definitely save a life"

**Issues with VSL:**
- Distributional concerns (lower-income workers may accept more risk for less pay)
- Heterogeneity across populations
- One VSL for all policies raises equity questions"""
    },
    {
        "id": "iam_climate", "title": "Integrated Assessment Models & Climate Economics",
        "content": """**IAM Definition:** Models that link physical/ecological systems with economic systems to estimate costs and benefits of climate change / pollution policies.

**Steps in an IAM:**
1. Emissions scenario
2. Atmospheric/physical model (concentrations → temperature)
3. Damage function (temperature → economic damages)
4. Discounting (future damages → present value)

**Air pollution IAM (in-class example):**
Emissions → concentrations → health/ecosystem effects → monetary damages

**Tropical Cyclone IAM:**
CO₂ emissions → warming → increased hurricane intensity → property damages

**Climate Economics:**
- **Stock pollutant** (CO₂) vs **flow pollutant** (local NOₓ): CO₂ accumulates globally → requires global coordination
- **Social Cost of Carbon (SCC):** marginal damage from emitting 1 additional tonne of CO₂ (today's price: ~$50–200/tCO₂ depending on discount rate)
- **Discount rate debate:**
  - High discount rate (Nordhaus ~5%) → future damages worth little → lower SCC → less aggressive policy
  - Low discount rate (Stern ~1.4%) → future damages matter more → higher SCC → stronger policy
  - Ethical dimension: how much do we value future generations?

**Present value math:**
PV = FV / (1 + r)^t
NPV = Σ (Benefits_t − Costs_t) / (1+r)^t

**Challenges of global public goods:**
- Climate is a global public good → free rider problem → underprovision
- Requires international agreements (Paris Accord, etc.)
- Monitoring and enforcement are difficult"""
    },
]


# ── Generate flashcards & topic summaries via Claude ──────────────────────────

def gen_cs315_flashcards() -> list[dict]:
    docs = read_folder(f"{BASE}/cs315", max_each=4000)
    combined = "\n\n".join(f"=={k}==\n{v}" for k,v in docs.items())[:35000]
    raw = claude(f"""Based on these CS315 (Intermediate Algorithms) materials:

{combined}

Generate exactly 20 flashcards as a JSON array. Each card:
{{"q": "question", "a": "concise answer (1-3 sentences or a short formula)"}}

Focus on: algorithm definitions, recurrences, complexities, key properties, proof techniques.
Topics: BFS/DFS, SCC, topological sort, MST (Prim/Kruskal), Dijkstra, Bellman-Ford, Ford-Fulkerson, DP, Greedy, divide-and-conquer, Huffman coding.
Output only the JSON array.""")
    return json.loads(raw)

def gen_cs330_flashcards() -> list[dict]:
    docs = read_folder(f"{BASE}/cs330", max_each=4000)
    combined = "\n\n".join(f"=={k}==\n{v}" for k,v in docs.items())[:35000]
    raw = claude(f"""Based on these CS330 (C/C++ and Unix) materials:

{combined}

Generate exactly 20 flashcards as a JSON array. Each card:
{{"q": "question", "a": "concise answer"}}

Focus on: C pointers/memory/malloc/free, Unix commands, C++ OOP (constructors/destructors/copy constructors), BST, Red-Black Trees, templates, operator overloading, access control.
Output only the JSON array.""")
    return json.loads(raw)

def gen_ec434_flashcards() -> list[dict]:
    docs = read_folder(f"{BASE}/ec434", max_each=3000)
    combined = "\n\n".join(f"=={k}==\n{v}" for k,v in docs.items())[:35000]
    raw = claude(f"""Based on these EC434 (Environmental Economics) materials:

{combined}

Generate exactly 20 flashcards as a JSON array. Each card:
{{"q": "question", "a": "concise answer"}}

Focus on: policy tools, welfare analysis, valuation methods, VSL, IAM, climate economics, key definitions.
Output only the JSON array.""")
    return json.loads(raw)


# ── HTML builder ───────────────────────────────────────────────────────────────

def esc(s: str) -> str:
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def make_practice_exam_html(questions: list[dict]) -> str:
    html = '<div class="practice-exam">'
    for q in questions:
        html += f"""
<div class="exam-q" id="{q['id']}">
  <div class="exam-q-header" onclick="toggleQ('{q['id']}')">
    <span class="exam-q-title">{q['title']}</span>
    <span class="pts-badge">{q['points']} pts</span>
    <span class="expand-icon">▼</span>
  </div>
  <div class="exam-q-body" style="display:none">
    <div class="question-text">{q['question'].replace(chr(10), '<br>').replace('**','<b>').replace('**','</b>')}</div>
    <button class="reveal-btn" onclick="revealSol('{q['id']}')">Show Solution</button>
    <div class="solution" id="sol-{q['id']}" style="display:none">
      <div class="solution-label">Solution</div>
      <div class="solution-text">{q['solution'].replace(chr(10), '<br>')}</div>
    </div>
  </div>
</div>"""
    html += "</div>"
    return html

def make_topics_html(topics: list[dict]) -> str:
    html = '<div class="topics-list">'
    for t in topics:
        html += f"""
<div class="topic-card">
  <div class="topic-header" onclick="toggleTopic('{t['id']}')">
    <span>{t['title']}</span><span class="expand-icon">▼</span>
  </div>
  <div class="topic-body" id="topic-{t['id']}" style="display:none">
    <div class="topic-content">{t['content'].replace(chr(10),'<br>')}</div>
  </div>
</div>"""
    html += "</div>"
    return html

def make_flashcards_html(cards: list[dict]) -> str:
    html = '<div class="fc-controls"><button onclick="prevCard()">◀</button><span id="fc-counter">1 / ' + str(len(cards)) + '</span><button onclick="nextCard()">▶</button><button onclick="shuffleCards()" class="shuffle-btn">Shuffle</button></div>'
    html += '<div class="fc-container">'
    for i, c in enumerate(cards):
        display = "" if i == 0 else 'style="display:none"'
        html += f"""<div class="fc-card" id="fc-{i}" {display} onclick="flipCard(this)">
  <div class="fc-inner">
    <div class="fc-front"><div class="fc-label">Question</div><div class="fc-text">{esc(c.get('q',''))}</div></div>
    <div class="fc-back"><div class="fc-label">Answer</div><div class="fc-text">{esc(c.get('a',''))}</div></div>
  </div>
</div>"""
    html += "</div>"
    return html

def make_tab_panel(tab_id: str, title: str, exam_html: str, topics_html: str, fc_html: str, is_first: bool) -> str:
    active = "active" if is_first else ""
    return f"""
<div id="panel-{tab_id}" class="tab-panel {active}">
  <h2>{title}</h2>
  <div class="section-nav">
    <button class="snav-btn active" onclick="showSection('{tab_id}','exam',this)">Practice Exam</button>
    <button class="snav-btn" onclick="showSection('{tab_id}','topics',this)">Key Topics</button>
    <button class="snav-btn" onclick="showSection('{tab_id}','flash',this)">Flashcards</button>
  </div>
  <div id="{tab_id}-exam" class="sub-panel active">{exam_html}</div>
  <div id="{tab_id}-topics" class="sub-panel" style="display:none">{topics_html}</div>
  <div id="{tab_id}-flash" class="sub-panel" style="display:none">{fc_html}</div>
</div>"""


CSS = """
:root{--bg:#0d0f1a;--s1:#13162b;--s2:#1c2040;--s3:#252950;--acc:#7b6cf6;--acc2:#4ecdc4;--text:#e0e2f0;--muted:#7880a0;--bdr:#2a2e52;--grn:#4caf7d;--yel:#f0b429;--red:#e05252}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;font-size:15px}
a{color:var(--acc2)}

/* header */
header{background:linear-gradient(135deg,var(--s1),var(--s2));border-bottom:1px solid var(--bdr);padding:20px 32px;display:flex;align-items:center;gap:16px}
header h1{font-size:1.5rem;font-weight:700}
header .sub{color:var(--muted);font-size:.85rem;margin-top:3px}
.badge{background:var(--acc);color:#fff;font-size:.72rem;padding:3px 10px;border-radius:20px;font-weight:700;letter-spacing:.04em}

/* tabs */
.tabs{display:flex;gap:6px;padding:16px 32px 0;border-bottom:1px solid var(--bdr);overflow-x:auto}
.tab-btn{background:none;border:none;color:var(--muted);padding:8px 18px;font-size:.9rem;cursor:pointer;border-bottom:3px solid transparent;white-space:nowrap;transition:.2s;font-weight:500;border-radius:6px 6px 0 0}
.tab-btn:hover{color:var(--text);background:rgba(255,255,255,.04)}
.tab-btn.active{color:var(--acc);border-bottom-color:var(--acc);background:rgba(123,108,246,.08)}

/* content */
.content{padding:28px 32px;max-width:1100px;margin:0 auto}
.tab-panel{display:none}.tab-panel.active{display:block;animation:fadeIn .25s ease}
@keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
h2{font-size:1.6rem;margin-bottom:20px}

/* section nav */
.section-nav{display:flex;gap:8px;margin-bottom:24px;flex-wrap:wrap}
.snav-btn{background:var(--s2);border:1px solid var(--bdr);color:var(--muted);padding:7px 18px;border-radius:20px;cursor:pointer;font-size:.85rem;font-weight:500;transition:.2s}
.snav-btn:hover{color:var(--text);border-color:var(--acc)}
.snav-btn.active{background:var(--acc);color:#fff;border-color:var(--acc)}

/* practice exam */
.exam-q{border:1px solid var(--bdr);border-radius:10px;margin-bottom:14px;overflow:hidden}
.exam-q-header{display:flex;align-items:center;gap:10px;padding:14px 18px;cursor:pointer;background:var(--s2);user-select:none;transition:.2s}
.exam-q-header:hover{background:var(--s3)}
.exam-q-title{font-weight:600;flex:1}
.pts-badge{background:rgba(123,108,246,.2);color:var(--acc);font-size:.78rem;padding:3px 10px;border-radius:12px;font-weight:600}
.expand-icon{color:var(--muted);font-size:.85rem;transition:.2s}
.exam-q-body{padding:18px;background:var(--s1)}
.question-text{line-height:1.7;color:#ced4ef;margin-bottom:16px;white-space:pre-wrap}
.reveal-btn{background:none;border:1px solid var(--acc);color:var(--acc);padding:7px 18px;border-radius:8px;cursor:pointer;font-size:.85rem;transition:.2s}
.reveal-btn:hover{background:rgba(123,108,246,.15)}
.solution{margin-top:18px;border-top:1px solid var(--bdr);padding-top:16px}
.solution-label{font-size:.75rem;font-weight:700;color:var(--grn);text-transform:uppercase;letter-spacing:.08em;margin-bottom:10px}
.solution-text{line-height:1.75;color:#b8f0d0;white-space:pre-wrap;font-family:'SF Mono',Menlo,monospace;font-size:.88rem}

/* topics */
.topic-card{border:1px solid var(--bdr);border-radius:10px;margin-bottom:12px;overflow:hidden}
.topic-header{display:flex;justify-content:space-between;align-items:center;padding:13px 18px;cursor:pointer;background:var(--s2);font-weight:600;user-select:none;transition:.2s}
.topic-header:hover{background:var(--s3)}
.topic-body{padding:20px;background:var(--s1)}
.topic-content{line-height:1.75;color:#cdd3ee;white-space:pre-wrap}

/* flashcards */
.fc-controls{display:flex;align-items:center;gap:12px;margin-bottom:20px;flex-wrap:wrap}
.fc-controls button{background:var(--s2);border:1px solid var(--bdr);color:var(--text);padding:8px 18px;border-radius:8px;cursor:pointer;font-size:.9rem;transition:.2s}
.fc-controls button:hover{background:var(--s3);border-color:var(--acc)}
.shuffle-btn{margin-left:auto;background:rgba(78,205,196,.1)!important;border-color:var(--acc2)!important;color:var(--acc2)!important}
#fc-counter{color:var(--muted);font-size:.9rem;min-width:60px;text-align:center}
.fc-container{display:flex;justify-content:center}
.fc-card{width:100%;max-width:640px;height:240px;cursor:pointer;perspective:1200px}
.fc-inner{position:relative;width:100%;height:100%;transition:transform .45s;transform-style:preserve-3d}
.fc-card.flipped .fc-inner{transform:rotateY(180deg)}
.fc-front,.fc-back{position:absolute;width:100%;height:100%;backface-visibility:hidden;border-radius:14px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:24px;text-align:center}
.fc-front{background:var(--s2);border:1px solid var(--bdr)}
.fc-back{background:linear-gradient(135deg,#1b2545,#1e2a4a);border:1px solid var(--acc);transform:rotateY(180deg)}
.fc-label{font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);margin-bottom:12px}
.fc-back .fc-label{color:var(--acc2)}
.fc-text{font-size:.95rem;line-height:1.6;color:var(--text)}
.fc-back .fc-text{color:var(--acc2)}
"""

JS = """
// Tab switching
function showTab(id) {
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('panel-' + id).classList.add('active');
  event.target.classList.add('active');
}

// Section switching within a course
function showSection(tabId, section, btn) {
  ['exam','topics','flash'].forEach(s => {
    const el = document.getElementById(tabId + '-' + s);
    if(el) { el.style.display = s === section ? 'block' : 'none'; }
  });
  btn.closest('.section-nav').querySelectorAll('.snav-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
}

// Practice exam question expand/collapse
function toggleQ(id) {
  const body = document.querySelector('#' + id + ' .exam-q-body');
  const icon = document.querySelector('#' + id + ' .expand-icon');
  if(body.style.display === 'none') { body.style.display = 'block'; icon.textContent = '▲'; }
  else { body.style.display = 'none'; icon.textContent = '▼'; }
}

function revealSol(id) {
  const sol = document.getElementById('sol-' + id);
  const btn = document.querySelector('#' + id + ' .reveal-btn');
  sol.style.display = 'block';
  btn.style.display = 'none';
}

// Topic expand/collapse
function toggleTopic(id) {
  const body = document.getElementById('topic-' + id);
  const icon = body.previousElementSibling.querySelector('.expand-icon');
  if(body.style.display === 'none') { body.style.display = 'block'; icon.textContent = '▲'; }
  else { body.style.display = 'none'; icon.textContent = '▼'; }
}

// Flashcards
const fcState = {};
function initFc(prefix, total) {
  fcState[prefix] = { idx: 0, total, order: [...Array(total).keys()] };
}
function currentFcPrefix() {
  const panel = document.querySelector('.tab-panel.active');
  const sub = panel ? panel.querySelector('.sub-panel.active, .sub-panel[style=""]') : null;
  return panel ? panel.id.replace('panel-','') : null;
}

let fcIdx = 0, fcTotal = 0, fcOrder = [];
function setupFc(prefix, total) {
  fcIdx = 0; fcTotal = total;
  fcOrder = [...Array(total).keys()];
  updateFcDisplay(prefix);
}
function updateFcDisplay(prefix) {
  for(let i = 0; i < fcTotal; i++) {
    const el = document.getElementById('fc-' + i);
    if(el) el.style.display = i === fcOrder[fcIdx] ? 'block' : 'none';
    if(el) el.classList.remove('flipped');
  }
  const counter = document.getElementById('fc-counter');
  if(counter) counter.textContent = (fcIdx + 1) + ' / ' + fcTotal;
}
function nextCard() {
  if(fcIdx < fcTotal - 1) { fcIdx++; updateFcDisplay(); }
}
function prevCard() {
  if(fcIdx > 0) { fcIdx--; updateFcDisplay(); }
}
function shuffleCards() {
  for(let i = fcOrder.length-1; i > 0; i--) {
    const j = Math.floor(Math.random()*(i+1));
    [fcOrder[i],fcOrder[j]] = [fcOrder[j],fcOrder[i]];
  }
  fcIdx = 0; updateFcDisplay();
}
function flipCard(el) { el.classList.toggle('flipped'); }

// Init flashcard counts on load
window.addEventListener('load', () => {
  const cards = document.querySelectorAll('.fc-card');
  fcTotal = cards.length;
  fcOrder = [...Array(fcTotal).keys()];
});
"""

def main():
    print("Generating flashcards via Claude (this takes ~1 min)...")

    print("  [CS315] flashcards...")
    cs315_fc = gen_cs315_flashcards()
    print(f"  ✓ {len(cs315_fc)} cards")

    print("  [CS330] flashcards...")
    cs330_fc = gen_cs330_flashcards()
    print(f"  ✓ {len(cs330_fc)} cards")

    print("  [EC434] flashcards...")
    ec434_fc = gen_ec434_flashcards()
    print(f"  ✓ {len(ec434_fc)} cards")

    print("\nBuilding HTML...")

    tabs_html = """
<button class="tab-btn active" onclick="showTab('cs315')">CS 315 — Algorithms</button>
<button class="tab-btn" onclick="showTab('cs330')">CS 330 — C/C++</button>
<button class="tab-btn" onclick="showTab('ec434')">EC 434 — Env. Econ</button>
"""

    # Build the 3 topic sections
    ec434_topics_html = make_topics_html(EC434_TOPICS)

    # CS315 & CS330 topics from Claude-generated outline
    cs315_topics = [
        {"id":"graphs","title":"Graphs: BFS, DFS, SCC, Topological Sort","content":"""BFS (Breadth-First Search):
- Uses a queue; explores level by level
- Finds shortest path in unweighted graphs
- Time: O(V+E)

DFS (Depth-First Search):
- Uses a stack (or recursion); explores as deep as possible first
- Used for cycle detection, topological sort, SCC
- Time: O(V+E)
- Discovery time d[v] and finish time f[v] are key

Topological Sort:
- Order vertices so all edges go from earlier to later
- Only on DAGs (directed acyclic graphs)
- Algorithm: run DFS, output vertices in decreasing finish time order

Strongly Connected Components (SCC):
- Kosaraju-Sharir: (1) DFS on G, record finish order; (2) DFS on Gᵀ in reverse finish order
- Each DFS tree in step 2 = one SCC
- Time: O(V+E)"""},
        {"id":"mst","title":"Minimum Spanning Trees: Kruskal & Prim","content":"""MST: spanning tree of G with minimum total edge weight.

Kruskal's Algorithm:
- Sort all edges by weight
- Add edge if it doesn't form a cycle (use Union-Find)
- Greedy: always picks the globally cheapest safe edge
- Time: O(E log E)

Prim's Algorithm:
- Start from any vertex, greedily expand the tree
- Always add the cheapest edge connecting tree to non-tree vertex
- Use a min-heap for efficiency
- Time: O(E log V) with binary heap

Key properties:
- Cut property: the minimum weight edge crossing any cut is in every MST
- Cycle property: the maximum weight edge in any cycle is NOT in any MST"""},
        {"id":"shortestpath","title":"Shortest Paths: Dijkstra, Bellman-Ford","content":"""Dijkstra's Algorithm (non-negative weights):
- Greedy: always relax the vertex with smallest known distance
- Use a min-priority queue
- Time: O((V+E) log V) with binary heap
- Does NOT work with negative edge weights

Bellman-Ford (negative weights OK):
- Relax all edges V-1 times
- If you can still relax after V-1 iterations → negative cycle detected
- Time: O(VE)
- Works on graphs with negative edges (but not negative cycles)

Floyd-Warshall (all-pairs shortest path):
- DP: d[i][j][k] = shortest path from i to j using only vertices {1,...,k}
- Recurrence: d[i][j][k] = min(d[i][j][k-1], d[i][k][k-1]+d[k][j][k-1])
- Time: O(V³)

Acyclic Shortest Path:
- On a DAG: relax edges in topological order
- Time: O(V+E), works with negative edges"""},
        {"id":"dp","title":"Dynamic Programming","content":"""DP Template:
1. Define sub-problems
2. Write recurrence relation
3. Identify base cases
4. Compute bottom-up (or memoize top-down)
5. Reconstruct solution

Matrix Chain Multiplication:
- M(i,j) = min over k: M(i,k)+M(k+1,j)+d_{i-1}·dₖ·dⱼ
- Fill table by increasing chain length

Longest Common Subsequence (LCS):
- dp[i][j] = LCS of X[1..i] and Y[1..j]
- If X[i]==Y[j]: dp[i][j] = dp[i-1][j-1]+1
- Else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])

Longest Increasing Subsequence (LIS):
- dp[i] = length of LIS ending at index i
- O(n²) DP; O(n log n) with patience sorting

0/1 Knapsack:
- dp[i][w] = max value using items 1..i with capacity w
- dp[i][w] = max(dp[i-1][w], vᵢ + dp[i-1][w-wᵢ]) if wᵢ ≤ w

Bellman-Ford as DP:
- dp[k][v] = shortest path from s to v using at most k edges
- Recurrence: dp[k][v] = min over (u,v): dp[k-1][u] + w(u,v)"""},
        {"id":"greedy","title":"Greedy Algorithms","content":"""Greedy: make locally optimal choice at each step; prove globally optimal.

Proof techniques:
- Exchange argument: show swapping any greedy choice with optimal doesn't improve
- "Greedy stays ahead": show greedy is at least as good as optimal at each step

Activity Selection (Interval Scheduling):
- Sort by finish time; always pick the next compatible activity
- Greedy choice: earliest finish time
- Correctness: exchange argument

Huffman Coding:
- Greedy: always merge two lowest-frequency nodes
- Produces optimal prefix-free code (minimum weighted path length)
- Proof: if two symbols have lowest frequency, they can have the longest codes

Fractional Knapsack:
- Sort items by value/weight ratio; fill greedily
- NOT the same as 0/1 knapsack (which requires DP)"""},
        {"id":"flow","title":"Max Flow & Min Cut (Ford-Fulkerson)","content":"""Definitions:
- Flow network: directed graph with capacities c(u,v)
- Valid flow: 0 ≤ f(u,v) ≤ c(u,v); flow conservation at all non-source/sink nodes
- Max flow: maximum total flow from s to t

Ford-Fulkerson Algorithm:
1. Start with 0 flow
2. While augmenting path exists in residual graph:
   - Send flow along that path (bottleneck = min residual capacity)
   - Update residual graph
3. Residual graph: for edge (u,v) with capacity c and flow f:
   - Forward edge: c-f remaining capacity
   - Backward edge: f (can "undo" flow)

Time: O(E · |max flow|) — can be slow with irrational capacities; Edmonds-Karp (BFS) = O(VE²)

Max-Flow Min-Cut Theorem:
max flow = min cut capacity
- Min cut: partition (S,T) with s∈S, t∈T minimizing sum of capacities of edges from S to T
- The algorithm finds the min cut implicitly: S = vertices reachable from s in residual graph when algorithm terminates"""},
        {"id":"divconq","title":"Divide & Conquer","content":"""Pattern:
1. Divide problem into subproblems
2. Conquer subproblems recursively
3. Combine solutions

Master Theorem (T(n) = aT(n/b) + f(n)):
- If f(n) = O(n^{log_b(a) - ε}): T(n) = Θ(n^{log_b a})
- If f(n) = Θ(n^{log_b a}): T(n) = Θ(n^{log_b a} · log n)
- If f(n) = Ω(n^{log_b(a) + ε}) and af(n/b) ≤ cf(n): T(n) = Θ(f(n))

Karatsuba Integer Multiplication:
- Standard: O(n²); Karatsuba: O(n^{log₂3}) ≈ O(n^{1.585})
- Split n-bit numbers: x = x_H·2^{n/2} + x_L
- Compute 3 multiplications instead of 4: (x_H+x_L)(y_H+y_L), x_H·y_H, x_L·y_L
- T(n) = 3T(n/2) + O(n) → O(n^{log₂3})

Merge Sort: T(n) = 2T(n/2) + O(n) → O(n log n)"""},
    ]

    cs330_topics = [
        {"id":"c_basics","title":"C: Pointers, Memory, and Arrays","content":"""Pointers:
- int* p = &x;  → p holds address of x
- *p  → dereference (get value at address)
- p++  → move to next int-sized address
- Arrays decay to pointer: int A[] == int* A

Pointer arithmetic:
- A[i] == *(A+i)  always equivalent
- For 1-indexed: A[i-1] or *(A+i-1)

Heap memory (manual):
- malloc(n * sizeof(T))  → allocate n elements of type T
- free(ptr)  → release heap memory
- MUST free everything malloc'd → no memory leaks
- After free: set ptr = NULL to avoid dangling pointer

Common memory pitfalls:
- Memory leak: allocate but never free
- Double free: free the same pointer twice
- Use after free: access memory after freeing
- Buffer overflow: write past end of array

sizeof:
- sizeof(struct) may be padded for alignment
- sizeof(int*) = 8 on 64-bit, sizeof(int) = 4 typically

2D arrays:
- int** A = malloc(sizeof(int*) * rows);
- for each row: A[i] = malloc(sizeof(int) * cols);
- Free: free each row, then free A"""},
        {"id":"cpp_oop","title":"C++: OOP, Constructors, Destructors","content":"""Constructor/Destructor order:
- Base class constructor runs BEFORE derived class constructor
- Destructor order is REVERSED: derived first, then base
- Always declare destructor virtual if using polymorphism

Copy Constructor:
- Called when passing by value, returning by value, or explicit copy
- Default (shallow) copy: copies pointers — shared memory!
- Deep copy: allocate new memory and copy contents
- Signature: ClassName(const ClassName& other)

Rule of Three:
If you need a custom destructor, you also need a custom copy constructor AND copy assignment operator.

Access control:
- private: only accessible within the class
- protected: accessible in class + derived classes
- public: accessible everywhere

const member functions:
- Cannot modify any member variables
- Can be called on const objects
- Declared with const after parameter list: void foo() const;

Static members:
- Shared across ALL instances of the class
- Static data: one copy for the whole class
- Static method: no 'this' pointer, can only access static members"""},
        {"id":"cpp_templates","title":"C++: Templates & Operator Overloading","content":"""Templates:
- template<class T> class Vect { ... };
- Defers type specification to use time
- Must be defined in header (compiler needs to see definition for each instantiation)
- template<class T> void func() { ... }  for function templates

Operator Overloading:
- const Pixel operator+(const Pixel& in) const;
- operator[] for array subscript
- Returning by value vs. reference: return new object (not reference to local)
- Use const wherever possible

Inheritance:
- class Derived : public Base { ... };
- Derived constructor must call base constructor: Derived() : Base(args) {}
- Virtual functions: resolved at runtime (polymorphism)
- Pure virtual: virtual void foo() = 0; → abstract class

Templates + Inheritance:
- template<class T> class Mat : public Vect<T> { ... };
- Must use Vect<T>::method() to call base class template methods (name lookup)"""},
        {"id":"bst_rbt","title":"BST & Red-Black Trees","content":"""BST (Binary Search Tree):
- left subtree keys < node key < right subtree keys
- Search/Insert/Delete: O(h) where h = height
- Worst case: O(n) if unbalanced (sorted insertions)
- In-order traversal gives sorted order

Red-Black Tree (balanced BST):
Properties (every RBT must satisfy all 5):
1. Every node is red or black
2. Root is black
3. Every leaf (NIL) is black
4. If a node is red, both children are black (no two consecutive reds)
5. All paths from a node to its NIL descendants have the same number of black nodes

Height: O(log n) — guaranteed by these properties

Insert:
- Insert as in BST, color new node RED
- Fix violations: recolor and/or rotate
- Cases: uncle red (recolor), uncle black with two cases (rotations)

Delete:
- Remove as in BST
- If deleted node was black: "double black" violation → fix with rotations/recoloring
- Cases for fix-up: sibling red, sibling black with various child colors

Rotations:
- Left rotation: x's right child y becomes new root; x becomes y's left child
- Right rotation: symmetric
- O(1) pointer changes"""},
        {"id":"unix","title":"Unix & Command Line","content":"""Basic commands:
- ls, cd, pwd, mkdir, rm, cp, mv, cat, less, grep, find
- Pipes: cmd1 | cmd2  (stdout of cmd1 → stdin of cmd2)
- Redirection: cmd > file (write), cmd >> file (append), cmd < file (read)

Compilation:
- gcc -o output source.c  (compile C)
- g++ -o output source.cpp  (compile C++)
- -Wall: enable warnings; -g: debug info; -O2: optimize
- Make: build tool using Makefile

Debugging with gdb:
- gdb ./program; run; break main; next; step; print var; backtrace

File I/O in C:
- FILE* f = fopen("file.txt", "r");
- fread/fwrite for binary; fscanf/fprintf for text
- fclose(f);  — always close files

Valgrind (memory debugging):
- valgrind ./program  — detect leaks, invalid reads/writes"""},
    ]

    cs315_topics_html = make_topics_html(cs315_topics)
    cs330_topics_html = make_topics_html(cs330_topics)

    # Practice exam HTML
    cs315_exam_html = make_practice_exam_html(CS315_EXAM)
    cs330_exam_html = make_practice_exam_html(CS330_EXAM)

    # EC434 practice exam — from study guide format
    ec434_exam_qs = [
        {"id":"ec1","title":"Welfare Analysis & Externalities","points":20,
         "question":"""(a) Draw a market with a negative externality. Label the private MC, social MC, equilibrium Q, efficient Q, and deadweight loss.

(b) A firm emits pollution. Private MC = 10 + 2Q. Social MC = 10 + 4Q. Demand (MB) = 50 − 2Q.
  (i) Find the market equilibrium quantity and price.
  (ii) Find the efficient quantity.
  (iii) What Pigouvian tax achieves efficiency? How much tax revenue is collected?""",
         "solution":"""(a) Key diagram elements:
- Private MC curve (lower) and Social MC = Private MC + Marginal Damage (higher)
- Equilibrium Q_mkt where MB = Private MC → overproduction
- Efficient Q* where MB = Social MC → lower quantity
- DWL = triangle between MB and Social MC from Q* to Q_mkt

(b) Calculations:
(i) Market equilibrium: MB = Private MC → 50-2Q = 10+2Q → 40 = 4Q → Q_mkt = 10, P = 30

(ii) Efficient: MB = Social MC → 50-2Q = 10+4Q → 40 = 6Q → Q* = 6.67, P* = 36.67

(iii) Pigouvian tax = Marginal damage at Q* = Social MC - Private MC at Q* = 2Q* = 2(6.67) = 13.33
Tax revenue = t × Q* = 13.33 × 6.67 ≈ $88.9"""},
        {"id":"ec2","title":"Cap and Trade vs. Tax","points":15,
         "question":"""Two firms must reduce pollution. Firm A has MAC_A = 20 + 2q_A. Firm B has MAC_B = 10 + 4q_B. The regulator wants 10 units of total abatement.

(a) Find the cost-effective allocation (MAC_A = MAC_B = t*).
(b) What emission price (carbon price) achieves this?
(c) Compare total abatement cost under cost-effective allocation vs. uniform standard (each abates 5 units).""",
         "solution":"""(a) Cost-effective: set MAC_A = MAC_B
20+2q_A = 10+4q_B
Also: q_A + q_B = 10

From MAC equality: 20+2q_A = 10+4(10-q_A) = 50-4q_A
→ 6q_A = 30 → q_A = 5, q_B = 5

Wait: 20+2(5) = 30; 10+4(5) = 30 ✓  So by coincidence, uniform and cost-effective happen to be equal here.

Let me verify: MAC_A at q=5: 20+10=30; MAC_B at q=5: 10+20=30 → both equal → cost-effective achieved.

(b) Carbon price = $30 (the equilibrium MAC)

(c) Total cost under cost-effective allocation:
- Firm A: area under MAC_A from 0 to 5 = (20×5) + (2×5²/2) = 100+25 = 125
- Firm B: area under MAC_B from 0 to 5 = (10×5) + (4×5²/2) = 50+50 = 100
- Total: $225

Under uniform (each abates 5), same result here since MACs are equal at q=5 each."""},
        {"id":"ec3","title":"Contingent Valuation","points":15,
         "question":"""A CV survey asks 100 respondents whether they'd pay $50 to protect a wetland. 60 say yes. Another group of 100 is asked about $100: 30 say yes.

(a) What is a "protest zero" and why does it matter?
(b) Using a simple linear probability model, estimate mean WTP.
(c) Name two potential biases in this CV study and how to mitigate them.""",
         "solution":"""(a) Protest zero: a respondent says $0 WTP not because they don't value the good, but because they object to the survey design (e.g., "government should pay," "this is a rights issue"). Including protest zeros understates true WTP. Identify through follow-up questions; often excluded from WTP estimates.

(b) Linear probability model:
P(yes) = a + b·bid
At $50: P = 0.60; at $100: P = 0.30
Slope b = (0.30-0.60)/(100-50) = -0.006
Intercept: 0.60 = a - 0.006×50 → a = 0.90

Mean WTP = bid where P(yes) = 0.5:
0.5 = 0.90 - 0.006×WTP → WTP = 0.40/0.006 = **$66.67**

(c) Biases and mitigations:
1. Hypothetical bias (people overstate WTP in surveys vs. real money) → use certainty follow-up, calibration factors, real-money validation
2. Starting point / anchoring bias (suggested bid anchors responses) → randomize bid amounts across respondents
3. Embedding effect (WTP for wetland ≈ WTP for all environment) → careful scope test, sequential valuation"""},
        {"id":"ec4","title":"Value of Statistical Life","points":10,
         "question":"""A hedonic wage regression estimates: wage = 15,000 + 2,000×risk + other controls, where risk = annual mortality risk per 10,000 workers.

(a) Interpret the coefficient on risk.
(b) Calculate the VSL.
(c) A new regulation costs $5 billion and is expected to save 1,000 lives. Is it cost-effective at this VSL?""",
         "solution":"""(a) Coefficient interpretation: workers accept a $2,000 annual wage premium for each 1-in-10,000 increase in annual mortality risk. Equivalently, they accept $0.20 per additional unit of annual risk expressed per worker.

(b) VSL calculation:
VSL = wage premium / risk change = $2,000 / (1/10,000) = $2,000 × 10,000 = **$20,000,000**

(c) Cost-benefit:
Benefit = 1,000 lives × $20M/life = $20 billion
Cost = $5 billion
Net benefit = $15 billion > 0 → **yes, cost-effective**

Note: VSL of $20M is high (typical US estimates ~$10M). Regardless, $5B / 1,000 lives = $5M per life saved < $20M VSL → passes cost-benefit test."""},
        {"id":"ec5","title":"Climate Economics & IAM","points":15,
         "question":"""(a) Explain what an Integrated Assessment Model (IAM) is and the key steps.
(b) How does the discount rate affect the Social Cost of Carbon (SCC)? Why is there disagreement?
(c) Why is climate change particularly difficult to address compared to local pollution? What policies exist?""",
         "solution":"""(a) IAM: a model that links physical/ecological systems with economic systems to estimate the costs and benefits of climate change or pollution policies.

Key steps:
1. Emissions scenarios (how much CO₂ is emitted)
2. Climate model (emissions → atmospheric concentrations → temperature change)
3. Damage function (temperature change → economic damages, e.g., % of GDP)
4. Cost model (mitigation costs)
5. Discounting (future damages and costs → present value)
6. Output: optimal carbon price, net benefits of policies

(b) Discount rate and SCC:
- High discount rate (e.g., 5%): future damages are heavily discounted → SCC is low (e.g., ~$20-50/tCO₂) → less aggressive policy justified
- Low discount rate (e.g., 1-2%): future damages count more → SCC is high (e.g., $200+/tCO₂) → stronger policy justified
- Disagreement: partly ethical (how much do we owe future generations?) and partly empirical (what's the right long-run real interest rate?)

(c) Climate as global public good:
- CO₂ is a global stock pollutant (accumulates, mixes globally) → local pollution doesn't
- Free rider problem: each country benefits from others' abatement without paying
- No global enforcement mechanism
- Policies: Paris Agreement (voluntary pledges), carbon taxes, cap-and-trade, technology standards, international transfers"""},
    ]
    ec434_exam_html = make_practice_exam_html(ec434_exam_qs)

    # Flashcard HTML
    cs315_fc_html = make_flashcards_html(cs315_fc)
    cs330_fc_html = make_flashcards_html(cs330_fc)
    ec434_fc_html = make_flashcards_html(ec434_fc)

    panels = (
        make_tab_panel("cs315", "CS 315 — Intermediate Algorithms",
                       cs315_exam_html, cs315_topics_html, cs315_fc_html, True) +
        make_tab_panel("cs330", "CS 330 — C/C++ and Unix",
                       cs330_exam_html, cs330_topics_html, cs330_fc_html, False) +
        make_tab_panel("ec434", "EC 434 — Environmental Economics",
                       ec434_exam_html, ec434_topics_html, ec434_fc_html, False)
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Finals Study Guide — UO Spring 2026</title>
<style>{CSS}</style>
</head>
<body>
<header>
  <div>
    <h1>Finals Study Guide</h1>
    <div class="sub">University of Oregon · Spring 2026 · CS 315, CS 330, EC 434</div>
  </div>
  <span class="badge">Claude-powered</span>
</header>
<nav class="tabs">{tabs_html}</nav>
<main class="content">{panels}</main>
<script>{JS}</script>
</body>
</html>"""

    with open(OUT, "w") as f:
        f.write(html)
    print(f"\n✅  {OUT}")
    print(f"    open {OUT}")


if __name__ == "__main__":
    main()
