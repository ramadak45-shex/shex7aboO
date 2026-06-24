import streamlit as st
from google import genai
import os

# ڕێکخستنی سەرەتایی لاپەڕەی وێبەکە (دەبێت هەمیشە لە سەرەتای کۆدەکە بێت)
st.set_page_config(page_title="RYZEN AI Web", page_icon="🤖", layout="centered")

# خوێندنەوەی کلیلی API لە ستریملێت بە شێوازێکی پارێزراو
if "GEMINI_API_KEY" in st.secrets:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
else:
    # ئەگەر لە سێرڤەر ڕێکنەخرابوو، لێرە کلیلەکەت دابنێ بۆ تاقیکردنەوەی ناوخۆیی (Local)
    os.environ["GEMINI_API_KEY"] = "AQ.Ab8RN6L2lEx1MYrlumEnbC9xINpzkr0_F4o0QpfIMyUVfnriCA"

try:
    client = genai.Client()
except Exception as e:
    st.error(f"❌ کێشەیەک لە کتبێخانەی گوگل هەیە: {e}")

st.title("🤖 RYZEN AI Web")
st.caption("🚀 وێبسایتی تایبەت بە ژیریی دەستکردی RYZEN - بە هێزی Gemini 2.5 Flash")
st.markdown("---")

# دروستکردنی میمۆری بۆ چاتەکە (بۆ ئەوەی نامەکانی پێشوو بیر نەچێت)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "سڵاو برام! من ژیریی دەستکردی RYZEN AI لۆ وێبم. چۆن دەتوانم یارمەتیت بدەم؟"}
    ]

# پیشاندانی نامەکانی ناو چاتەکە بە شێوازی جوان
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# وەرگرتنی نامەی نوێ لە بەکارهێنەر (Input Box)
if user_input := st.chat_input("نامەیەک لێرە بنووسە..."):
    # زیادکردنی نامەی بەکارهێنەر بۆ شاشەکە
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # ناردنی نامەکە بۆ گوگل و وەرگرتنی وەڵام
    with st.chat_message("assistant"):
        with st.spinner("خەریکم بیر دەکەمەوە..."):
            try:
                response = client.models.generate_content(
                    model="gemini-1.5-flash-002",
                    contents=user_input,
                )
                answer = response.text
                st.markdown(answer)
                # پاشەکەوتکردنی وەڵامی بۆتەکە لە میمۆریدا
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"هەڵەیەک ڕوویدا: {e}")