import streamlit as st
import requests
from app.data_loader import load_jobs


jobs = load_jobs()

st.title("AI Job Recommendation System")

st.write(
    "Enter your profile details to find suitable job recommendations."
)


name = st.text_input("Candidate Name")

skills = st.text_input(
    "Skills",
    placeholder="Python, SQL, Machine Learning, Pandas"
)

experience = st.number_input(
    "Years of Experience",
    min_value=0.0,
    step=0.5
)

education = st.text_input(
    "Education",
    placeholder="BS Data Science"
)

preferred_role = st.text_input(
    "Preferred Job Role",
    placeholder="Machine Learning Engineer"
)

location = st.text_input(
    "Location",
    placeholder="Kozhikode"
)

summary = st.text_area(
    "Profile Summary",
    placeholder="Describe your skills, experience and career interests..."
)


if st.button("Recommend Jobs"):

    if not name.strip():
        st.warning("Please enter your name.")

    elif not skills.strip():
        st.warning("Please enter at least one skill.")

    elif not summary.strip():
        st.warning("Please enter your profile summary.")

    else:

        candidate = {
            "name": name.strip(),
            "skills": [
                skill.strip()
                for skill in skills.split(",")
                if skill.strip()
            ],
            "experience": experience,
            "education": education or None,
            "location": location or None,
            "preferred_role": preferred_role or None,
            "summary": summary.strip()
        }

        st.write("Processing your profile...")

        response = requests.post(
            "http://127.0.0.1:8000/recommend",
            json={
                "candidate": candidate,
                "jobs": jobs
            }
        )

        if response.status_code == 200:

            data = response.json()

            st.success(
                "Recommendations generated successfully!"
            )

            recommendations = data["recommendations"]

            st.subheader("Recommended Jobs")

            for index, job in enumerate(
                recommendations,
                start=1
            ):

                st.markdown("---")

                st.subheader(
                    f"{index}. {job['job_title']}"
                )

                st.write(
                    f"**Company:** {job['company']}"
                )

                st.metric(
                    "Match Score",
                    f"{job['match_score']}%"
                )

                st.write("**Matched Skills**")

                if job["matched_skills"]:
                    for skill in job["matched_skills"]:
                        st.success(f"✓ {skill}")
                else:
                    st.write("No matching skills")


                st.write("**Missing Skills**")

                if job["missing_skills"]:
                    for skill in job["missing_skills"]:
                        st.warning(f"⚠ {skill}")
                else:
                    st.write("No missing skills")

                st.write("**Score Breakdown**")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "Experience",
                        f"{job['experience_score']}%"
                    )

                with col2:
                    st.metric(
                        "Education",
                        f"{job['education_score']}%"
                    )

                with col3:
                    st.metric(
                        "Location",
                        f"{job['location_score']}%"
                    )

                with col4:
                    st.metric(
                        "Role Relevance",
                        f"{job['role_score']}%"
                    )
             

                st.write("**Explanation**")

                st.info(job["explanation"])

        else:

            st.error(
                f"API request failed: "
                f"{response.status_code}"
            )