import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")


def extract_keywords(text):
    doc = nlp(text)
    return [token.lemma_.lower() for token in doc if
            token.pos_ in ['NOUN', 'PROPN', 'VERB', 'ADJ'] and not token.is_stop]


def match_resume_to_job(resume_text, job_description):
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_description)

    all_texts = [' '.join(resume_keywords), ' '.join(job_keywords)]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    return round(score * 100, 2)


def parse_resume_text(text):
    doc = nlp(text)

    skills = []
    experience_sentences = []
    education_sentences = []

    for ent in doc.ents:
        if ent.label_ in ['ORG', 'PRODUCT', 'SKILL']:
            skills.append(ent.text)

    for sent in doc.sents:
        if 'experience' in sent.text.lower():
            experience_sentences.append(sent.text)
        if any(x in sent.text.lower() for x in ['university', 'bachelor', 'msc', 'phd']):
            education_sentences.append(sent.text)

    return {
        'skills': list(set(skills)),
        'experience': "\n".join(experience_sentences),
        'education': "\n".join(education_sentences),
    }
