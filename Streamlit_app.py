import streamlit as st
import ast
import re

# ---------------------------------------------------
# Page Config
# ---------------------------------------------------
st.set_page_config(page_title="Ultimate Python Error Helper", page_icon="🛠️", layout="wide")

st.title("🛠️ Ultimate Python Error Helper")
st.caption("ตรวจหาข้อผิดพลาด • วิเคราะห์โค้ด • อธิบายโค้ด • เสนอวิธีแก้ไข")

# ---------------------------------------------------
# Dark Mode Toggle
# ---------------------------------------------------
dark_mode = st.toggle("🌙 Dark Mode")

if dark_mode:
    st.markdown("""
        <style>
            body { background-color: #0d1117; color: #c9d1d9; }
            .stTextInput textarea, .stTextArea textarea { background-color: #161b22 !important; color: #c9d1d9 !important; }
        </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------
# Input Code
# ---------------------------------------------------
code = st.text_area("พิมพ์โค้ด Python ที่ต้องการตรวจ:", height=250)

run_btn = st.button("🔍 ตรวจโค้ด + แก้ไขให้")

# ---------------------------------------------------
# Helper Functions
# ---------------------------------------------------

def check_syntax(code):
    try:
        compile(code, "<string>", "exec")
        return None
    except Exception as e:
        return f"{type(e).__name__}: {e}"

def check_brackets(text):
    brackets = {"(": ")", "[": "]", "{": "}"}
    stack = []
    for i, ch in enumerate(text):
        if ch in brackets:
            stack.append((ch, i))
        elif ch in brackets.values():
            if not stack or brackets[stack[-1][0]] != ch:
                return f"พบวงเล็บปิดเกินแถว index {i}"
            stack.pop()
    if stack:
        return f"วงเล็บเปิดที่ index {stack[-1][1]} ยังไม่ถูกปิด"
    return None

def find_undefined(code):
    declared = set()
    used = set()

    for line in code.split("\n"):
        line_strip = line.strip()
        if "=" in line_strip and not line_strip.startswith("#"):
            var = line_strip.split("=")[0].strip()
            if var.isidentifier():
                declared.add(var)

        for token in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", line_strip):
            used.add(token)

    # ลบ keyword
    python_keywords = {
        "def","return","if","else","for","while","class","import","from","in","and","or","not"
    }
    used = used - python_keywords

    undefined = used - declared
    return undefined

def guess_missing_imports(code):
    common = ["json","random","math","os","re","datetime"]
    missing = []
    for m in common:
        if f"{m}." in code and f"import {m}" not in code:
            missing.append(m)
    return missing

def explain_code(code):
    explanation = []
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                explanation.append(f"กำหนดตัวแปร `{node.targets[0].id}`")
            elif isinstance(node, ast.FunctionDef):
                explanation.append(f"ฟังก์ชัน `{node.name}` ใช้งานสำหรับงานบางอย่างในโปรแกรม")
            elif isinstance(node, ast.If):
                explanation.append("มีการตรวจสอบเงื่อนไขด้วย if")
            elif isinstance(node, ast.For):
                explanation.append("มีการวนลูป for")
            elif isinstance(node, ast.While):
                explanation.append("มีการวนลูป while")
        return "\n".join(explanation) if explanation else "ไม่มีโครงสร้างสำคัญให้วิเคราะห์"
    except:
        return "ไม่สามารถอธิบายโค้ดได้ เนื่องจากมี Syntax Error"

def basic_auto_fix(code):
    fixed = code

    # แก้ tab → 4 spaces
    fixed = fixed.replace("\t", "    ")

    # เติม pass ถ้าฟังก์ชันว่าง
    fixed = re.sub(r"def (.*):\s*$", r"def \1:\n    pass", fixed)

    # แก้วงเล็บเยื้องต้น (ง่ายมาก)
    if check_brackets(code):
        fixed += "\n# TODO: ตรวจสอบวงเล็บไม่ครบ"

    return fixed

# ---------------------------------------------------
# Main Output
# ---------------------------------------------------

if run_btn:

    if not code.strip():
        st.warning("กรุณาใส่โค้ดก่อนตรวจครับ")
        st.stop()

    st.header("📌 ผลการตรวจสอบ")

    # 1) Syntax Check
    st.subheader("1) ตรวจ Syntax")
    syntax_error = check_syntax(code)
    if syntax_error:
        st.error(f"❌ พบ Syntax Error:\n{syntax_error}")
    else:
        st.success("✔️ Syntax ปกติ ไม่พบข้อผิดพลาด")

    # 2) Bracket Check
    st.subheader("2) ตรวจวงเล็บ")
    bracket_issue = check_brackets(code)
    if bracket_issue:
        st.warning(f"⚠️ {bracket_issue}")
    else:
        st.success("✔️ วงเล็บครบถ้วน")

    # 3) Undefined variable
    st.subheader("3) ตัวแปรที่ยังไม่ถูกประกาศ")
    undefined = find_undefined(code)
    if undefined:
        st.warning("⚠️ อาจยังไม่ประกาศตัวแปร: " + ", ".join(undefined))
    else:
        st.success("✔️ ไม่พบตัวแปรที่ไม่ถูกประกาศ")

    # 4) Missing imports
    st.subheader("4) โมดูลที่อาจลืม import")
    missing = guess_missing_imports(code)
    if missing:
        st.warning("⚠️ อาจลืม import โมดูล: " + ", ".join(missing))
    else:
        st.success("✔️ ไม่พบโมดูลที่ลืม")

    # 5) Code Explanation
    st.header("📘 อธิบายโค้ด")
    st.info(explain_code(code))

    # 6) Auto Fix
    st.header("🛠️ โค้ดที่ระบบช่วยแก้ให้ (เบื้องต้น)")
    fixed_code = basic_auto_fix(code)
    st.code(fixed_code, language="python")

    st.success("เสร็จเรียบร้อย! 🎉")


