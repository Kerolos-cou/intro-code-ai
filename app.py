import streamlit as st
import google.generativeai as genai
import json
import pandas as pd
from datetime import datetime
import os

# --- إعدادات الواجهة الاحترافية لـ Intro Code ---
st.set_page_config(page_title="Intro Code | تواصل معنا", page_icon="✉️", layout="centered")

# تصميم الهوية البصرية (Branding)
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

# --- إعداد الذكاء الاصطناعي (باستخدام Secrets للأمان) ---
try:
    # التعديل الأهم: قراءة المفتاح من إعدادات Streamlit Cloud السرية
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("خطأ: لم يتم العثور على API Key في الإعدادات السرية (Secrets).")

def get_working_model():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    for target in ['models/gemini-1.5-flash', 'models/gemini-pro']:
        if target in available_models: return genai.GenerativeModel(target)
    return genai.GenerativeModel(available_models[0])

model = get_working_model()

# --- واجهة العميل ---
st.title("🚀 Intro Code")
st.markdown("### أهلاً بك في شركة إنترو كود")
st.write("نسعد باستلام استفسارك، سيقوم نظامنا الذكي بتزويدك بالمعلومات الأولية فوراً.")

client_name = st.text_input("الأسم الكريم:")
client_phone = st.text_input("رقم الواتساب:")
client_task = st.selectbox("الخدمة المطلوبة:", ["برمجة مواقع", "تصميم جرافيك", "تحليل بيانات"])
customer_msg = st.text_area("تفاصيل استفسارك:", height=120)

if st.button("عرض الرد الفوري ⚡"):
    if client_name and customer_msg:
        with st.spinner('جاري معالجة طلبك...'):
            prompt = f"""
            أنت مساعد مبيعات في Intro Code. معلوماتنا: برمجة مواقع، تصميم جرافيك، تحليل بيانات. الأسعار من 5000ج.
            العميل {client_name} يسأل عن {client_task}: "{customer_msg}".
            اكتب رد بيعي مقنع واحترافي يوضح العروض والضمان.
            رد بـ JSON فقط فيه مفتاح واحد اسمه suggested_reply.
            """
            try:
                response = model.generate_content(prompt)
                res_text = response.text.strip().replace('```json', '').replace('```', '')
                res = json.loads(res_text)
                ai_reply = res.get('suggested_reply')

                # عرض الرد للعميل
                st.markdown("---")
                st.success(f"**مرحباً يا {client_name}، إليك تفاصيل عرضنا:**\n\n{ai_reply}")

                # حفظ البيانات في ملف leads.csv في الخلفية
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
                st.error("نعتذر، حدث خطأ أثناء تجهيز الرد. يرجى المحاولة مرة أخرى.")
    else:
        st.warning("برجاء ملء جميع الخانات المطلوبة.")