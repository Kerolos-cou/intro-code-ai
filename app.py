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

# --- إعداد الذكاء الاصطناعي (نسخة مرنة) ---
def load_model():
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=API_KEY)
        # محاولة تشغيل أحدث موديل، ولو فشل يشغل البرو
        try:
            return genai.GenerativeModel('gemini-1.5-flash')
        except:
            return genai.GenerativeModel('gemini-pro')
    except Exception as e:
        st.error(f"خطأ في الإعدادات: {e}")
        return None

model = load_model()

# --- واجهة التطبيق ---
st.title("🚀 Intro Code")
st.markdown("### المساعد الذكي لخدمات البرمجة والتصميم")

client_name = st.text_input("الأسم الكريم:")
client_phone = st.text_input("رقم الواتساب:")
client_task = st.selectbox("الخدمة المطلوبة:", ["برمجة مواقع", "تصميم جرافيك", "تحليل بيانات"])
customer_msg = st.text_area("تفاصيل استفسارك:", height=100)

if st.button("الحصول على عرض سعر فوري ✨"):
    if client_name and customer_msg and model:
        with st.spinner('جاري تحضير العرض...'):
            try:
                prompt = f"أنت مساعد مبيعات في Intro Code. العميل {client_name} مهتم بـ {client_task} ويقول: {customer_msg}. اكتب رد بيعي جذاب واحترافي."
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.success(response.text)

                # حفظ البيانات
                new_row = {"Date": datetime.now(), "Name": client_name, "Phone": client_phone, "Service": client_task}
                pd.DataFrame([new_row]).to_csv("leads.csv", mode='a', header=not os.path.exists("leads.csv"), index=False)
                
            except Exception as e:
                st.error(f"عذراً، الموديل يواجه صعوبة حالياً: {e}")
    else:
        st.warning("تأكد من إدخال البيانات.")

st.markdown("<br><p style='text-align: center; color: gray;'>© 2026 Intro Code</p>", unsafe_allow_html=True)