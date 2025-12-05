import streamlit as st

st.set_page_config(page_title="Basic Error Checker", page_icon="🛠️", layout="wide")

st.title("🛠️ เครื่องหาข้อผิดพลาดเบื้องต้น (Basic Error Checker)")
st.write("ตรวจความผิดพลาดในโค้ด Python แบบง่ายๆ")

code = st.text_area("พิมพ์โค้ด Python ที่ต้องการตรวจสอบ:", height=250)

check_btn = st.button("🔍 ตรวจโค้ด")

def check_brackets(text):
    brackets = {
        "(": ")", 
        "[": "]", 
        "{": "}"
    }
    stack = []
    for i, char in enumerate(text):
        if char in brackets:
            stack.append((char, i))
        elif char in brackets.values():
            if not stack or brackets[stack[-1][0]] != char:
                return f"❌ วงเล็บปิดเกินที่ index {i}"
            stack.pop()
    if stack:
        return f"❌ วงเล็บเปิดยังไม่ปิดที่ index {stack[-1][1]}"
    return "✔️ วงเล็บถูกต้องครบถ้วน"

if check_btn:
    if not code.strip():
        st.warning("กรุณาใส่โค้ดก่อนตรวจนะครับ 🙂")
    else:
        st.subheader("ผลการตรวจสอบ")

        # --- ตรวจ Syntax ---
        try:
            compile(code, "<string>", "exec")
            st.success("✔️ Syntax ปกติ ไม่พบข้อผิดพลาด")
        except Exception as e:
            st.error(f"❌ พบ Syntax Error: `{type(e).__name__}` → {e}")

        # --- ตรวจวงเล็บ ---
        st.write("### 🔎 ตรวจวงเล็บ")
        st.write(check_brackets(code))

        # --- ตรวจตัวแปรที่ใช้งานแต่ไม่ประกาศ ---
        st.write("### 🔎 ตรวจตัวแปรที่อาจไม่ถูกประกาศ")
        lines = code.split("\n")
        declared = set()
        used = set()

        for line in lines:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                var = line.split("=")[0].strip()
                if var.isidentifier():
                    declared.add(var)
            for token in line.split():
                if token.isidentifier():
                    used.add(token)

        undefined_vars = used - declared

        if undefined_vars:
            st.warning(f"⚠️ ตัวแปรที่อาจยังไม่ถูกประกาศ: {', '.join(undefined_vars)}")
        else:
            st.info("✔️ ไม่พบตัวแปรที่ใช้งานก่อนประกาศ")

        # --- ตรวจ import ที่อาจลืม ---
        st.write("### 🔎 ตรวจโมดูลที่อาจถูกเรียกใช้แต่ไม่ถูก import")
        common_modules = ["json", "math", "random", "os"]
        missing_imports = []

        for m in common_modules:
            if f"{m}." in code and f"import {m}" not in code:
                missing_imports.append(m)

        if missing_imports:
            st.warning(f"⚠️ อาจลืม import โมดูล: {', '.join(missing_imports)}")
        else:
            st.info("✔️ ไม่พบโมดูลที่ลืม import")
