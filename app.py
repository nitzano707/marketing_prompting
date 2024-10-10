import streamlit as st
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

@st.cache_resource
def load_model():
    model_name = "MBZUAI/LaMini-Flan-T5-783M"
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return pipeline('text2text-generation', model=model, tokenizer=tokenizer)

generator = load_model()

st.title("מחולל תוכן שיווקי למוסדות חינוך")

institution_name = st.text_input("שם המוסד החינוכי")
institution_type = st.selectbox("סוג המוסד", ["גן ילדים", "בית ספר יסודי", "חטיבת ביניים", "תיכון", "מכללה", "אוניברסיטה"])
unique_features = st.text_area("מאפיינים ייחודיים של המוסד")
target_audience = st.text_input("קהל היעד")

def generate_content(institution_name, institution_type, unique_features, target_audience):
    prompt = f"""משימה: צור תוכן שיווקי קצר בעברית עבור מוסד חינוכי.

מידע:
- שם המוסד: {institution_name}
- סוג המוסד: {institution_type}
- מאפיינים ייחודיים: {unique_features}
- קהל היעד: {target_audience}

הנחיות: כתוב פסקה קצרה ומושכת שמתארת את המוסד החינוכי, מדגישה את יתרונותיו הייחודיים ופונה לקהל היעד המתאים. השתמש בשפה עשירה ומשכנעת בעברית.

תוכן שיווקי:"""

    response = generator(prompt, max_length=300, num_return_sequences=1)
    return response[0]['generated_text']

if st.button("צור תוכן שיווקי"):
    if institution_name and institution_type and unique_features and target_audience:
        try:
            content = generate_content(institution_name, institution_type, unique_features, target_audience)
            st.subheader("תוכן שיווקי מוצע:")
            st.write(content)
        except Exception as e:
            st.error(f"אירעה שגיאה בעת יצירת התוכן: {str(e)}")
    else:
        st.error("אנא מלא את כל השדות")
