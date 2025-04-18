import spacy
import pdfplumber
import docx

nlp = spacy.load("en_core_web_sm")


def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        return '\n'.join(page.extract_text() or '' for page in pdf.pages)


def extract_text_from_docx(file):
    doc = docx.Document(file)
    return '\n'.join(p.text for p in doc.paragraphs)


def parse_resume_text(text):
    doc = nlp(text)
    skills = [ent.text for ent in doc.ents if ent.label_ in ['SKILL', 'ORG', 'PERSON']]
    experience = '\n'.join([sent.text for sent in doc.sents if 'experience' in sent.text.lower()])
    education = '\n'.join([
        sent.text for sent in doc.sents
        if 'university' in sent.text.lower() or 'bachelor' in sent.text.lower()
    ])
    return {
        'skills': list(set(skills)),
        'experience': experience,
        'education': education
    }
