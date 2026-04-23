import streamlit as st
import google.generativeai as genai
import pandas as pd
from datetime import datetime
import os

# --- إعدادات الواجهة الاحترافية ---
st.set_page_config(page_title="Intro Code | تواصل معنا", page_icon="🚀", layout="centered")

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
        cursor: pointer;
    }
    .stTextArea textarea { border-radius: 15px; background-color: #1a1c23; color: white; }
    .stTextInput input { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- ربط الذكاء الاصطناعي (مباشرة وبدون تعقيد) ---
try:
    # قراءة المفتاح من الـ Secrets أونلاين
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"خطأ في إعدادات المفتاح السري: {e}")

# --- واجهة شركة Intro Code ---
st.title("🚀 Intro Code")
st.markdown("### أهلاً بك في منصتنا الذكية")
st.write("أدخل بياناتك وسيقوم المساعد الذكي بالرد على استفسارك في ثوانٍ.")

client_name = st.text_input("الأسم الكريم:")
client_phone = st.text_input("رقم الواتساب:")
client_task = st.selectbox("الخدمة المطلوبة:", ["برمجة مواقع", "تصميم جرافيك", "تحليل بيانات"])
customer_msg = st.text_area("تفاصيل استفسارك:", height=120)

if st.button("عرض الرد الفوري ⚡"):
    if client_name and customer_msg:
        with st.spinner('جاري تحضير الرد...'):
            # برومبت مباشر للحصول على أفضل نتيجة
            prompt = f"""
            أنت مساعد مبيعات في شركة Intro Code. 
            العميل {client_name} مهتم بـ {client_task} ويقول: {customer_msg}.
            اكتب له رداً احترافياً ومقنعاً يبدأ بـ "مرحباً يا {client_name}" 
            ويوضح له تميزنا في تقديم خدمات {client_task} بأسعار تبدأ من 5000 جنيه وضمان 3 شهور.
            """
            try:
                response = model.generate_content(prompt)
                ai_reply = response.text
                
                st.markdown("---")
                st.success(ai_reply)

                # حفظ البيانات في ملف leads.csv (بيتحفظ أونلاين في السيرفر)
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
                st.error("نعتذر، يبدو أن هناك ضغطاً على السيرفر حالياً. يرجى المحاولة بعد لحظات.")
    else:
        st.warning("برجاء إدخال الاسم وتفاصيل الرسالة.")