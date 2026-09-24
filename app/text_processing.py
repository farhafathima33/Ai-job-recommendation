from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def normalize_skill(skill):
    """
    Normalize a skill name for consistent comparison.
    """
    return skill.strip().lower()


def match_skills(
    candidate_skills,
    required_skills,
    mandatory_skills=None   #mandotary skills defined bcos if a candidate is perfectly match with education, experience, locatian all but doesnt have important skill for that job never get high matching score
):
    """
    Compare candidate skills with job-required skills
    and identify missing mandatory skills.
    """

    if mandatory_skills is None:
        mandatory_skills = []

    candidate_normalized = {
        normalize_skill(skill)
        for skill in candidate_skills
    }

    required_normalized = {
        normalize_skill(skill)
        for skill in required_skills
    }

    mandatory_normalized = {
        normalize_skill(skill)
        for skill in mandatory_skills
    }

    matched_skills = (
        candidate_normalized.intersection(required_normalized)
    )

    missing_skills = (
        required_normalized - candidate_normalized
    )

    missing_mandatory_skills = (
        mandatory_normalized - candidate_normalized
    )

    if not required_normalized:
        skill_score = 0
    else:
        skill_score = (
            len(matched_skills) / len(required_normalized)
        ) * 100

    return {
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
        "missing_mandatory_skills": sorted(
            missing_mandatory_skills
        ),
        "mandatory_skill_gap": bool(
            missing_mandatory_skills
        ),
        "score": round(skill_score, 2)
    }

###Experience Scoring
###Formula Experience Score = min(candidate_experience / required_experience, 1) × 100

def calculate_experience_score(candidate_experience, required_experience):
    """
    Calculate how well the candidate's experience meets the job requirement.
    """

    # If the job does not specify an experience requirement
    if required_experience is None or required_experience <= 0:
        return 100.0

    # If candidate experience is missing
    if candidate_experience is None:
        return 0.0

    score = min(
        candidate_experience / required_experience,
        1
    ) * 100

    return round(score, 2)


###Education function
def calculate_education_score(candidate_education, required_education):
    """
    Calculate how well the candidate's education  satisfies the job requirement.
    """

    if required_education is None:
        return 100.0

    if candidate_education is None:
        return 0.0

    candidate = candidate_education.lower().strip()
    required = required_education.lower().strip()

    if candidate == required:
        return 100.0

    if "bachelor" in required and (
        "bachelor" in candidate
        or "bs" in candidate
        or "b.sc" in candidate
        or "bsc" in candidate
    ):
        return 100.0

    if "master" in required and (
        "master" in candidate
        or "ms" in candidate
        or "m.sc" in candidate
        or "msc" in candidate
    ):
        return 100.0

    return 0.0

###Location Matching

def calculate_location_score(
    candidate_location,
    job_location,
    remote_type
):
    """
    Calculate how well the job location/work arrangement
    fits the candidate's location.
    """

    # Remote jobs are accessible regardless of location
    if remote_type is not None:
        if remote_type.lower().strip() == "remote":
            return 100.0

    # Missing location information
    if candidate_location is None or job_location is None:
        return 50.0

    candidate = candidate_location.lower().strip()
    job = job_location.lower().strip()

    # Same location
    if candidate == job:
        return 100.0

    # Different location + hybrid
    if remote_type is not None:
        if remote_type.lower().strip() == "hybrid":
            return 50.0

    # Different location + on-site
    return 0.0


### TF-IDF cosine similarity
def calculate_role_similarity(
    candidate_role,
    candidate_summary,
    job_title,
    job_description
):
    """
    Calculate text similarity between the candidate's
    preferred role/profile and the job's title/description
    using TF-IDF and cosine similarity.
    """

    candidate_text = " ".join(
        value
        for value in [
            candidate_role,
            candidate_summary
        ]
        if value
    )

    job_text = " ".join(
        value
        for value in [
            job_title,
            job_description
        ]
        if value
    )

    if not candidate_text or not job_text:
        return 0.0

    documents = [
        candidate_text,
        job_text
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    return round(similarity * 100, 2)

###Calculate Final Match
def calculate_final_score(
    skill_score,
    experience_score,
    role_score,
    education_score,
    location_score,
    mandatory_skill_gap=False
):
    """
    Calculate the overall job match score
    using weighted scoring.

    If a mandatory skill is missing,
    cap the score at 59.99%.
    """

    final_score = (
        skill_score * 0.45
        + experience_score * 0.20
        + role_score * 0.15
        + education_score * 0.10
        + location_score * 0.10
    )

    if mandatory_skill_gap:
        final_score = min(final_score, 59.99)

    return round(final_score, 2)

###Explanation generator
def generate_explanation(candidate, job, result):
    """
    Generate a human-readable explanation
    for the job recommendation.
    """

    matched_skills = result["matched_skills"]
    missing_skills = result["missing_skills"]

    missing_mandatory_skills = result.get(
    "missing_mandatory_skills", []
    )
 
    # Skill explanation
    if matched_skills:
        skill_text = (
            f"Matched skills include "
            f"{', '.join(matched_skills)}."
        )
    else:
        skill_text = "There are no matching required skills."

    if missing_skills:
        missing_text = (
            f"Missing skills include "
            f"{', '.join(missing_skills)}."
        )
    else:
        missing_text = "The candidate has all required skills."

    if missing_mandatory_skills:
        mandatory_text = (
            f"Important: the candidate is missing "
            f"mandatory skill(s): "
            f"{', '.join(missing_mandatory_skills)}."
        )
    else:
        mandatory_text = (
            "The candidate has all specified mandatory skills."
        )

    # Experience explanation
    candidate_experience = candidate.get("experience")
    required_experience = job.get("min_experience")

    if required_experience is None:
        experience_text = (
            "The job does not specify a minimum "
            "experience requirement."
        )
    elif candidate_experience is None:
        experience_text = (
            "The candidate's experience information "
            "was not provided."
        )
    elif candidate_experience >= required_experience:
        experience_text = (
            f"The candidate has {candidate_experience} "
            f"years of experience and meets the "
            f"{required_experience}-year requirement."
        )
    else:
        experience_text = (
            f"The candidate has {candidate_experience} "
            f"years of experience, while the job requires "
            f"{required_experience} years."
        )

    # Education explanation
    education_score = result["education_score"]

    if education_score == 100:
        education_text = (
            "The candidate's education satisfies "
            "the job requirement."
        )
    elif candidate.get("education") is None:
        education_text = (
            "The candidate's education information "
            "was not provided."
        )
    else:
        education_text = (
            "The candidate's education does not "
            "fully satisfy the stated requirement."
        )

    # Location explanation
    location_score = result["location_score"]

    if job.get("remote_type", "").lower() == "remote":
        location_text = (
            "The job is remote, so location does not "
            "restrict the candidate."
        )
    elif location_score == 100:
        location_text = (
            "The candidate and job are in the same location."
        )
    elif location_score == 50:
        location_text = (
            "Location compatibility is partial because "
            "the job is hybrid or location information "
            "is incomplete."
        )
    else:
        location_text = (
            "The candidate and job are in different "
            "locations and the job is not remote."
        )

    explanation = (
        f"{skill_text} {missing_text} "
        f"{mandatory_text} "
        f"{experience_text} "
        f"{education_text} "
        f"{location_text}"
    )

    return explanation

##Complete job matching function
def match_candidate_to_job(candidate, job):
    """
    Calculate the complete match between a candidate
    and a single job.
    """

    # 1. Skill matching
    skill_result = match_skills(
        candidate.get("skills", []),
        job.get("required_skills", []),
        job.get("mandatory_skills", [])
    )
    # 2. Experience matching
    experience_score = calculate_experience_score(
        candidate.get("experience"),
        job.get("min_experience")
    )

    # 3. Education matching
    education_score = calculate_education_score(
        candidate.get("education"),
        job.get("education")
    )

    # 4. Location matching
    location_score = calculate_location_score(
        candidate.get("location"),
        job.get("location"),
        job.get("remote_type")
    )

    # 5. Role / text similarity
    role_score = calculate_role_similarity(
        candidate.get("preferred_role"),
        candidate.get("summary"),
        job.get("title"),
        job.get("description")
    )

    # 6. Final weighted score
    final_score = calculate_final_score(
        skill_score=skill_result["score"],
        experience_score=experience_score,
        role_score=role_score,
        education_score=education_score,
        location_score=location_score,
        mandatory_skill_gap=skill_result["mandatory_skill_gap"]
    )

    # Create the result
    result = {
        "job_title": job.get("title"),
        "company": job.get("company"),
        "match_score": final_score,
        "matched_skills": skill_result["matched_skills"],
        "missing_skills": skill_result["missing_skills"],
        "missing_mandatory_skills": skill_result[
            "missing_mandatory_skills"
    ],
        "mandatory_skill_gap": skill_result[
            "mandatory_skill_gap"
    ],
        "experience_score": experience_score,
        "education_score": education_score,
        "location_score": location_score,
        "role_score": role_score
    }

    # Generate explanation
    result["explanation"] = generate_explanation(
        candidate,
        job,
        result
    )

    return result

###Recommendation Function
def recommend_jobs(candidate, jobs, top_n=3):
    """
    Match a candidate against multiple jobs,
    rank the jobs by match score, and return
    the top recommendations.
    """

    recommendations = []

    for job in jobs:
        result = match_candidate_to_job(candidate, job)
        recommendations.append(result)

    recommendations.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return recommendations[:top_n]

if __name__ == "__main__":

    print("\nJob Recommendation Test")

    candidate = {
        "name": "Alex",
        "skills": [
            "Python",
            "Machine Learning",
            "SQL",
            "Pandas"
        ],
        "experience": 2,
        "education": "BS Data Science",
        "location": "Kozhikode",
        "preferred_role": "Machine Learning Engineer",
        "summary": (
            "Data science graduate with experience in "
            "machine learning using Python and SQL."
        )
    }

    jobs = [
        {
            "title": "Junior Machine Learning Engineer",
            "company": "TechNova",
            "description": (
                "Looking for a machine learning engineer "
                "with Python and SQL experience."
            ),
            "required_skills": [
                "Python",
                "Machine Learning",
                "SQL",
                "TensorFlow"
            ],
            "mandatory_skills": [
                "Python",
                "Machine Learning"
            ],
            
            "min_experience": 1,
            "education": "Bachelor's degree",
            "location": "Bangalore",
            "remote_type": "Hybrid"
        },

        {
            "title": "Data Analyst",
            "company": "DataCorp",
            "description": (
                "Looking for a data analyst with SQL, "
                "Python and data analysis skills."
            ),
            "required_skills": [
                "SQL",
                "Python",
                "Excel",
                "Power BI"
            ],
            "min_experience": 1,
            "education": "Bachelor's degree",
            "location": "Kozhikode",
            "remote_type": "On-site"
        },

        {
            "title": "Graphic Designer",
            "company": "CreativeStudio",
            "description": (
                "Looking for a graphic designer with "
                "Photoshop and Illustrator experience."
            ),
            "required_skills": [
                "Photoshop",
                "Illustrator",
                "Figma"
            ],
            "min_experience": 2,
            "education": "Bachelor's degree",
            "location": "Mumbai",
            "remote_type": "On-site"
        },

        {
            "title": "Python Developer",
            "company": "CodeWorks",
            "description": (
                "Python developer needed for backend "
                "development and API development."
            ),
            "required_skills": [
                "Python",
                "SQL",
                "FastAPI"
            ],
            "min_experience": 1,
            "education": "Bachelor's degree",
            "location": "Bangalore",
            "remote_type": "Remote"
        }
    ]

    recommendations = recommend_jobs(
        candidate,
        jobs,
        top_n=3
    )

    for index, recommendation in enumerate(
        recommendations,
        start=1
    ):
        print(
    f"\n{index}. "
    f"{recommendation['job_title']} - "
    f"{recommendation['company']} - "
    f"{recommendation['match_score']}%"
        )

        print(
            "Matched skills:",
            ", ".join(recommendation["matched_skills"])
        )

        print(
        "Missing skills:",
        ", ".join(recommendation["missing_skills"])
        )

        print(
        "Explanation:",
        recommendation["explanation"]
        )
