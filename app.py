import streamlit as st
from google import genai
import os

# ڕێکخستنی سەرەتایی لاپەڕەی وێبەکە
st.set_page_config(page_title="RYZEN AI Web", page_icon="🤖", layout="centered")

st.title("🤖 RYZEN AI Web")
st.caption("🚀 وێبسایتی تایبەت بە ژیریی دەستکردی RYZEN - بە هێزی Gemini 2.5 Flash")
st.markdown("---")

# دروستکردنی بەشێک لە لای چەپ (Sidebar) بۆ ئەوەی خەڵک کلیل دابنێت ئەگەر کۆتا تەواو بوو
st.sidebar.title("🔑 ڕێکخستنی کلیل")
user_api_key = st.sidebar.text_input("کلیلی API تایبەت بە خۆت لێرە دابنێ (ئارەزوومەندانه):", type="password")

# دیاریکردنی کلیلەکە (ئەگەر بەکارهێنەر کلیلەکەی خۆی دانا ئەوە بەکاردێت، ئەگەر نا ئەوەی تۆ بەکاردێت)
if user_api_key:
    api_key = user_api_key
elif "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = "AQ.Ab8RN6L2lEx1MYrlumEnbC9xINpzkr0_F4o0QpfIMyUVfnriCA"

# دروستکردنی کلاینتی گۆگڵ بەو کلیلەی دیاری کراوە
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"❌ کێشەیەک لە کتبێخانەی گوگل هەیە: {e}")

# دروستکردنی میمۆری بۆ چاتەکە
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "سڵاو برام! من ژیریی دەستکردی RYZEN AI لۆ وێبم. چۆن دەتوانم یارمەتیت بدەم؟"}
    ]

# پیشاندانی نامەکانی ناو چاتەکە
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# وەرگرتنی نامەی نوێ لە بەکارهێنەر
if user_input := st.chat_input("نامەیەک لێرە بنووسە..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # ناردنی نامەکە بۆ گوگل بە مۆدێلی دروستی ٢.٥
    with st.chat_message("assistant"):
        with st.spinner("خەریکم بیر دەکەمەوە..."):
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=user_input,
                )
                answer = response.text
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                # ئەگەر کۆتا تەواو بووبوو، ڕێنماییان دەکات چی بکەن
                if "429" in str(e) or "QUOTA_EXCEEDED" in str(e):
                    st.error("⚠️ کۆتای خۆڕایی ئەمڕۆی پڕۆژەکە تەواو بووە! تکایە لە مینیوی لای چەپ (Sidebar) کلیلی API تایبەت بە خۆت دابنێ بۆ ئەوەی بەردەوام بیت.")
                else:
                    st.error(f"هەڵەیەک ڕوویدا: {e}")