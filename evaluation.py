import json
from pathlib import Path

from app.data_loader import load_jobs
from app.text_processing import recommend_jobs


def load_evaluation_data():
    """
    Load manually labelled evaluation data.
    """

    file_path = (
        Path(__file__).parent
        / "data"
        / "evaluation.json"
    )

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def precision_at_k(recommended_jobs, relevant_jobs, k):
    """
    Calculate Precision@K.
    """

    top_k_jobs = recommended_jobs[:k]

    recommended_titles = {
        job["job_title"]
        for job in top_k_jobs
    }

    relevant_titles = set(relevant_jobs)

    relevant_recommendations = (
        recommended_titles.intersection(
            relevant_titles
        )
    )

    if k == 0:
        return 0.0

    return round(
        len(relevant_recommendations) / k,
        2
    )


def recall_at_k(recommended_jobs, relevant_jobs, k):
    """
    Calculate Recall@K.
    """

    top_k_jobs = recommended_jobs[:k]

    recommended_titles = {
        job["job_title"]
        for job in top_k_jobs
    }

    relevant_titles = set(relevant_jobs)

    relevant_recommendations = (
        recommended_titles.intersection(
            relevant_titles
        )
    )

    if not relevant_titles:
        return 0.0

    return round(
        len(relevant_recommendations)
        / len(relevant_titles),
        2
    )


def evaluate():
    """
    Evaluate the recommendation system.
    """

    evaluation_data = load_evaluation_data()
    jobs = load_jobs()

    for case in evaluation_data:

        candidate = case["candidate"]
        print(
            f"\n{'=' * 50}"
        )

        print(
            f"Candidate: {candidate['name']}"
        )

        print(
            f"{'=' * 50}"
        )

        relevant_jobs = case["relevant_jobs"]

        recommendations = recommend_jobs(
            candidate,
            jobs,
            top_n=3
        )

        precision = precision_at_k(
            recommendations,
            relevant_jobs,
            k=3
        )

        recall = recall_at_k(
            recommendations,
            relevant_jobs,
            k=3
        )

        print("\nRecommended jobs:")

        for job in recommendations:
            print(
                f"- {job['job_title']}: "
                f"{job['match_score']}%"
            )

        print(
            f"\nPrecision@3: {precision}"
        )

        print(
            f"Recall@3: {recall}"
        )


if __name__ == "__main__":
    evaluate()