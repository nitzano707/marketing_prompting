import streamlit as st
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
from huggingface_hub import InferenceApi

# שימוש במפתח ה-API מתוך secrets של Streamlit
api_key = st.secrets["HUGGINGFACEHUB_API_TOKEN"]

# טעינת מודל מ-Hugging Face
@st.cache_resource
def load_model():
    api = InferenceApi(repo_id="geonm/nllb-200-hebrew", token=api_key)
    return api

generator = load_model()

st.title("מחולל תוכן שיווקי למוסדות חינוך")

# קלט המשתמש
institution_name = st.text_input("שם המוסד החינוכי")
institution_type = st.selectbox("סוג המוסד", ["גן ילדים", "בית ספר יסודי", "חטיבת ביניים", "תיכון", "מכללה", "אוניברסיטה"])
unique_features = st.text_area("מאפיינים ייחודיים של המוסד")
target_audience = st.text_input("קהל היעד")
content_type = st.selectbox("סוג התוכן השיווקי", ["פוסט לווצאפ", "פוסט לפייסבוק", "תוכן לאתר אינטרנט"])

# פונקציה ליצירת פרומפט ושליחת השאילתא למודל
def generate_content(institution_name, institution_type, unique_features, target_audience, content_type):
    prompt = f"""משימה: צור {content_type} בעברית עבור מוסד חינוכי.
    
    מידע:
    - שם המוסד: {institution_name}
    - סוג המוסד: {institution_type}
    - מאפיינים ייחודיים: {unique_features}
    - קהל היעד: {target_audience}
    
    הנחיות: כתוב פסקה קצרה ומושכת שמתארת את המוסד החינוכי, מדגישה את יתרונותיו הייחודיים ופונה לקהל היעד המתאים. השתמש בשפה עשירה ומשכנעת בעברית.
    
    תוכן {content_type}:"""
    
    response = generator(inputs=prompt)
    return response[0]['generated_text']

# כפתור ליצירת התוכן
if st.button("צור תוכן שיווקי"):
    if institution_name and institution_type and unique_features and target_audience and content_type:
        try:
            content = generate_content(institution_name, institution_type, unique_features, target_audience, content_type)
            st.subheader("תוכן שיווקי מוצע:")
            st.write(content)
        except Exception as e:
            st.error(f"אירעה שגיאה בעת יצירת התוכן: {str(e)}")
    else:
        st.error("אנא מלא את כל השדות")
