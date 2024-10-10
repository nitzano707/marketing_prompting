import streamlit as st
import requests

# Set your Hugging Face API key
API_TOKEN = st.secrets["huggingface_api_token"]

def query(payload):
    API_URL = "https://api-inference.huggingface.co/models/gpt2"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

st.title("מחולל תוכן שיווקי למוסדות חינוך")

institution_name = st.text_input("שם המוסד החינוכי")
institution_type = st.selectbox("סוג המוסד", ["גן ילדים", "בית ספר יסודי", "חטיבת ביניים", "תיכון", "מכללה", "אוניברסיטה"])
unique_features = st.text_area("מאפיינים ייחודיים של המוסד")
target_audience = st.text_input("קהל היעד")

if st.button("צור תוכן שיווקי"):
    if institution_name and institution_type and unique_features and target_audience:
        prompt = f"Write a short and engaging message to market {institution_type} named {institution_name}. The institution is characterized by: {unique_features}. The target audience is: {target_audience}."
        
        output = query({
            "inputs": prompt,
            "parameters": {"max_length": 200}
        })
        
        if isinstance(output, list) and len(output) > 0 and "generated_text" in output[0]:
            st.subheader("תוכן שיווקי מוצע:")
            st.write(output[0]["generated_text"])
        else:
            st.error("אירעה שגיאה בעת יצירת התוכן. נסה שוב מאוחר יותר.")
    else:
        st.error("אנא מלא את כל השדות")
