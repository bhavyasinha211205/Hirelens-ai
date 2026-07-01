from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


def semantic_match(jd_skills, resume_data):

    resume_texts = []

    # Resume skills
    resume_texts.extend(resume_data.get("skills", []))

    # Project technologies
    for project in resume_data.get("projects", []):
        resume_texts.extend(project.get("tech_stack", []))

    # Experience
    for exp in resume_data.get("experience", []):
        sentence = f"{exp.get('role', '')} {exp.get('company', '')}"
        resume_texts.append(sentence)

    # Remove duplicates
    resume_texts = list(set(resume_texts))

    if len(resume_texts) == 0:
        return {
            "matches": []
        }

    resume_embeddings = model.encode(
        resume_texts,
        normalize_embeddings=True
    )

    matches = []

    for jd_skill in jd_skills:

        jd_embedding = model.encode(
            [jd_skill],
            normalize_embeddings=True
        )

        similarities = cosine_similarity(
            jd_embedding,
            resume_embeddings
        )[0]

        top_indices = np.argsort(similarities)[-3:][::-1]

        top_matches = []

        for idx in top_indices:

            top_matches.append({
                "text": resume_texts[idx],
                "similarity": round(float(similarities[idx]), 3)
            })

        matches.append({
            "jdSkill": jd_skill,
            "bestMatch": top_matches[0]["text"],
            "similarity": top_matches[0]["similarity"],
            "topMatches": top_matches
        })

    return {
        "matches": matches
    }