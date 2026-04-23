import streamlit as st
import google.generativeai as genai
import pandas as pd
import os
from datetime import datetime

# --- إعدادات الواجهة ---
st.set_page_config(page_title="Intro Code AI", page_icon="🚀")

# --- دالة الربط العبقرية ---
def get_working_model():
    try:
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
            # إجبار المكتبة على استخدام الإصدار المستقر
            genai.configure(api_key=api_key, transport='grpc')
            
            # قائمة بكل الاحتمالات الممكنة للموديلات
            potential_models = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
            
            for m_name in potential_models:
                try:
                    model = genai.GenerativeModel(model_name=m_name)
                    # تجربة اختبار بسيطة جداً
                    model.generate_content("test", generation_config={"max_output_tokens": 1})
                    return model
                except:
                    continue
        return None
    except:
        return None

model = get_working_model()

st.title("🚀 Intro Code")
st.markdown("### نظام الرد الذكي")

name = st.text_input("الأسم:")
service = st.selectbox("الخدمة:", ["برمجة مواقع", "تصميم جرافيك", "تحليل بيانات"])
msg = st.text_area("تفاصيل الطلب:")

if st.button("إرسال الطلب ✨"):
    if name and msg:
        if model:
            with st.spinner('جاري التواصل مع الذكاء الاصطناعي...'):
                try:
                    prompt = f"أنت خبير مبيعات في Intro Code. رد على {name} بخصوص {service}. طلبه: {msg}"
                    response = model.generate_content(prompt)
                    st.markdown("---")
                    st.success(response.text)
                except Exception as e:
                    st.error(f"خطأ في توليد الرد: {str(e)}")
        else:
            st.error("السيرفر غير قادر على تحديد الموديل المناسب حالياً. تأكد من صحة الـ API Key في الإعدادات.")
    else:
        st.warning("كمل بياناتك يا هندسة")