import streamlit as st
import google.generativeai as genai
import pandas as pd
import os
from datetime import datetime

# --- إعدادات الواجهة ---
st.set_page_config(page_title="Intro Code | AI 2026", page_icon="🚀")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button {
        width: 100%; border-radius: 20px; height: 3.5em;
        background: linear-gradient(45deg, #007bff, #00d4ff);
        color: white; font-weight: bold; border: none;
    }
    .stTextArea textarea, .stTextInput input { border-radius: 10px; background-color: #1a1c23; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- الربط بأحدث موديل متاح في حسابك (Gemini 3) ---
API_KEY = "AIzaSyDWR3DIkMHgZZqh585X32H1I6j7v9SZaes"

try:
    genai.configure(api_key=API_KEY)
    # استخدمنا الموديل رقم 22 في القائمة بتاعتك لأنه الأحدث والأنسب
    model = genai.GenerativeModel('gemini-3-flash-preview')
except Exception as e:
    st.error(f"خطأ في الاتصال: {e}")

st.title("🚀 Intro Code")
st.markdown("### المساعد الذكي (إصدار 2026)")

name = st.text_input("الأسم الكريم:")
service = st.selectbox("الخدمة:", ["برمجة مواقع", "تصميم جرافيك", "تحليل بيانات"])
msg = st.text_area("تفاصيل استفسارك:")

if st.button("الحصول على رد فوري ⚡"):
    if name and msg:
        with st.spinner('جاري استخدام طاقة Gemini 3 للرد عليك...'):
            try:
                prompt = f"أنت مساعد مبيعات في Intro Code. رد على {name} بخصوص {service}. طلبه: {msg}. اكتب رد احترافي ومقنع جداً."
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.success(response.text)
                
                # حفظ البيانات
                new_row = {"Date": datetime.now(), "Name": name, "Service": service}
                pd.DataFrame([new_row]).to_csv("leads.csv", mode='a', header=not os.path.exists("leads.csv"), index=False)
                
            except Exception as e:
                st.error(f"حدث خطأ غير متوقع: {e}")
    else:
        st.warning("كمل بياناتك يا وحش")