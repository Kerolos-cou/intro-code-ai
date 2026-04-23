import streamlit as st
import google.generativeai as genai
import pandas as pd
from datetime import datetime
import os

# --- إعدادات الواجهة ---
st.set_page_config(page_title="Intro Code | تواصل معنا", page_icon="✉️", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
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
    .stTextArea textarea { border-radius: 15px; background-color: #1a1c23; color: white; }
    .stTextInput input { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- إعداد الذكاء الاصطناعي ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("API Key missing!")

# --- واجهة العميل ---
st.title("🚀 Intro Code")
st.markdown("### أهلاً بك في شركة إنترو كود")

client_name = st.text_input("الأسم الكريم:")
client_phone = st.text_input("رقم الواتساب:")
client_task = st.selectbox("الخدمة المطلوبة:", ["برمجة مواقع", "تصميم جرافيك", "تحليل بيانات"])
customer_msg = st.text_area("تفاصيل استفسارك:", height=120)

if st.button("عرض الرد الفوري ⚡"):
    if client_name and customer_msg:
        with st.spinner('جاري معالجة طلبك...'):
            # طلب الرد كنص مباشر لضمان عدم حدوث خطأ
            prompt = f"""
            أنت مساعد مبيعات محترف في شركة Intro Code. 
            العميل {client_name} مهتم بـ {client_task} ويقول: {customer_msg}.
            اكتب رد بيعي جذاب، احترافي، ومقنع جداً يشجعه على التعاقد معنا.
            اجعل الرد يبدأ بـ "مرحباً يا {client_name}".
            """
            try:
                response = model.generate_content(prompt)
                ai_reply = response.text
                
                st.markdown("---")
                st.success(ai_reply)

                # حفظ البيانات
                new_row = {
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Name": client_name,
                    "Phone": client_phone,
                    "Service": client_task
                }
                pd.DataFrame([new_row]).to_csv("leads.csv", mode='a', header=not os.path.exists("leads.csv"), index=False, encoding='utf-8-sig')
                
            except Exception as e:
                st.error("حدث ضغط بسيط، جرب تضغط مرة تانية.")
    else:
        st.warning("برجاء ملء البيانات.")