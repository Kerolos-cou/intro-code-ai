import streamlit as st
import google.generativeai as genai
import pandas as pd
import os
from datetime import datetime

# --- إعدادات الواجهة ---
st.set_page_config(page_title="Intro Code | AI", page_icon="🚀", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    h1, h3 { text-align: center; color: #00d4ff; }
    .stButton>button {
        width: 100%; border-radius: 20px; height: 3.5em;
        background: linear-gradient(45deg, #007bff, #00d4ff);
        color: white; font-weight: bold; border: none;
    }
    .stTextArea textarea, .stTextInput input { border-radius: 10px; background-color: #1a1c23; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- إعداد الذكاء الاصطناعي (أكثر استقراراً) ---
def initialize_ai():
    try:
        if "GEMINI_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            # هنستخدم gemini-pro لأنه الأكثر استقراراً حالياً لتجنب خطأ الـ 404
            return genai.GenerativeModel('gemini-pro')
        else:
            st.error("المفتاح السري (API Key) غير موجود في الإعدادات.")
            return None
    except Exception as e:
        st.error(f"خطأ في الاتصال: {e}")
        return None

model = initialize_ai()

# --- واجهة التطبيق ---
st.title("🚀 Intro Code")
st.markdown("### المساعد الذكي لخدمات البرمجة والتصميم")

name = st.text_input("الأسم الكريم:")
phone = st.text_input("رقم الواتساب:")
service = st.selectbox("الخدمة المطلوبة:", ["برمجة مواقع", "تصميم جرافيك", "تحليل بيانات"])
msg = st.text_area("تفاصيل استفسارك:", height=100)

if st.button("الحصول على عرض سعر فوري ✨"):
    if name and msg and model:
        with st.spinner('جاري تحضير العرض...'):
            try:
                # برومبت يركز على الهوية الاحترافية لشركة Intro Code
                prompt = (f"أنت خبير مبيعات في شركة Intro Code. العميل {name} يسأل عن {service}. "
                         f"رسالته هي: {msg}. اكتب رد بيعي قصير، مقنع، واحترافي.")
                
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.success(response.text)

                # حفظ البيانات
                new_row = {"Date": datetime.now(), "Name": name, "Phone": phone, "Service": service}
                pd.DataFrame([new_row]).to_csv("leads.csv", mode='a', header=not os.path.exists("leads.csv"), index=False)
                
            except Exception as e:
                st.error("السيرفر مشغول حالياً، يرجى إعادة الضغط على الزر.")
    else:
        st.warning("برجاء إدخال البيانات المطلوبة.")

st.markdown("<br><p style='text-align: center; color: gray;'>© 2026 Intro Code</p>", unsafe_allow_html=True)