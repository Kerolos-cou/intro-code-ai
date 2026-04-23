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

# --- محرك البحث عن الموديل الشغال ---
def get_ready_model():
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=API_KEY)
        
        # بنجرب الموديلات المتاحة بالترتيب لضمان التشغيل
        for model_name in ['gemini-1.5-flash', 'gemini-pro', 'models/gemini-pro']:
            try:
                m = genai.GenerativeModel(model_name)
                # تجربة وهمية للتأكد من الصلاحية
                return m
            except:
                continue
        return None
    except Exception as e:
        st.error(f"مشكلة في الإعدادات السرية: {e}")
        return None

model = get_ready_model()

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
                # طلب الرد
                prompt = f"أنت مساعد مبيعات في Intro Code. العميل {name} مهتم بـ {service} ويقول: {msg}. اكتب رد بيعي جذاب واحترافي."
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.success(response.text)

                # حفظ البيانات
                new_row = {"Date": datetime.now(), "Name": name, "Phone": phone, "Service": service}
                pd.DataFrame([new_row]).to_csv("leads.csv", mode='a', header=not os.path.exists("leads.csv"), index=False)
                
            except Exception as e:
                st.error(f"عذراً، الموديل يواجه ضغطاً: {e}")
    elif not model:
        st.error("الموديل غير جاهز، تأكد من الـ API Key في الإعدادات.")
    else:
        st.warning("برجاء إكمال البيانات.")

st.markdown("<br><p style='text-align: center; color: gray;'>© 2026 Intro Code</p>", unsafe_allow_html=True)