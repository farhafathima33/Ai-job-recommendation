>AI-Powered Job Recommendation System

An explainable AI-powered job recommendation system that analyses a candidate's profile against available job descriptions and recommends the most relevant job opportunities.

The system combines rule-based matching for structured candidate information with TF-IDF and cosine similarity for text relevance. It provides match scores, matched skills, missing skills, score breakdowns, and human-readable explanations.

## Features

- Candidate profile input through a Streamlit interface
- Job recommendation based on multiple matching factors
- Skill matching and missing-skill identification
- Mandatory skill tracking
- Experience matching
- Education matching
- Location and remote-work compatibility
- TF-IDF and cosine similarity for profile/job text relevance
- Preferred-role and job-title relevance
- Weighted overall match score
- Explainable recommendation results
- Top-N job ranking
- Input validation and error handling
- FastAPI backend API
- Streamlit frontend
- Automated unit tests using pytest
- Recommendation evaluation using Precision and Recall


## Setup and Run Instructions

1. Clone the Repository
[git clone https://github.com/farhafathima33/Ai-job-recommendation.git
cd Ai-job-recommendation]

2. Create a Virtual Environment
[python3 -m venv venv]

Activate the virtual environment on Ubuntu/Linux
[source venv/bin/activate]

3. Install Dependencies
[pip install -r requirements.txt]

4. Run the Tests
[pytest]

5. Start the FastAPI Backend
[uvicorn main:app --reload]

The API will be available at:
http://127.0.0.1:8000

Interactive Swagger documentation:
http://127.0.0.1:8000/docs
Keep this terminal running.

6. Start the Streamlit Frontend

Open a second terminal and activate the virtual environment:
[cd Ai-job-recommendation]
[source venv/bin/activate]

Then run:
streamlit run streamlit_app.py
Open the local URL provided by Streamlit, usually:
[http://localhost:8501]


7. Use the Application

Enter the candidate's:
Name
Skills
Years of experience
Education
Preferred job role
Location
Profile summary
Click Recommend Jobs to receive ranked job recommendations with match scores, matched/missing skills, score breakdown, and explanations. 

## System Architecture

The system follows a simple frontend-backend-recommendation architecture:

Candidate
   |
Streamlit Frontend
   |
FastAPI Backend
   |
Pydantic Validation
   |
Recommendation Engine
   |
├── Skill Matching
├── Experience Matching
├── Education Matching
├── Location Matching
└── TF-IDF Text Similarity
   |
Weighted Match Score
   |
Top-N Recommendations
   |
Explanation + Score Breakdown

## Recommendation Methodology (Description of AI/Matching approach)

The system uses a hybrid and explainable matching approach.

Structured candidate information such as skills, experience, education, and location is evaluated using rule-based matching. Textual relevance between the candidate profile and job information is calculated using TF-IDF and cosine similarity.

The final match score is calculated using weighted scoring:

| Matching Factor | Weight |

| Skills          | 45%    |
| Experience      | 20%    |
| Role/Text Relevance| 15% |
| Education       | 10%    |
| Location        | 10%    |
| **Total**       |**100%**|

The final score is calculated as:

Final Score =
(Skill Score × 0.45) +
(Experience Score × 0.20) +
(Role Score × 0.15) +
(Education Score × 0.10) +
(Location Score × 0.10)

> Weighting Rational

-Skills receive the highest weight because technical and functional skills are central to determining whether a candidate can satisfy the requirements of a job.

-Experience is given the second-highest weight because the required level of professional experience is an important eligibility factor.

-Role/text relevance captures similarity between the candidate's preferred role and profile summary and the job title and description.

-Education and location are included as additional compatibility factors.

> Text Similarity

The system uses TF-IDF and cosine similarity to estimate textual relevance between a candidate and a job.

> TF-IDF

TF-IDF (Term Frequency-Inverse Document Frequency) converts text into numerical vectors based on the importance of words within the available documents.

Common words receive less importance, while words that are more distinctive within the text receive higher importance.

> Cosine Similarity

After converting the candidate and job text into TF-IDF vectors, cosine similarity measures how similar the two vectors are.

The resulting similarity value is converted into a percentage and used as the Role/Text Relevance score.

For this prototype, the candidate text combines:

- Preferred role
- Profile summary

The job text combines:

- Job title
- Job description

> Why TF-IDF?

TF-IDF was selected because it provides a simple, explainable, and computationally inexpensive approach for textual matching.

Advantages for this prototype include:

- Easy to implement and understand
- Fast for small and medium-sized datasets
- No external model API is required
- No GPU is required 
- Easy to test and debug

## Mandatory Skills

The system distinguishes between general required skills and mandatory skills.

General required skills contribute to the overall skill score. Mandatory skills are treated separately because they may represent essential requirements for a particular role.

For each job, the system can define a list of mandatory skills:

json
{
    "mandatory_skills": [
        "Python",
        "Machine Learning"
    ]
}
 
## Explainability

The system provides an explanation for each recommendation instead of returning only a numerical match score.

The explanation is generated from the actual matching results and includes:

- Matched skills
- Missing skills
- Experience comparison
- Education 
- Location 
- Role/text relevance

For example:

> Matched skills include machine learning, Python, and SQL. Missing skills include TensorFlow. The candidate has 2 years of experience and meets the 1-year requirement. The candidate's education satisfies the job requirement. Location compatibility is partial because the job is hybrid.

The explanation is generated using deterministic rules.
This makes the output:
- Easy to understand
- Easy to test

## Key Assumptions and Design Decisions 

The following assumptions and design decisions were made while developing the prototype.

 1. Skills are explicitly provided
Assume the candidate's skills and the job's required skills are already available as lists.
Example:
Candidate: Python, SQL, Pandas
Job requires: Python, SQL, TensorFlow
[We compare these lists after converting them to lowercase and removing extra spaces.]

 2. Experience is measured in years

Assume experience is given numerically.
Example:
Candidate = 2 years
Job requires = 1 year
→ Experience score = 100%
[If the candidate has less experience, the score is reduced proportionally.]

 3. Education matching is rule-based

Compared education using predefined rules.
For example:
Candidate: BS Data Science
Job: Bachelor's degree
→ Match

 4. Location depends on work mode

Consider both location and whether the job is remote/hybrid/on-site.
For example:
Remote job → Location doesn't matter much
Same location → Good compatibility
Different location + on-site → Low compatibility

 5. TF-IDF is used for text relevance

Used TF-IDF + cosine similarity to compare the candidate's profile/role with the job title/description.
 
 6. Weighted scoring is used

Will combine all matching factors into one final score:
Skills       → 45%
Experience   → 20%
Role         → 15%
Education    → 10%
Location     → 10%
[Skills are considered the most important factor for this prototype, while the other factors contribute to the overall compatibility.
Importantly, these are our prototype design choices, not universally correct weights.]

 7. Mandatory skills are tracked separately

Some skills may be essential for a particular job.
For example:
Required: Python, SQL, TensorFlow
Mandatory: Python
[The system separately checks whether mandatory skills are missing.]

 8. Mock job data is used

I used jobs.json instead of a real job database.

## Limitations and Possible Improvements

    Limitation                             |       Possible Improvment
                                           |
TF-IDF has limited semantic understanding  | Use embeddings/Sentence Transformers for semantic similarity.
                                           |
User has to enter skills, experience,      | Allow PDF/resume upload and automatically extract candidate 
education, etc. manually.                  | information.
                                           |
Jobs are currently stored in jobs.json,    | Use PostgreSQL/MySQL for larger applications.
which is fine for a small prototype.       |
                                           |
We currently use sample jobs from          | Connect to an authorised job database/API and update job
jobs.json.                                 | listings automatically.
                                           |
                                           
                                           

## Evaluation

The recommendation system was evaluated using manually labelled candidate-job examples.

For each evaluation case, the expected relevant jobs were defined in `data/evaluation.json`. The system generated the top 3 recommendations, which were then compared with the labelled relevant jobs.

- Evaluation Metrics

> Precision

Precision@3 measures how many of the top 3 recommended jobs are relevant.
Precision@3 = Relevant jobs in top 3 recommendations / 3

> Recall

Recall@3 measures how many of the relevant jobs were successfully retrieved within the top 3 recommendations.
Recall@3 = Relevant jobs in top 3 recommendations / Total relevant jobs

 API Documentation

The project provides a FastAPI backend for generating job recommendations.

- Start the API
Run the following command from the project root:
[uvicorn main:app --reload]

- Endpoint
POST /recommend
The endpoint accepts a candidate profile and a list of jobs and returns the ranked job recommendations.

 Testing

The project uses `pytest` for automated testing.
Test cases are stored in:
[tests/test_recommendation.py]

### Example request
{
  "candidate": {
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
    "summary": "Data science graduate with experience in machine learning using Python and SQL."
  },
  "jobs": [
    {
      "title": "Junior Machine Learning Engineer",
      "company": "TechNova",
      "description": "Looking for a machine learning engineer with Python and SQL experience.",
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
    }
  ]
}

### Example Response
{
  "recommendations": [
    {
      "job_title": "Junior Machine Learning Engineer",
      "company": "TechNova",
      "match_score": 78.79,
      "matched_skills": [
        "machine learning",
        "pandas",
        "python",
        "sql"
      ],
      "missing_skills": [
        "tensorflow"
      ],
      "missing_mandatory_skills": [],
      "mandatory_skill_gap": false,
      "experience_score": 100.0,
      "education_score": 100.0,
      "location_score": 50.0,
      "role_score": 66.94
    }
  ]
}

 Response Fields

     Field	             |         Description

job_title	               |   Recommended job title
company	                 |   Company offering the job
match_score              |	 Overall weighted match score
matched_skills           |	 Skills shared by the candidate and job
missing_skills           |   Required skills missing from the candidate profile
missing_mandatory_skills |	 Mandatory skills missing from the candidate profile
mandatory_skill_gap	     |   Indicates whether a mandatory skill is missing
experience_score	       |   Experience compatibility score
education_score	         |   Education compatibility score
location_score	         |   Location/work-mode compatibility score
role_score	             |   TF-IDF-based role/text relevance score

 
 API Validation

The API uses Pydantic models to validate incoming candidate and job data.

For example, the candidate must contain:
-Candidate name
-Skills
-Profile summary
Other fields such as experience, education, location and preferred role can be optional at the API model level.