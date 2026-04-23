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

# --- ربط مباشر بالمفتاح ---
API_KEY = "AIzaSyDWR3DIkMHgZZqh585X32H1I6j7v9SZaes"
genai.configure(api_key=API_KEY)

# دالة لاختيار الموديل المتاح
def get_model():
    # بنجرب الموديلات المتاحة حالياً بالترتيب
    for model_name in ['gemini-1.5-flash', 'gemini-pro']:
        try:
            m = genai.GenerativeModel(model_name)
            # تجربة بسيطة للتأكد من العمل
            return m
        except:
            continue
    return None

model = get_model()

# --- واجهة التطبيق ---
st.title("🚀 Intro Code")
st.markdown("### المساعد الذكي لشركة إنترو كود")

name = st.text_input("الأسم الكريم:")
phone = st.text_input("رقم الواتساب:")
service = st.selectbox("الخدمة المطلوبة:", ["برمجة مواقع", "تصميم جرافيك", "تحليل بيانات"])
msg = st.text_area("تفاصيل استفسارك:")

if st.button("عرض الرد الفوري ✨"):
    if name and msg:
        if model:
            with st.spinner('جاري معالجة طلبك...'):
                try:
                    prompt = f"أنت خبير مبيعات في شركة Intro Code. العميل {name} مهتم بـ {service} ويقول: {msg}. اكتب رد احترافي ومقنع."
                    response = model.generate_content(prompt)
                    
                    st.markdown("---")
                    st.success(response.text)

                    # حفظ البيانات محلياً على السيرفر
                    new_row = {"Date": datetime.now(), "Name": name, "Phone": phone, "Service": service}
                    pd.DataFrame([new_row]).to_csv("leads.csv", mode='a', header=not os.path.exists("leads.csv"), index=False)
                except Exception as e:
                    st.error(f"خطأ في توليد الرد: {e}")
        else:
            st.error("السيرفر لا يدعم الموديلات الحالية، تأكد من صلاحية المفتاح.")
    else:
        st.warning("برجاء إكمال البيانات.")

st.markdown("<br><p style='text-align: center; color: gray;'>© 2026 Intro Code</p>", unsafe_allow_html=True)