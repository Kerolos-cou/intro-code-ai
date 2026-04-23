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
        width: 100%;
        border-radius: 20px;
        height: 3.5em;
        background: linear-gradient(45deg, #007bff, #00d4ff);
        color: white;
        font-weight: bold;
        border: none;
    }
    .stTextArea textarea, .stTextInput input { border-radius: 10px; background-color: #1a1c23; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- إعداد الذكاء الاصطناعي ---
try:
    # جلب المفتاح من Secrets
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("تنبيه: تأكد من إضافة GEMINI_API_KEY في إعدادات Secrets")

# --- واجهة التطبيق ---
st.title("🚀 Intro Code")
st.markdown("### المساعد الذكي لخدمات البرمجة والتصميم")

with st.container():
    client_name = st.text_input("الأسم الكريم:")
    client_phone = st.text_input("رقم الواتساب:")
    client_task = st.selectbox("الخدمة المطلوبة:", ["برمجة مواقع", "تصميم جرافيك", "تحليل بيانات"])
    customer_msg = st.text_area("تفاصيل استفسارك:", height=100)

    if st.button("الحصول على عرض سعر فوري ✨"):
        if client_name and customer_msg:
            with st.spinner('جاري تحليل طلبك وتحضير العرض...'):
                try:
                    # البرومبت الاحترافي
                    prompt = f"أنت مساعد مبيعات في Intro Code. العميل {client_name} مهتم بـ {client_task} ويقول: {customer_msg}. اكتب رد بيعي جذاب واحترافي يوضح أن أسعارنا تبدأ من 5000ج مع ضمان وجودة عالية."
                    
                    response = model.generate_content(prompt)
                    ai_reply = response.text
                    
                    # عرض الرد
                    st.markdown("---")
                    st.success(ai_reply)

                    # حفظ البيانات في ملف CSV
                    new_row = {
                        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Name": client_name,
                        "Phone": client_phone,
                        "Service": client_task,
                        "Message": customer_msg[:50]
                    }
                    df = pd.DataFrame([new_row])
                    df.to_csv("leads.csv", mode='a', header=not os.path.exists("leads.csv"), index=False, encoding='utf-8-sig')
                    
                except Exception as e:
                    st.error(f"حدث خطأ فني: {e}")
        else:
            st.warning("برجاء ملء البيانات الأساسية (الاسم والرسالة).")

st.markdown("<br><p style='text-align: center; color: gray;'>© 2026 Intro Code - جميع الحقوق محفوظة</p>", unsafe_allow_html=True)