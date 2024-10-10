import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForMaskedLM

# Initialize the model and tokenizer
@st.cache_resource
def load_model():
    model_name = "Onlplab/alephbert-base"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForMaskedLM.from_pretrained(model_name)
    return pipeline('fill-mask', model=model, tokenizer=tokenizer)

nlp = load_model()

st.title("מחולל תוכן שיווקי למוסדות חינוך")

institution_name = st.text_input("שם המוסד החינוכי")
institution_type = st.selectbox("סוג המוסד", ["גן ילדים", "בית ספר יסודי", "חטיבת ביניים", "תיכון", "מכללה", "אוניברסיטה"])
unique_features = st.text_area("מאפיינים ייחודיים של המוסד")
target_audience = st.text_input("קהל היעד")

def generate_content(institution_name, institution_type, unique_features, target_audience):
    prompt = f"{institution_name} הוא {institution_type} מוביל המציע [MASK]. "
    result = nlp(prompt)
    first_part = result[0]['sequence']
    
    prompt2 = f"{first_part} המוסד מתאפיין ב{unique_features} ומיועד ל[MASK]."
    result2 = nlp(prompt2)
    second_part = result2[0]['sequence']
    
    final_text = f"{second_part} אנו מזמינים את {target_audience} להצטרף אלינו ולחוות חינוך ברמה הגבוהה ביותר."
    return final_text

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
