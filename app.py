from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import pdfplumber
import spacy
import re
from spacy.lang.en.stop_words import STOP_WORDS

# Common skill list (you can expand this)
SKILL_LIST = [
    'python', 'java', 'c++', 'html', 'css', 'javascript', 'sql',
    'react', 'node', 'django', 'flask', 'git', 'github', 'linux',
    'excel', 'powerpoint', 'word', 'nlp', 'machine learning',
    'deep learning', 'tensorflow', 'pandas', 'numpy', 'matplotlib',
    'seaborn', 'data analysis', 'data visualization', 'communication',
    'teamwork', 'problem solving', 'leadership', 'time management'
]


# Load spaCy model once
nlp = spacy.load("en_core_web_sm")
# Load sentence-transformers model
embedder = SentenceTransformer('all-MiniLM-L6-v2')


def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # remove special characters and numbers
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if token.text not in STOP_WORDS and not token.is_punct and not token.is_space]
    return " ".join(tokens)

def extract_skills(text, skill_list):
    text = text.lower()
    found_skills = [skill for skill in skill_list if skill in text]
    return list(set(found_skills))



st.set_page_config(page_title="Smart Resume Screener", layout="centered")

st.markdown("<h1 style='text-align: center; color: darkblue;'>🧠 Smart Resume Screener</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

st.title("📄 Smart Resume Screener")
st.markdown("Upload a **Resume PDF** and a **Job Description PDF** to begin.")

# File uploaders
resume_files = st.file_uploader("Upload Resumes (PDF)", type=["pdf"], accept_multiple_files=True)

jd_file = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

if resume_files and jd_file:
    st.success("✅ Files uploaded successfully!")

    jd_text = extract_text_from_pdf(jd_file)
    preprocessed_jd = preprocess_text(jd_text)

    # Show JD text
    with st.expander("🧼 Cleaned Job Description Text"):
        st.write(preprocessed_jd)

    jd_embedding = embedder.encode([preprocessed_jd])[0]
    jd_skills = extract_skills(preprocessed_jd, SKILL_LIST)

    results = []

    for resume_file in resume_files:
        resume_text = extract_text_from_pdf(resume_file)
        preprocessed_resume = preprocess_text(resume_text)
        resume_embedding = embedder.encode([preprocessed_resume])[0]

        similarity_score = cosine_similarity([resume_embedding], [jd_embedding])[0][0] * 100

        resume_skills = extract_skills(preprocessed_resume, SKILL_LIST)

        matched_skills = list(set(resume_skills) & set(jd_skills))
        missing_skills = list(set(jd_skills) - set(resume_skills))

        skill_match_percent = (len(matched_skills) / len(jd_skills)) * 100 if jd_skills else 0.0

        results.append({
            "Resume Name": resume_file.name,
            "Match %": round(similarity_score, 2),
            "Skill Match %": round(skill_match_percent, 2),
            "Matched Skills": ", ".join(matched_skills),
            "Missing Skills": ", ".join(missing_skills),
        })

    # Display all results in a sorted table
    st.subheader("📊 Ranked Resume Results")
    
    sorted_results = sorted(results, key=lambda x: x["Match %"], reverse=True)
    best_resume = sorted_results[0]
    st.success(f"🏆 Best Match: **{best_resume['Resume Name']}** with {best_resume['Match %']}% match")

    st.dataframe(sorted_results)
    import pandas as pd

    # Convert to DataFrame
    df = pd.DataFrame(sorted_results)

    # Download button
    st.download_button(
        label="⬇️ Download Results as CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="ranked_resumes.csv",
        mime="text/csv"
    )




else:
    st.info("Please upload both Resume and Job Description PDFs.")
