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

# --- الربط بالمفتاح والموديل ---
API_KEY = "AIzaSyDRDIJOo4XpcSpaPQXHSBZVic04zQjEeEM"
genai.configure(api_key=API_KEY)
# استخدام الموديل اللي أثبت كفاءة في حسابك
model = genai.GenerativeModel('gemini-3-flash-preview')

st.title("🚀 Intro Code")
st.markdown("### المساعد الذكي لشركة إنترو كود")

# --- مدخلات البيانات ---
name = st.text_input("الأسم الكريم:")
phone = st.text_input("رقم الهاتف / واتساب:")
service = st.selectbox("الخدمة المطلوبة:", ["برمجة مواقع", "تصميم جرافيك", "تحليل بيانات"])
msg = st.text_area("تفاصيل استفسارك:")

if st.button("إرسال الطلب والحصول على رد فوري ⚡"):
    if name and phone and msg:
        with st.spinner('جاري معالجة طلبك وحفظ البيانات...'):
            try:
                # 1. توليد الرد الذكي
                prompt = f"أنت مساعد مبيعات في Intro Code. رد على {name} بخصوص {service}. طلبه: {msg}. اكتب رد احترافي ومقنع."
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.success(response.text)
                
                # 2. الحفظ التلقائي في ملف Excel (leads.csv)
                file_path = "leads.csv"
                new_data = {
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Customer Name": name,
                    "Phone Number": phone,
                    "Service Requested": service,
                    "Message": msg
                }
                
                df_new = pd.DataFrame([new_data])
                
                # لو الملف موجود ضيف عليه، لو مش موجود انشئه بالعناوين
                if os.path.isfile(file_path):
                    df_new.to_csv(file_path, mode='a', header=False, index=False, encoding='utf-8-sig')
                else:
                    df_new.to_csv(file_path, mode='w', header=True, index=False, encoding='utf-8-sig')
                
                st.info("✅ تم حفظ بياناتك بنجاح في سجل المبيعات.")
                
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
    else:
        st.warning("برجاء ملء جميع الحقول (الاسم، الهاتف، والرسالة).")

st.markdown("<br><p style='text-align: center; color: gray;'>© 2026 Intro Code - Powered by Gemini 3</p>", unsafe_allow_html=True)