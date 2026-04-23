import streamlit as st
import google.generativeai as genai
import pandas as pd
import os
from datetime import datetime

# --- إعدادات الواجهة ---
st.set_page_config(page_title="Intro Code AI", page_icon="🚀")

# --- محرك الذكاء الاصطناعي - النسخة المستقرة جداً ---
def start_ai():
    try:
        if "GEMINI_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            # هنستخدم إصدار 1.0 لأنه الأكثر استقراراً في السيرفرات حالياً
            return genai.GenerativeModel('gemini-1.0-pro')
        return None
    except:
        return None

model = start_ai()

st.title("🚀 Intro Code")
st.markdown("### نظام الرد الآلي الذكي")

name = st.text_input("الأسم:")
phone = st.text_input("الواتساب:")
service = st.selectbox("الخدمة:", ["برمجة مواقع", "تصميم جرافيك", "تحليل بيانات"])
msg = st.text_area("تفاصيل الطلب:")

if st.button("إرسال الطلب ✨"):
    if name and msg and model:
        with st.spinner('جاري الاتصال بالسيرفر...'):
            try:
                # طلب بسيط جداً لضمان الاستجابة
                prompt = f"أجب كخبير مبيعات في شركة Intro Code. العميل {name} يريد {service}. رسالته: {msg}. اكتب رد قصير ومحفز."
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.success(response.text)

                # حفظ البيانات (اختياري لو السيرفر سمح بالكتابة)
                try:
                    new_row = {"Date": datetime.now(), "Name": name, "Phone": phone, "Service": service}
                    pd.DataFrame([new_row]).to_csv("leads.csv", mode='a', header=not os.path.exists("leads.csv"), index=False)
                except:
                    pass
                
            except Exception as e:
                # هنا هيظهر لنا السبب الحقيقي للخطأ
                st.error(f"عذراً يا هندسة، السيرفر بيقول: {str(e)}")
    else:
        st.warning("تأكد من إدخال البيانات أو وجود الـ API Key")