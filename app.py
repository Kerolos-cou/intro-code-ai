import streamlit as st
import google.generativeai as genai
import pandas as pd
import os

# --- إعدادات الواجهة ---
st.set_page_config(page_title="Intro Code AI", page_icon="🚀")

# --- الربط المباشر (الضربة القاضية) ---
API_KEY = "AIzaSyDWR3DIkMHgZZqh585X32H1I6j7v9SZaes"

try:
    genai.configure(api_key=API_KEY)
    # استخدمنا gemini-pro مباشرة لتجنب مشاكل الـ flash في الـ beta
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"خطأ في الربط: {e}")

st.title("🚀 Intro Code")
st.markdown("### مساعد المبيعات الذكي")

name = st.text_input("الأسم:")
service = st.selectbox("الخدمة:", ["برمجة مواقع", "تصميم جرافيك", "تحليل بيانات"])
msg = st.text_area("تفاصيل طلبك:")

if st.button("إرسال ✨"):
    if name and msg:
        with st.spinner('جاري تحضير الرد...'):
            try:
                # طلب بسيط جداً لضمان عدم حدوث تعارض في الإصدارات
                prompt = f"أنت مساعد مبيعات في شركة Intro Code. العميل {name} يسأل عن {service}. رسالته: {msg}. اكتب رد بيعي احترافي ومقنع."
                response = model.generate_content(prompt)
                
                if response.text:
                    st.markdown("---")
                    st.success(response.text)
                    
                    # حفظ البيانات
                    try:
                        new_data = pd.DataFrame([{"Name": name, "Service": service}])
                        new_data.to_csv("leads.csv", mode='a', header=not os.path.exists("leads.csv"), index=False)
                    except:
                        pass
                else:
                    st.error("السيرفر لم يرسل رداً، جرب مرة أخرى.")
            except Exception as e:
                # لو لسه فيه 404، هنطبع لستة الموديلات المتاحة لحسابك عشان نختار منها
                st.error(f"عذراً، حدث خطأ فني: {e}")
                if "404" in str(e):
                    st.info("جاري فحص الموديلات المتاحة في حسابك...")
                    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    st.write("الموديلات المتاحة لك هي:", models)
    else:
        st.warning("كمل بياناتك يا هندسة")