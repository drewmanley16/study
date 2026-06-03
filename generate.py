"""
Canvas Study Tool Generator
Extracts content from downloaded PDFs and uses Claude to generate
a complete study guide with summaries, key concepts, and flashcards.
"""

import os
import json
import pdfplumber
import anthropic

BASE = "/Users/drewmanley/Documents/projects/study/files"
OUT = "/Users/drewmanley/Documents/projects/study/study_guide.html"
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def extract_pdf(path: str, max_chars: int = 12000) -> str:
    try:
        with pdfplumber.open(path) as pdf:
            text = "\n\n".join(
                page.extract_text() or "" for page in pdf.pages
            )
        return text[:max_chars]
    except Exception as e:
        return f"[Could not extract: {e}]"


def extract_all(folder: str, limit_per_file: int = 6000) -> dict[str, str]:
    docs = {}
    for fn in sorted(os.listdir(folder)):
        if fn.endswith(".pdf"):
            path = os.path.join(folder, fn)
            docs[fn] = extract_pdf(path, limit_per_file)
    return docs


def ask_claude(system: str, user: str) -> str:
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8096,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return msg.content[0].text


def generate_course_content(course_name: str, docs: dict[str, str]) -> dict:
    """Generate study guide and flashcards for a course."""
    # Build combined content
    combined = ""
    for name, text in docs.items():
        combined += f"\n\n=== {name} ===\n{text}"

    combined = combined[:40000]  # stay within context

    system = (
        "You are a study assistant helping a college student prepare for finals. "
        "Be concise, clear, and exam-focused. Use bullet points and numbered lists. "
        "Output valid JSON only."
    )

    prompt = f"""Course: {course_name}

Here are the course materials:
{combined}

Generate a JSON object with exactly these keys:
{{
  "summary": "2-3 paragraph overview of what this course covers and what matters for finals",
  "key_topics": [
    {{"topic": "topic name", "description": "1-2 sentence explanation", "exam_tip": "what to know for the exam"}}
  ],
  "flashcards": [
    {{"question": "...", "answer": "..."}}
  ],
  "common_mistakes": ["mistake 1", "mistake 2", ...],
  "study_checklist": ["item 1", "item 2", ...]
}}

Include exactly 16 flashcards covering the most important testable concepts.
Include exactly 10 key topics.
Keep all string values concise (under 120 chars each).
Focus on what would appear on a final exam.
IMPORTANT: Output ONLY valid JSON. No markdown, no explanation, no code fences."""

    raw = ask_claude(system, prompt)

    # strip markdown code fences if present
    raw = raw.strip()
    if raw.startswith("```"):
        raw = "\n".join(raw.split("\n")[1:])
        if raw.endswith("```"):
            raw = raw[:-3]

    return json.loads(raw)


def build_html(courses: dict[str, dict]) -> str:
    tabs_html = ""
    panels_html = ""

    for i, (name, data) in enumerate(courses.items()):
        active = "active" if i == 0 else ""
        short = name.replace(" ", "_").lower()

        tabs_html += f'<button class="tab-btn {active}" onclick="showTab(\'{short}\')">{name}</button>\n'

        # Build flashcards
        cards_html = ""
        for j, fc in enumerate(data.get("flashcards", [])):
            cards_html += f"""
        <div class="card" onclick="this.classList.toggle('flipped')">
          <div class="card-inner">
            <div class="card-front"><span>{fc['question']}</span></div>
            <div class="card-back"><span>{fc['answer']}</span></div>
          </div>
        </div>"""

        # Build key topics
        topics_html = ""
        for t in data.get("key_topics", []):
            topics_html += f"""
          <div class="topic-item">
            <strong>{t['topic']}</strong>
            <p>{t['description']}</p>
            <div class="exam-tip">📝 Exam tip: {t['exam_tip']}</div>
          </div>"""

        # Build checklist
        checklist_html = ""
        for item in data.get("study_checklist", []):
            checklist_html += f'<li><label><input type="checkbox"> {item}</label></li>\n'

        # Build common mistakes
        mistakes_html = ""
        for m in data.get("common_mistakes", []):
            mistakes_html += f"<li>{m}</li>\n"

        summary = data.get("summary", "").replace("\n", "<br>")

        panels_html += f"""
    <div id="panel-{short}" class="tab-panel {'active' if i==0 else ''}">
      <h2>{name}</h2>

      <section class="section summary-section">
        <h3>Course Overview</h3>
        <p>{summary}</p>
      </section>

      <section class="section">
        <h3>Key Topics</h3>
        <div class="topics-grid">
          {topics_html}
        </div>
      </section>

      <section class="section">
        <h3>Flashcards <small>(click to flip)</small></h3>
        <div class="cards-grid">
          {cards_html}
        </div>
      </section>

      <div class="two-col">
        <section class="section">
          <h3>Study Checklist</h3>
          <ul class="checklist">{checklist_html}</ul>
        </section>
        <section class="section">
          <h3>Common Mistakes to Avoid</h3>
          <ul class="mistakes">{mistakes_html}</ul>
        </section>
      </div>
    </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Finals Study Guide — University of Oregon</title>
<style>
  :root {{
    --bg: #0f1117;
    --surface: #1a1d2e;
    --surface2: #242740;
    --accent: #7c6af7;
    --accent2: #4ecdc4;
    --text: #e8e8f0;
    --muted: #8888aa;
    --border: #2e3050;
    --green: #4caf7d;
    --yellow: #f0b429;
    --red: #e05252;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }}

  header {{ background: linear-gradient(135deg, #1a1d2e 0%, #242740 100%); border-bottom: 1px solid var(--border); padding: 24px 32px; display: flex; align-items: center; gap: 16px; }}
  header h1 {{ font-size: 1.6rem; font-weight: 700; }}
  header .badge {{ background: var(--accent); color: white; font-size: 0.75rem; padding: 4px 10px; border-radius: 20px; font-weight: 600; }}
  header .sub {{ color: var(--muted); font-size: 0.9rem; margin-top: 4px; }}

  .tabs {{ display: flex; gap: 8px; padding: 20px 32px 0; border-bottom: 1px solid var(--border); overflow-x: auto; }}
  .tab-btn {{ background: none; border: none; color: var(--muted); padding: 10px 20px; font-size: 0.95rem; cursor: pointer; border-bottom: 3px solid transparent; white-space: nowrap; transition: all 0.2s; font-weight: 500; }}
  .tab-btn:hover {{ color: var(--text); }}
  .tab-btn.active {{ color: var(--accent); border-bottom-color: var(--accent); }}

  .content {{ padding: 32px; max-width: 1400px; margin: 0 auto; }}
  .tab-panel {{ display: none; }}
  .tab-panel.active {{ display: block; animation: fadeIn 0.3s ease; }}
  @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: translateY(0); }} }}

  h2 {{ font-size: 1.8rem; margin-bottom: 24px; color: var(--text); }}
  h3 {{ font-size: 1.1rem; font-weight: 600; margin-bottom: 16px; color: var(--accent2); text-transform: uppercase; letter-spacing: 0.05em; }}
  h3 small {{ text-transform: none; font-weight: 400; color: var(--muted); letter-spacing: 0; font-size: 0.85rem; }}

  .section {{ background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 24px; margin-bottom: 24px; }}
  .summary-section p {{ line-height: 1.7; color: #ccd; }}

  .topics-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }}
  .topic-item {{ background: var(--surface2); border-radius: 8px; padding: 16px; border-left: 3px solid var(--accent); }}
  .topic-item strong {{ display: block; margin-bottom: 6px; color: var(--text); }}
  .topic-item p {{ font-size: 0.9rem; color: var(--muted); line-height: 1.5; margin-bottom: 8px; }}
  .exam-tip {{ font-size: 0.82rem; color: var(--yellow); background: rgba(240,180,41,0.08); padding: 6px 10px; border-radius: 6px; }}

  .cards-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; }}
  .card {{ height: 160px; cursor: pointer; perspective: 1000px; }}
  .card-inner {{ position: relative; width: 100%; height: 100%; transition: transform 0.5s; transform-style: preserve-3d; }}
  .card.flipped .card-inner {{ transform: rotateY(180deg); }}
  .card-front, .card-back {{ position: absolute; width: 100%; height: 100%; backface-visibility: hidden; border-radius: 10px; display: flex; align-items: center; justify-content: center; padding: 16px; text-align: center; font-size: 0.9rem; line-height: 1.5; }}
  .card-front {{ background: var(--surface2); border: 1px solid var(--border); color: var(--text); }}
  .card-back {{ background: linear-gradient(135deg, #1e2a4a, #242740); border: 1px solid var(--accent); color: var(--accent2); transform: rotateY(180deg); }}

  .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
  @media (max-width: 768px) {{ .two-col {{ grid-template-columns: 1fr; }} }}

  .checklist {{ list-style: none; }}
  .checklist li {{ margin-bottom: 10px; }}
  .checklist label {{ display: flex; align-items: flex-start; gap: 10px; cursor: pointer; font-size: 0.9rem; line-height: 1.4; }}
  .checklist input[type=checkbox] {{ margin-top: 2px; accent-color: var(--accent); width: 16px; height: 16px; flex-shrink: 0; }}

  .mistakes {{ list-style: none; }}
  .mistakes li {{ padding: 8px 12px; margin-bottom: 8px; background: rgba(224,82,82,0.08); border-left: 3px solid var(--red); border-radius: 0 6px 6px 0; font-size: 0.9rem; line-height: 1.4; color: #eecccc; }}
  .mistakes li::before {{ content: "⚠ "; }}
</style>
</head>
<body>

<header>
  <div>
    <h1>Finals Study Guide</h1>
    <div class="sub">University of Oregon · Spring 2026</div>
  </div>
  <div class="badge">Powered by Claude</div>
</header>

<nav class="tabs">
  {tabs_html}
</nav>

<main class="content">
  {panels_html}
</main>

<script>
function showTab(id) {{
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('panel-' + id).classList.add('active');
  event.target.classList.add('active');
}}
</script>
</body>
</html>"""


def main():
    print("Extracting PDF content...")

    courses_data = {}

    # CS 315
    print("\n[CS 315] Reading lecture PDFs...")
    cs315_docs = extract_all(f"{BASE}/cs315", limit_per_file=5000)
    print(f"  → {len(cs315_docs)} files, generating study guide...")
    courses_data["CS 315: Intermediate Algorithms"] = generate_course_content(
        "CS 315: Intermediate Algorithms (Graphs, MST, Shortest Paths, Dynamic Programming, Greedy, Max Flow)",
        cs315_docs,
    )
    print("  ✓ Done")

    # CS 330
    print("\n[CS 330] Reading lecture PDFs...")
    cs330_docs = extract_all(f"{BASE}/cs330", limit_per_file=5000)
    print(f"  → {len(cs330_docs)} files, generating study guide...")
    courses_data["CS 330: C/C++ and Unix"] = generate_course_content(
        "CS 330: C/C++ and Unix (C programming, pointers, Unix, C++ OOP, BST, Red-Black Trees)",
        cs330_docs,
    )
    print("  ✓ Done")

    # EC 434
    print("\n[EC 434] Reading course files...")
    ec434_docs = extract_all(f"{BASE}/ec434", limit_per_file=5000)
    print(f"  → {len(ec434_docs)} files, generating study guide...")
    courses_data["EC 434: Environmental Economics"] = generate_course_content(
        "EC 434/534: Environmental Economics (externalities, pollution policy, cap-and-trade, contingent valuation, VSL, climate economics, IAM)",
        ec434_docs,
    )
    print("  ✓ Done")

    print("\nBuilding HTML...")
    html = build_html(courses_data)
    with open(OUT, "w") as f:
        f.write(html)
    print(f"\n✅ Study guide saved to: {OUT}")
    print(f"   Open with: open {OUT}")


if __name__ == "__main__":
    main()
