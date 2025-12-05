# streamlit_ai_helper.py
import streamlit as st
import ast
import re
import textwrap
import openai
from typing import List, Tuple, Dict, Any, Optional

# ----------------------------
# Page config + Neon + Dark CSS
# ----------------------------
st.set_page_config(page_title="AI Python Helper — Neon", page_icon="🤖", layout="wide")
NEON_CSS = """
<style>
:root{
  --bg1: #050306;
  --bg2: #0f0b1a;
  --card: rgba(255,255,255,0.03);
  --accent: #7cffcb;
  --accent2: #7c8cff;
  --text: #e6f0ff;
}
body {
  background: radial-gradient(circle at 10% 10%, #07102b 0%, var(--bg1) 30%, var(--bg2) 100%);
  color: var(--text);
}
.stApp > header { background: linear-gradient(90deg, rgba(124,255,203,0.06), rgba(124,140,255,0.03)); }
.stButton>button { border-radius: 12px; padding: 8px 12px; box-shadow: 0 6px 18px rgba(124,255,203,0.06); }
.stTextArea textarea, .stTextInput input {
  background: rgba(255,255,255,0.02) !important;
  color: var(--text) !important;
  border: 1px solid rgba(124,140,255,0.12) !important;
  border-radius: 8px;
}
.code-block, pre, code {
  background: rgba(0,0,0,0.35) !important;
  border-left: 3px solid rgba(124,255,203,0.18);
  padding: 8px !important;
  border-radius: 6px;
}
.neon-title {
  font-weight: 700;
  text-shadow: 0 0 8px rgba(124,255,203,0.15), 0 0 20px rgba(124,140,255,0.06);
}
.sidebar .stButton>button { background: linear-gradient(90deg,#7cffcb44,#7c8cff44); color: #eafaf3; }
</style>
"""
st.markdown(NEON_CSS, unsafe_allow_html=True)

st.markdown("<h1 class='neon-title'>🤖 AI Python Helper — Neon UI</h1>", unsafe_allow_html=True)
st.write("Static analysis + optional AI deep analysis (rewrite, line-by-line explanation, PEP8 & performance hints).")

# ----------------------------
# Sidebar (options)
# ----------------------------
st.sidebar.header("⚙️ Options / AI")
use_ai = st.sidebar.checkbox("Enable AI analysis (requires API key)", value=False)
api_key_input = st.sidebar.text_input("OpenAI API Key (optional)", type="password")
model_choice = st.sidebar.selectbox("Model (if using AI)", options=["gpt-4o-mini", "gpt-4o", "gpt-4o-mini-tts"], index=0)
temperature = st.sidebar.slider("AI creativity (temperature)", 0.0, 1.0, 0.2, 0.05)
show_pep8 = st.sidebar.checkbox("Show PEP8 suggestions", value=True)
show_perf = st.sidebar.checkbox("Show performance hints", value=True)
st.sidebar.markdown("---")
st.sidebar.markdown("⚠️ App does **not** execute your code. AI analysis will send the code to the selected model if enabled.")

if api_key_input:
    openai.api_key = api_key_input
else:
    import os
    if os.getenv("OPENAI_API_KEY"):
        openai.api_key = os.getenv("OPENAI_API_KEY")

# ----------------------------
# Input: code
# ----------------------------
st.subheader("Paste your Python code below")
code_input = st.text_area("Python code", height=300, value="# ตัวอย่าง: พิมพ์โค้ดที่นี่\n")

col_a, col_b, col_c = st.columns([1, 1, 1])
analyze_btn = col_a.button("🔍 Static Analyze")
ai_btn = col_b.button("🤖 AI Analyze & Rewrite")
all_btn = col_c.button("🔁 All (Static + AI)")

# ----------------------------
# Utilities: Static analysis
# ----------------------------
def safe_parse(code: str) -> Tuple[Optional[ast.AST], Optional[str]]:
    try:
        tree = ast.parse(code)
        return tree, None
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"

def pep8_heuristics(code: str, max_len:int=79) -> List[Tuple[int,str]]:
    issues=[]
    for i, line in enumerate(code.splitlines(), start=1):
        if len(line)>max_len:
            issues.append((i, f"line too long ({len(line)}>{max_len})"))
        if line.rstrip()!=line:
            issues.append((i, "trailing whitespace"))
        leading = len(line)-len(line.lstrip(' '))
        if line.strip() and leading%4!=0:
            issues.append((i, "indentation not multiple of 4"))
        if re.search(r"\w=[^\s=]", line) or re.search(r"[^\s=]=\w", line):
            issues.append((i, "missing spaces around operator"))
    # simple naming checks
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not re.match(r"^[a-z_][a-z0-9_]*$", node.name):
                    issues.append((node.lineno, f"function name not snake_case: {node.name}"))
            if isinstance(node, ast.ClassDef):
                if not re.match(r"^[A-Z][A-Za-z0-9]+$", node.name):
                    issues.append((node.lineno, f"class name not CamelCase: {node.name}"))
    except Exception:
        pass
    return issues

def explain_ast_lines(code: str) -> List[Tuple[int,str]]:
    try:
        tree = ast.parse(code)
    except Exception as e:
        return [(-1, f"Cannot parse: {e}")]
    expl=[]
    for node in ast.walk(tree):
        if hasattr(node, "lineno"):
            ln = node.lineno
            if isinstance(node, ast.Assign):
                try:
                    targ = ast.unparse(node.targets[0])
                except Exception:
                    targ = "assignment"
                expl.append((ln, f"Assign: {targ} = ..."))
            elif isinstance(node, ast.FunctionDef):
                args = [a.arg for a in node.args.args]
                expl.append((ln, f"FunctionDef: {node.name}({', '.join(args)})"))
            elif isinstance(node, ast.If):
                expl.append((ln, "If statement"))
            elif isinstance(node, ast.For):
                expl.append((ln, "For loop"))
            elif isinstance(node, ast.While):
                expl.append((ln, "While loop"))
            elif isinstance(node, ast.Import):
                expl.append((ln, "Import statement"))
            elif isinstance(node, ast.ImportFrom):
                expl.append((ln, f"from {node.module} import ..."))
            elif isinstance(node, ast.Return):
                expl.append((ln, "Return statement"))
            elif isinstance(node, ast.Call):
                try:
                    func = ast.unparse(node.func)
                except Exception:
                    func = "call"
                expl.append((ln, f"Call: {func}(...)"))
    expl_sorted = sorted(expl, key=lambda x:x[0])
    # compress to one explanation per line (join multiple)
    grouped = {}
    for ln, text in expl_sorted:
        grouped.setdefault(ln, []).append(text)
    return [(ln, " | ".join(grouped[ln])) for ln in sorted(grouped.keys())]

def performance_hints(code: str) -> List[str]:
    hints=[]
    try:
        tree = ast.parse(code)
    except Exception:
        return ["Cannot parse code for performance analysis."]
    # nested loop depth
    maxd=0
    def visit_depth(node, d=0):
        nonlocal maxd
        if isinstance(node, (ast.For, ast.While)):
            d+=1
            maxd = max(maxd,d)
        for ch in ast.iter_child_nodes(node):
            visit_depth(ch,d)
    visit_depth(tree)
    if maxd>=3:
        hints.append(f"Nested loop depth = {maxd}. Consider reducing complexity or using vectorized library.")
    # append in loop pattern
    class AppendLoopVisitor(ast.NodeVisitor):
        def __init__(self):
            self.appends=[]
            self.in_loop=0
        def visit_For(self,node):
            self.in_loop+=1; self.generic_visit(node); self.in_loop-=1
        def visit_While(self,node):
            self.in_loop+=1; self.generic_visit(node); self.in_loop-=1
        def visit_Call(self,node):
            if isinstance(node.func, ast.Attribute) and getattr(node.func,'attr',None)=="append" and self.in_loop>0:
                try:
                    owner = ast.unparse(node.func.value)
                except Exception:
                    owner = "list"
                self.appends.append((node.lineno, owner))
            self.generic_visit(node)
    v=AppendLoopVisitor(); v.visit(tree)
    for ln, owner in v.appends[:5]:
        hints.append(f"Found {owner}.append(...) inside loop at line {ln}; consider listcomp or preallocation.")
    # string concat in loop
    class ConcatVisitor(ast.NodeVisitor):
        def __init__(self):
            self.found=[]
            self.in_loop=0
        def visit_For(self,node):
            self.in_loop+=1; self.generic_visit(node); self.in_loop-=1
        def visit_While(self,node):
            self.in_loop+=1; self.generic_visit(node); self.in_loop-=1
        def visit_AugAssign(self,node):
            if self.in_loop and isinstance(node.op, ast.Add) and isinstance(node.target, ast.Name):
                self.found.append(node.lineno)
            self.generic_visit(node)
    cv=ConcatVisitor(); cv.visit(tree)
    for ln in cv.found[:5]:
        hints.append(f"String concat with += in loop at line {ln}; consider join on list.")
    if not hints:
        hints.append("No obvious static performance issues found.")
    return hints

# ----------------------------
# AI helpers
# ----------------------------
def build_ai_prompt(code: str, tasks: List[str]) -> str:
    """
    Build a concise prompt describing tasks for the AI.
    tasks: list like ["rewrite", "line_by_line", "pep8", "performance"]
    """
    intro = (
        "You are a helpful Python assistant. The user will provide source code. "
        "Do NOT execute it. Provide safe, concise, actionable output.\n\n"
    )
    instructions = []
    if "rewrite" in tasks:
        instructions.append(
            "1) Provide a corrected, runnable rewrite of the code (preserve behavior where clear). "
            "If behavior is ambiguous, explain uncertainty and provide a conservative fix."
        )
    if "line_by_line" in tasks:
        instructions.append(
            "2) Provide a line-by-line explanation in Thai (keep each line short and numbered)."
        )
    if "pep8" in tasks:
        instructions.append("3) Provide PEP8 style suggestions and show a few example fixes.")
    if "performance" in tasks:
        instructions.append("4) Provide performance analysis and specific refactor suggestions.")
    prompt = intro + "\n".join(instructions) + "\n\nCode:\n" + code + "\n\nRespond in JSON with keys: rewritten, explanation, pep8, performance, suggestions. Keep rewritten code in a single string."
    return prompt

def call_openai_chat(prompt: str, model: str="gpt-4o-mini", temperature: float=0.2, max_tokens: int=1600) -> Optional[Dict[str,Any]]:
    if not getattr(openai, "api_key", None):
        st.error("OpenAI API key not provided.")
        return None
    try:
        resp = openai.ChatCompletion.create(
            model=model,
            messages=[{"role":"user","content":prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        text = resp.choices[0].message.content
        # try parse JSON out of response heuristically
        # user-facing: show raw text if not JSON
        try:
            import json as _json
            parsed = _json.loads(text)
            return parsed
        except Exception:
            return {"raw": text}
    except Exception as e:
        st.error(f"OpenAI API error: {e}")
        return None

# ----------------------------
# Main actions
# ----------------------------
def do_static_analysis(code: str):
    tree, err = safe_parse(code)
    st.subheader("🔎 Static Analysis")
    if err:
        st.error(f"Syntax parse error: {err}")
    else:
        st.success("Parsed successfully (AST OK).")
    if show_pep8:
        st.markdown("**PEP8 Heuristics**")
        issues = pep8_heuristics(code)
        if issues:
            for ln, msg in issues:
                st.warning(f"Line {ln}: {msg}")
        else:
            st.info("No PEP8 issues (heuristic) found.")
    st.markdown("**AST-based explanation (high-level)**")
    for ln, text in explain_ast_lines(code):
        st.write(f"Line {ln}: {text}")
    if show_perf:
        st.markdown("**Performance hints (heuristic)**")
        for hint in performance_hints(code):
            st.info(hint)

def do_ai_analysis(code: str):
    if not getattr(openai, "api_key", None):
        st.error("OpenAI API key not configured. Set it in sidebar or environment variable.")
        return
    tasks = ["rewrite", "line_by_line", "pep8", "performance"]
    st.subheader("🤖 AI Deep Analysis")
    with st.spinner("Sending to AI model..."):
        prompt = build_ai_prompt(code, tasks)
        result = call_openai_chat(prompt, model=model_choice, temperature=temperature)
    if not result:
        return
    if "raw" in result:
        st.markdown("**Raw AI response (not JSON)**")
        st.code(result["raw"])
        return
    # show rewritten
    if result.get("rewritten"):
        st.markdown("**Rewritten Code (AI suggestion)**")
        st.code(result["rewritten"], language="python")
    if result.get("explanation"):
        st.markdown("**Line-by-line Explanation (AI)**")
        st.text(result["explanation"])
    if result.get("pep8"):
        st.markdown("**PEP8 Suggestions (AI)**")
        st.text(result["pep8"])
    if result.get("performance"):
        st.markdown("**Performance Suggestions (AI)**")
        st.text(result["performance"])
    if result.get("suggestions"):
        st.markdown("**Other Suggestions**")
        st.text(result["suggestions"])

# ----------------------------
# Button handlers
# ----------------------------
if analyze_btn:
    do_static_analysis(code_input)

if ai_btn:
    if not use_ai:
        st.warning("Enable 'Enable AI analysis' in sidebar first.")
    else:
        do_ai_analysis(code_input)

if all_btn:
    do_static_analysis(code_input)
    if use_ai:
        do_ai_analysis(code_input)
