"""Programmatic grader for learning-mode evals. Usage: python grade.py <iteration_dir>"""
import json, re, sys
from pathlib import Path

FIX = Path(__file__).parent / "fixtures"
CASES = {
    "eval-1-python-retry": ("api_client.py", r"backoff|exponencial|exponential", True),
    "eval-2-js-refactor": ("discount.js", r"guard clause|early return|retorno antecipado", True),
    "eval-3-explain-only": ("slugify.ts", None, False),
}

def footnote(text):
    m = re.search(r"\n---\s*\n((?:>.*\n?)+)\s*$", text.strip() + "\n")
    return m.group(1) if m else None

def comment_lines(src, ext):
    pat = r"^\s*#" if ext == ".py" else r"^\s*//"
    return sum(1 for l in src.splitlines() if re.match(pat, l))

def grade(run_dir, case):
    fname, technique, expects_note = CASES[case]
    out = run_dir / "outputs"
    resp = (out / "response.md").read_text(encoding="utf-8") if (out / "response.md").exists() else ""
    code_p = out / fname
    code = code_p.read_text(encoding="utf-8") if code_p.exists() else ""
    fixture = (FIX / fname).read_text(encoding="utf-8")
    note = footnote(resp)
    exp = []
    def add(text, passed, ev): exp.append({"text": text, "passed": bool(passed), "evidence": ev})
    if expects_note:
        add("Response ends with footnote (--- + blockquote with 📝 and 🤔)",
            note and "📝" in note and "🤔" in note, (note or "no footnote found at end")[:300])
        expl = re.search(r"📝(.*)", note or "")
        expl_t = expl.group(1) if expl else ""
        n_sent = len([s for s in re.split(r"(?<=[.!?])\s+", expl_t.strip(" *")) if s.strip()])
        n_words = len(expl_t.split())
        add("📝 explanation is 1-2 sentences and <=45 words", expl and 1 <= n_sent <= 2 and n_words <= 45, f"{n_sent} sentences, {n_words} words")
        add("📝 names the technique used", expl and re.search(technique, expl_t, re.I), expl_t[:200])
        q = re.search(r"🤔(.*)", note or "")
        q_t = q.group(1) if q else ""
        add("🤔 is exactly one question, <=30 words, not answered after", q and q_t.count("?") == 1 and q_t.strip(" *").endswith("?") and len(q_t.split()) <= 30, f"{len(q_t.split())} words: " + q_t[:200])
        add("No teaching comments added to code (comment count not above fixture)",
            code and comment_lines(code, code_p.suffix) <= comment_lines(fixture, code_p.suffix),
            f"fixture={comment_lines(fixture, code_p.suffix)} output={comment_lines(code, code_p.suffix)}")
        add("No extra tutorial sections (no 'learning'/'por que'/'para fixar' headings)",
            not re.search(r"^#+ .*(learning|aprend|por que|para fixar|praticar)", resp, re.I | re.M), "headings checked")
    else:
        add("No learning-mode footnote (no code was changed)", "📝" not in resp and "🤔" not in resp, "searched for 📝/🤔")
        add("Code file unchanged", (not code) or code == fixture, "compared to fixture")
    passed = sum(e["passed"] for e in exp)
    res = {"expectations": exp, "summary": {"passed": passed, "failed": len(exp) - passed, "total": len(exp), "pass_rate": passed / len(exp)}}
    (run_dir / "grading.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    return res

it = Path(sys.argv[1])
for case in CASES:
    for cfg in ("with_skill", "without_skill"):
        d = it / case / cfg / "run-1"
        if (d / "outputs" / "response.md").exists():
            r = grade(d, case)
            print(case, cfg, f"{r['summary']['passed']}/{r['summary']['total']}")
