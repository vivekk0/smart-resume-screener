# smart-resume-screener
📄 Smart Resume Screener
An intelligent resume screening tool that compares a candidate's resume with a job description using Natural Language Processing (NLP) and Machine Learning embeddings.


🚀 Features
✅ Upload Resume PDF and Job Description PDF
✅ Extracts and cleans text using NLP (spaCy, regex)
✅ Uses sentence embeddings (sentence-transformers) to compare context
✅ Calculates:

Overall Match Percentage

Matched Skills

Missing Skills
✅ Built with Streamlit for an interactive, web-based interface

🧠 Tech Stack
Tool	Purpose
Streamlit	             : Web app frontend
pdfplumber	           : Extracts text from PDF resumes
spaCy	                 : NLP preprocessing (tokenizing, cleaning)
sentence-transformers	 : Contextual embeddings for similarity
scikit-learn	         : Cosine similarity
pandas	               : Skill matching logic

📦 Installation (Local)
Clone the repo:
git clone https://github.com/vivekk0/smart-resume-screener
cd smart-resume-screener

Create a virtual environment:
python -m venv venv
venv\Scripts\activate     # On Windows
source venv/bin/activate  # On Mac/Linux


Install dependencies:
pip install -r requirements.txt

Run the app:
streamlit run app.py

🖼️ App UI Preview
Resume & JD Upload	Match Score & Skill Comparison

🛠️ How It Works
Upload: A resume and job description PDF

Text is extracted and cleaned using pdfplumber and spaCy

Embeddings are generated using sentence-transformers

Cosine similarity is calculated between the texts

Skills are extracted from a predefined skill list

Final output:

Similarity Score (Match %)

Matched Skills

Missing Skills

🔮 Future Enhancements
 Batch resume uploads with ranking

 Dynamic skill extraction via custom NER

 Experience-weighted scoring

 Smart filtering by job title or domain

 Downloadable skill reports

💡 Use Cases
Job seekers checking how well their resume matches job roles

Recruiters doing initial resume filtering

Resume optimization for better ATS matching

🙋‍♂️ Author
Vivek Kumar
GitHub:https://github.com/vivekk0 • LinkedIn:https://www.linkedin.com/in/vivek-kumar-730974253/


