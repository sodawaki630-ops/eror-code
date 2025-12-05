import streamlit as st
import ast
import re
import textwrap
from collections import defaultdict

st.set_page_config(page_title="Ultimate Error Helper Pro", page_icon="🧰", layout="wide")
st.title("🧰 Ultimate Python Error Helper — Pro")
st.markdown("ตรวจ, rewrite, อธิบายทีละบรรทัด, ตรวจ PEP8 แบบเบื้องต้น และวิเคราะห์ performance (static analysis, ปลอดภัย)")

# -----------------------
# UI: inputs
# -----------------------
st.sidebar.header("Options")
dark = st.sidebar.checkbox("Dark mode", value=False)
show_raw_ast = st.sidebar.checkbox("แสดง AST (debug)", value=False)
max_line_length = st.sidebar.number_input("PEP8 max line length", min_value=60, max_value=200, value=79)

if dark:
    st.markdown(
        """
        <style>
        body { background-color: #0b1221; color: #c9d1d9; }
        .stTextArea textarea { background-color: #0e1624 !important; color: #c9d1d9 !important; }
        .stCodeBlock { background-color: #0e1624 !important; color: #c9d1d9 !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

st.subheader("วางโค้ด Python ของคุณที่ต้องการให้ตรวจและแก้ไข (ป้อนหลายบรรทัดได้)")
user_code = st.text_area("โค้ด Python", value="""# ตัวอย่าง
def greet(name)
    print("Hello " + name)

for i in range(5):
    print(i)
""", height=260)

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    analyze_btn = st.button("🔍 วิเคราะห์")
with col2:
    rewrite_btn = st.button("✍️ Rewrite + Suggest")
with col3:
    full_run = st.button("🔁 วิเคราะห์ + Rewrite ทั้งหมด")

# -----------------------
# Helpers: safety & utils
# -----------------------
PY_KEYWORDS = {
    "False","None","True","and","as","assert","async","await","break","class","continue","def","del","elif","else",
    "except","finally","for","from","global","if","import","in","is","lambda","nonlocal","not","or","pass","raise",
    "return","try","while","with","yield"
}

identifier_re = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")

def safe_parse(code):
    """Attempt to parse code into AST. Return (tree, error_message)."""
    try:
        tree = ast.parse(code)
        return tree, None
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"

def normalize_indentation(code):
    # replace tabs with 4 spaces and remove trailing spaces
    lines = code.splitlines()
    new = []
    for ln in lines:
        ln2 = ln.replace("\t", "    ").rstrip()
        new.append(ln2)
    return "\n".join(new) + ("\n" if code and not code.endswith("\n") else "")

def simple_auto_fix(code):
    """
    Basic automatic fixes:
    - normalize indentation (tabs -> 4 spaces)
    - if def/class line has no body, add '    pass'
    - ensure trailing newline
    - fix common missing colon by heuristic (line ending with def ... or if ... but missing ':')
    Note: this is conservative and won't attempt dangerous or ambiguous fixes.
    """
    code = normalize_indentation(code)
    lines = code.splitlines()
    fixed_lines = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        stripped = ln.strip()
        # fix def/class/if/for/while/match that miss colon at EOL
        header_match = re.match(r"^(def\s+[A-Za-z_][A-Za-z0-9_]*\s*\(.*\)|class\s+[A-Za-z_][A-Za-z0-9_]*\s*(\(.+\))?|if\s+.+|for\s+.+|while\s+.+|try|except\s+.+|else|elif\s+.+|with\s+.+)$", stripped)
        if header_match and not stripped.endswith(":"):
            fixed_lines.append(ln + ":")
            i += 1
            # if next line is end or next line is also dedent, insert pass
            if i >= len(lines) or (lines[i].strip() == "" or len(lines[i]) - len(lines[i].lstrip()) <= len(ln) - len(ln.lstrip())):
                fixed_lines.append(" " * (len(ln) - len(ln.lstrip()) + 4) + "pass")
            continue

        # add pass to empty def/class with no body
        def_match = re.match(r"^\s*def\s+[A-Za-z_][A-Za-z0-9_]*\s*\(.*\)\s*:$", ln)
        class_match = re.match(r"^\s*class\s+[A-Za-z_][A-Za-z0-9_]*\s*(\(.*\))?\s*:$", ln)
        if (def_match or class_match):
            # look ahead to see if next non-empty line is more indented
            j = i + 1
            body_found = False
            while j < len(lines):
                if lines[j].strip() == "":
                    j += 1
                    continue
                body_indent = len(lines[j]) - len(lines[j].lstrip())
                header_indent = len(ln) - len(ln.lstrip())
                if body_indent > header_indent:
                    body_found = True
                break
            if not body_found:
                fixed_lines.append(ln)
                fixed_lines.append(" " * (len(ln) - len(ln.lstrip()) + 4) + "pass")
                i += 1
                continue

        fixed_lines.append(ln)
        i += 1

    fixed_code = "\n".join(fixed_lines)
    if fixed_code and not fixed_code.endswith("\n"):
        fixed_code += "\n"
    return fixed_code

def attempt_unparse(tree):
    """Try to generate normalized code from AST. Fall back to None if not available."""
    try:
        # ast.unparse available in Python 3.9+
        return ast.unparse(tree)
    except Exception:
        return None

# -----------------------
# Analysis Functions
# -----------------------
def pep8_checks(code, max_line=79):
    issues = []
    lines = code.splitlines()
    for i, line in enumerate(lines, start=1):
        if len(line) > max_line:
            issues.append((i, "line-too-long", f"บรรทัดยาวเกิน {max_line} ตัวอักษร ({len(line)})"))
        if line.rstrip() != line:
            issues.append((i, "trailing-whitespace", "มีช่องว่างท้ายบรรทัด"))
        # indent not multiple of 4?
        leading = len(line) - len(line.lstrip(' '))
        if leading % 4 != 0:
            # ignore completely blank lines
            if line.strip():
                issues.append((i, "indentation", "การย่อหน้าไม่เป็น multiple ของ 4 ช่อง (PEP8 แนะนำ 4)"))
        # two spaces before inline comment?
        if "#" in line:
            code_part = line.split("#", 1)[0]
            if code_part.endswith("  "):
                issues.append((i, "whitespace-before-comment", "มีสองช่องว่างก่อน comment (แนะนำ 2 คือ acceptable แต่เช็คให้)"))
        # space around operator simple checks
        if re.search(r"\w=[^\s=]", line) or re.search(r"[^\s=]=\w", line):
            issues.append((i, "whitespace", "อาจไม่มีช่องว่างรอบเครื่องหมาย ="))

    # naming conventions (variables/functions)
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                name = node.name
                if not re.match(r"^[a-z_][a-z0-9_]*$", name):
                    issues.append((node.lineno, "func-name", f"ชื่ิอฟังก์ชัน '{name}' ไม่เป็น snake_case"))
            if isinstance(node, ast.ClassDef):
                name = node.name
                if not re.match(r"^[A-Z][A-Za-z0-9]+$", name):
                    issues.append((node.lineno, "class-name", f"ชื่อคลาส '{name}' ไม่เป็น CamelCase"))
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var = target.id
                        if not re.match(r"^[a-z_][a-z0-9_]*$", var):
                            issues.append((node.lineno, "var-name", f"ชื่อตัวแปร '{var}' ไม่เป็น snake_case"))
    except Exception:
        pass

    return issues

def explain_by_ast(code):
    """Return list of (lineno, explanation) by traversing AST and mapping nodes to lines."""
    try:
        tree = ast.parse(code)
    except Exception as e:
        return [("0", f"ไม่สามารถอธิบายโค้ดได้: {e}")]
    explanations = defaultdict(list)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            # simplistic: describe assignment
            try:
                targets = [ast.unparse(t) for t in node.targets]
            except Exception:
                targets = [getattr(node.targets[0], 'id', 'variable')]
            val = None
            try:
                val = ast.unparse(node.value)
            except Exception:
                val = type(node.value).__name__
            explanations[node.lineno].append(f"กำหนดตัวแปร {' ,'.join(targets)} = {val}")
        elif isinstance(node, ast.FunctionDef):
            args = [a.arg for a in node.args.args]
            explanations[node.lineno].append(f"ประกาศฟังก์ชัน `{node.name}({', '.join(args)})`")
        elif isinstance(node, ast.If):
            explanations[node.lineno].append("เงื่อนไข `if` ถูกใช้เพื่อตรวจสอบค่าบางอย่าง")
        elif isinstance(node, ast.For):
            explanations[node.lineno].append("วนลูป `for` เพื่อทำซ้ำค่าหลาย ๆ ค่า")
        elif isinstance(node, ast.While):
            explanations[node.lineno].append("วนลูป `while` (เงื่อนไขเป็นตัวกำหนดการหยุด)")
        elif isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
            explanations[node.lineno].append(f"นำเข้าโมดูล: {', '.join(names)}")
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            names = [alias.name for alias in node.names]
            explanations[node.lineno].append(f"นำเข้า {', '.join(names)} จาก `{mod}`")
        elif isinstance(node, ast.Return):
            explanations[node.lineno].append("คืนค่าจากฟังก์ชัน (return)")
        elif isinstance(node, ast.Call):
            # function call explanation
            try:
                funcname = ast.unparse(node.func)
            except Exception:
                funcname = "call"
            explanations[node.lineno].append(f"เรียกใช้งานฟังก์ชัน/เมธอด `{funcname}`")
    # convert to sorted list by line
    out = []
    for lineno in sorted(explanations.keys()):
        for text in explanations[lineno]:
            out.append((lineno, text))
    return out

def performance_hints(code):
    hints = []
    try:
        tree = ast.parse(code)
    except Exception:
        return ["ไม่สามารถวิเคราะห์ performance ได้ เนื่องจากโค้ดมี Syntax Error"]

    # detect nested loops depth
    max_depth = 0
    def loop_depth(node, depth=0):
        nonlocal max_depth
        if isinstance(node, (ast.For, ast.While)):
            depth += 1
            max_depth = max(max_depth, depth)
        for child in ast.iter_child_nodes(node):
            loop_depth(child, depth)
    loop_depth(tree)
    if max_depth >= 3:
        hints.append(f"มี nested loop ความลึก {max_depth} — พิจารณา refactor หรือใช้ algorithms ที่ซับซ้อนน้อยลง")

    # detect list append in loops (suggest listcomp)
    class AppendVisitor(ast.NodeVisitor):
        def __init__(self):
            self.append_in_loop = []
            self.in_loop = 0
            self.current_target = None
        def visit_For(self, node):
            self.in_loop += 1
            self.generic_visit(node)
            self.in_loop -= 1
        def visit_While(self, node):
            self.in_loop += 1
            self.generic_visit(node)
            self.in_loop -= 1
        def visit_Call(self, node):
            # look for x.append(...)
            if isinstance(node.func, ast.Attribute) and node.func.attr == "append":
                if self.in_loop > 0:
                    try:
                        owner = ast.unparse(node.func.value)
                    except Exception:
                        owner = "list"
                    self.append_in_loop.append((node.lineno, owner))
            self.generic_visit(node)
    av = AppendVisitor()
    av.visit(tree)
    if av.append_in_loop:
        for ln, owner in av.append_in_loop[:5]:
            hints.append(f"ที่บรรทัด {ln} พบ `{owner}.append(...)` ภายใน loop — พิจารณาใช้ list comprehension หรือ pre-allocate list เพื่อประสิทธิภาพ")

    # detect recursion (simple)
    funcs = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            funcs[node.name] = node
    for name, node in funcs.items():
        class RecVisitor(ast.NodeVisitor):
            def __init__(self, fname):
                self.fname = fname
                self.recursive = False
            def visit_Call(self, n):
                try:
                    fname = ast.unparse(n.func)
                except Exception:
                    fname = ""
                if fname == self.fname:
                    self.recursive = True
                self.generic_visit(n)
        rv = RecVisitor(name)
        rv.visit(node)
        if rv.recursive:
            hints.append(f"ฟังก์ชัน `{name}` เรียกตัวเอง (recursion) — ตรวจ stack depth และพิจารณาใช้ iterative ถ้าจำเป็น")

    # heavy string concatenation in loop: detect `s += something` inside loop
    class StrConcatVisitor(ast.NodeVisitor):
        def __init__(self):
            self.concat_in_loop = []
            self.in_loop = 0
        def visit_For(self, n):
            self.in_loop += 1
            self.generic_visit(n)
            self.in_loop -= 1
        def visit_While(self, n):
            self.in_loop += 1
            self.generic_visit(n)
            self.in_loop -= 1
        def visit_AugAssign(self, n):
            if isinstance(n.op, ast.Add) and isinstance(n.target, ast.Name):
                if self.in_loop > 0:
                    self.concat_in_loop.append(n.lineno)
            self.generic_visit(n)
    scv = StrConcatVisitor()
    scv.visit(tree)
    if scv.concat_in_loop:
        for ln in scv.concat_in_loop[:5]:
            hints.append(f"ที่บรรทัด {ln} พบการต่อ string (`+=`) ใน loop — ใช้ list append แล้ว `''.join()` แทนจะเร็วกว่า")

    if not hints:
        hints.append("ไม่พบ pattern ที่ชี้ชัดเรื่อง performance. โค้ดดูไม่มีปัญหา performance ที่ชัดเจนจาก static heuristics")

    return hints

def suggest_structure(code):
    suggestions = []
    # recommend modularization: functions for repeated logic
    try:
        tree = ast.parse(code)
    except Exception:
        return ["ไม่สามารถแนะนำโครงสร้างได้ เนื่องจากมี Syntax Error"]

    func_count = sum(1 for n in ast.walk(tree) if isinstance(n, ast.FunctionDef))
    top_level_statements = [n for n in tree.body if not isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.Import, ast.ImportFrom))]
    if len(top_level_statements) > 5:
        suggestions.append("พบโค้ดหลายบรรทัดที่อยู่บนระดับ top-level — แนะนำย้ายโค้ดเหล่านี้เข้าไปในฟังก์ชันและเรียกจาก `if __name__ == '__main__'`")
    if func_count == 0 and len(top_level_statements) > 0:
        suggestions.append("แนะนำสร้างฟังก์ชันแยกงานต่างๆ เพื่อให้ง่ายต่อการทดสอบและเรียกใช้ซ้ำ")
    # recommend adding main guard
    if not any(isinstance(n, ast.If) and getattr(n.test, 'left', None) and getattr(n.test.left, 'id', None) == '__name__' for n in tree.body if isinstance(n, ast.If)):
        suggestions.append("พิจารณาเพิ่ม `if __name__ == '__main__':` เพื่อให้โค้ดสามารถนำเข้าเป็นโมดูลได้โดยไม่รันทันที")
    # recommend splitting big functions
    for n in ast.walk(tree):
        if isinstance(n, ast.FunctionDef):
            n_lines = (getattr(n, 'end_lineno', None) or n.lineno) - n.lineno + 1
            if n_lines > 80:
                suggestions.append(f"ฟังก์ชัน `{n.name}` ยาว {n_lines} บรรทัด — แนะนำแยกเป็นฟังก์ชันย่อย")
    if not suggestions:
        suggestions.append("โครงสร้างพื้นฐานดูเรียบร้อย — พิจารณาเพิ่ม docstring ให้ฟังก์ชันและคอมเมนต์สั้น ๆ")
    return suggestions

# -----------------------
# Main actions
# -----------------------
def do_full_analysis(code, max_line_len=79):
    out = {}
    code_orig = code
    code_norm = normalize_indentation(code_orig)
    out['normalized_code'] = code_norm
    tree, parse_err = safe_parse(code_norm)
    out['syntax_error'] = parse_err
    if parse_err:
        # attempt automatic fix then reparse
        fixed = simple_auto_fix(code_norm)
        tree2, parse_err2 = safe_parse(fixed)
        out['auto_fixed_attempt'] = fixed
        out['auto_fix_success'] = parse_err2 is None
        out['syntax_error_after_fix'] = parse_err2
        if parse_err2 is None:
            tree = tree2
    # attempt rewrite via AST unparse if parse ok
    rewritten = None
    if tree is not None:
        up = attempt_unparse(tree)
        if up:
            # ast.unparse may produce compact formatting — re-indent nicely
            rewritten = textwrap.dedent(up) + ("\n" if not up.endswith("\n") else "")
    out['rewritten_code'] = rewritten
    out['pep8_issues'] = pep8_checks(code_norm, max_line=max_line_len)
    out['explanations'] = explain_by_ast(code_norm)
    out['performance_hints'] = performance_hints(code_norm)
    out['structure_suggestions'] = suggest_structure(code_norm)
    return out

# -----------------------
# Button events
# -----------------------
if analyze_btn or full_run:
    st.markdown("## 🔎 ผลการวิเคราะห์ (static)")
    result = do_full_analysis(user_code, max_line_len=max_line_length)
    # show syntax
    if result['syntax_error']:
        st.error(f"❌ Syntax Error: {result['syntax_error']}")
        if result.get('auto_fixed_attempt'):
            st.info("ลองแก้โค้ดอัตโนมัติแบบง่ายแล้ว — ดูด้านล่าง (auto fix attempt)")
    else:
        st.success("✔️ Syntax ปกติ")
    # show normalized code
    with st.expander("โค้ด (normalize indentation)"):
        st.code(result['normalized_code'], language="python")
    if result.get('auto_fixed_attempt'):
        with st.expander("โค้ดที่ระบบพยายามแก้ให้อัตโนมัติ (conservative fix)"):
            st.code(result['auto_fixed_attempt'], language="python")
            if result['auto_fix_success']:
                st.success("ระบบแก้ไขสำเร็จ (parsed OK) — แต่ควรตรวจดูว่า logic ถูกต้องตามต้องการ")
            else:
                st.warning("ระบบแก้แล้วยังมี Syntax Error — กรุณาตรวจโค้ดต้นฉบับ")

    # rewritten (AST unparse)
    if result.get('rewritten_code'):
        with st.expander("Rewrite (normalized via AST.unparse) — โค้ดที่แนะนำ"):
            st.code(result['rewritten_code'], language="python")
    else:
        st.info("ไม่สามารถ rewrite ด้วย AST ได้ (อาจเป็นเพราะไม่รองรับ ast.unparse ใน environment นี้)")

    # PEP8 issues
    st.markdown("### 🧾 ผลตรวจ PEP8 / Style (เบื้องต้น)")
    if result['pep8_issues']:
        for ln, code_key, msg in result['pep8_issues']:
            st.warning(f"บรรทัด {ln}: {msg}")
    else:
        st.success("✔️ ไม่มีปัญหา style ที่ตรวจพบ (ตาม heuristics ของเรา)")

    # Explanations by line
    st.markdown("### 📖 อธิบายโค้ดทีละบรรทัด (จาก AST)")
    if result['explanations']:
        last_ln = -1
        for ln, text in result['explanations']:
            st.write(f"**บรรทัด {ln}:** {text}")
    else:
        st.info("ไม่พบโครงสร้างให้วิเคราะห์ (หรือโค้ดว่าง)")

    # performance
    st.markdown("### ⚡ คำแนะนำด้าน performance (heuristic)")
    for h in result['performance_hints']:
        st.info(h)

    # structure suggestions
    st.markdown("### 🧱 คำแนะนำโครงสร้างโค้ด")
    for s in result['structure_suggestions']:
        st.write("- " + s)

    if show_raw_ast and ('rewritten_code' in result and result['rewritten_code']):
        try:
            st.subheader("Raw AST")
            tree2, _ = safe_parse(result['rewritten_code'])
            st.text(ast.dump(tree2, include_attributes=True, indent=2))
        except Exception:
            pass

if rewrite_btn or full_run:
    st.markdown("## ✍️ Rewrite / Suggested Fixes")
    # produce rewritten code and a suggested "refactor skeleton"
    res = do_full_analysis(user_code, max_line_len=max_line_length)
    rewritten = res.get('rewritten_code') or res.get('auto_fixed_attempt') or normalize_indentation(user_code)
    # further enhance: add main guard if missing
    try:
        tree = ast.parse(rewritten)
        has_main = any(isinstance(n, ast.If) and isinstance(n.test, ast.Compare) and
                       isinstance(n.test.left, ast.Name) and n.test.left.id == '__name__' for n in tree.body if isinstance(n, ast.If))
    except Exception:
        has_main = False

    suggested = rewritten
    if not has_main:
        # find top-level executable statements and wrap into main skeleton suggestion (done non-destructively: create a recommended file)
        suggested = (
            "# Suggested refactor: separate logic into functions and add main guard\n"
            "def main():\n"
        )
        # indent original top-level code into main (but avoid re-indenting function/class/import blocks)
        try:
            tree_orig = ast.parse(rewritten)
            body_lines = rewritten.splitlines()
            # naive: include all code but indent everything by 4 (conservative)
            for ln in rewritten.splitlines():
                suggested += "    " + ln + "\n"
            suggested += "\nif __name__ == '__main__':\n    main()\n"
        except Exception:
            suggested = rewritten + "\n\n# Add: if __name__ == '__main__': main()"

    st.subheader("โค้ดที่ rewrite/normalize แล้ว")
    st.code(rewritten, language="python")

    st.subheader("โค้ดที่แนะนำ (refactor skeleton)")
    st.code(suggested, language="python")

    st.markdown("**หมายเหตุ:** การ rewrite นี้เป็น automated และเป็น conservative fix — โปรดตรวจสอบ logic และ unit test ก่อนใช้งานจริง")

# -----------------------
# Utility: quick tips & examples
# -----------------------
st.markdown("---")
st.markdown("## 💡 เคล็ดลับสั้น ๆ")
st.markdown("""
- ถ้าต้องการให้ระบบอธิบายทีละบรรทัดได้แม่นขึ้น: ใส่ docstring/คอมเมนต์สั้น ๆ ในฟังก์ชัน  
- สำหรับ performance: ถ้ามี nested loop สูง ควรพิจารณาอัลกอริทึมใหม่หรือใช้ library เช่น `numpy`/`pandas` สำหรับงานเชิงตัวเลข  
- โค้ดที่ rewrite โดย AST จะเปลี่ยนรูปแบบ (formatting) — ถ้าต้องการ style ที่รัดกุม แนะนำใช้ `black` หรือ `autopep8` ภายนอก (ต้องติดตั้งเพิ่ม)  
""")

st.markdown("---")
st.markdown("ถ้าต้องการ ผมช่วยต่อได้: \n- เชื่อมกับ `black` / `autopep8` เพื่อ format ตาม PEP8 อัตโนมัติ\n- เพิ่ม unit-test generator (pytest)\n- เพิ่ม feature ให้ระบบเสนอแก้ทีละจุด และ apply ตามเลือกของผู้ใช้")
