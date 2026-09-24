from app.text_processing import match_candidate_to_job

###test high match candidate
def test_high_match():

    candidate = {
        "name": "Test Candidate",
        "skills": [
            "Python",
            "Machine Learning",
            "SQL",
            "Pandas"
        ],
        "experience": 3,
        "education": "BS Data Science",
        "location": "Kozhikode",
        "summary": (
            "Machine learning developer with experience "
            "in Python, SQL and machine learning."
        )
    }

    job = {
        "title": "Machine Learning Engineer",
        "company": "Test Company",
        "description": (
            "Looking for a machine learning engineer "
            "with Python, SQL and machine learning skills."
        ),
        "required_skills": [
            "Python",
            "Machine Learning",
            "SQL"
        ],
        "min_experience": 2,
        "education": "Bachelor's degree",
        "location": "Kozhikode",
        "remote_type": "On-site"
    }

    result = match_candidate_to_job(candidate, job)

    assert result["match_score"] >= 80

###test low match candidate
def test_low_match():

    candidate = {
        "name": "Test Candidate",
        "skills": [
            "Python",
            "Machine Learning",
            "SQL"
        ],
        "experience": 1,
        "education": "BS Data Science",
        "location": "Kozhikode",
        "summary": (
            "Data science graduate with experience "
            "in Python, machine learning and SQL."
        )
    }

    job = {
        "title": "Graphic Designer",
        "company": "Creative Studio",
        "description": (
            "Looking for a graphic designer with "
            "Photoshop, Illustrator and Figma skills."
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
    }

    result = match_candidate_to_job(candidate, job)

    assert result["match_score"] < 50

###test edge case candidates
def test_edge_case_missing_information():

    candidate = {
        "name": "Incomplete Candidate",
        "skills": ["Python"],
        "experience": None,
        "education": None,
        "location": None,
        "summary": None
    }

    job = {
        "title": "Python Developer",
        "company": "Test Company",
        "description": (
            "Looking for a Python developer "
            "with Python and SQL skills."
        ),
        "required_skills": [
            "Python",
            "SQL"
        ],
        "min_experience": 2,
        "education": "Bachelor's degree",
        "location": "Kozhikode",
        "remote_type": "On-site"
    }

    result = match_candidate_to_job(candidate, job)

    assert result is not None
    assert "match_score" in result

def test_missing_mandatory_skill():

    candidate = {
        "name": "Test Candidate",
        "skills": [
            "SQL",
            "Pandas",
            "Python"
        ],
        "experience": 5,
        "education": "BS Data Science",
        "location": "Kozhikode",
        "summary": (
            "Experienced data professional with strong "
            "Python, SQL and machine learning knowledge."
        )
    }

    job = {
        "title": "Machine Learning Engineer",
        "company": "Test Company",
        "description": (
            "Looking for a machine learning engineer "
            "with Python, SQL and TensorFlow skills."
        ),
        "required_skills": [
            "Python",
            "SQL",
            "TensorFlow"
        ],
        "mandatory_skills": [
            "Python",
            "TensorFlow"
        ],
        "min_experience": 2,
        "education": "Bachelor's degree",
        "location": "Kozhikode",
        "remote_type": "On-site"
    }

    result = match_candidate_to_job(candidate, job)

    assert result["mandatory_skill_gap"] is True
    assert "tensorflow" in result["missing_mandatory_skills"]
    assert result["match_score"] <= 59.99