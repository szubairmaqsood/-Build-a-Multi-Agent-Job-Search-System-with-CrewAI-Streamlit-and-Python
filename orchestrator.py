# Imports necessary modules
from crewai import Crew, Process

from agents.jd_analyst import (
    get_jd_analyst_agent,
    create_jd_analysis_task,
)
from agents.resume_cl_agent import (
    get_resume_cl_agent,
    create_resume_cl_task,
)
from agents.messaging_agent import (
    get_messaging_agent,
    create_messaging_task,
)

from usajobs_api import fetch_usajobs

# Loading sample resume from a text file
def load_resume(path="data/sample_resume.txt"):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

# Running pipeline
def run_pipeline():
    # Step 1: Fetch a job posting
    job_posts = fetch_usajobs(
        "business analyst",
        location="New York",
    )

    if not job_posts:
        print("No job posts found.")
        return

    # Step 2: Extract job details
    job_data = job_posts[0]["MatchedObjectDescriptor"]

    job_summary = (
        job_data.get("UserArea", {})
        .get("Details", {})
        .get("JobSummary", "Job summary not available.")
    )

    agency_name = job_data.get("OrganizationName", "Unknown agency")
    job_title = job_data.get("PositionTitle", "Unknown job title")

    print(f"\nJob Title: {job_title}")
    print(f"Agency: {agency_name}")

    # Step 3: Load the candidate's resume
    resume_text = load_resume()

    # Step 4: Define a sample candidate bio
    user_bio = (
        "I'm a data professional passionate about public service. "
        "I enjoy analyzing data, solving business problems, "
        "and developing data-driven solutions."
    )

    # Step 5: Initialize all three agents
    jd_agent = get_jd_analyst_agent()
    resume_agent = get_resume_cl_agent()
    messaging_agent = get_messaging_agent()

    # Step 6: Create tasks
    jd_task = create_jd_analysis_task(
        jd_agent,
        job_summary,
    )

    resume_task = create_resume_cl_task(
        resume_agent,
        job_summary,
        resume_text,
    )

    messaging_task = create_messaging_task(
        messaging_agent,
        job_summary,
        agency_name,
        user_bio,
    )

    # Step 7: Run all three agents sequentially
    crew = Crew(
        agents=[
            jd_agent,
            resume_agent,
            messaging_agent,
        ],
        tasks=[
            jd_task,
            resume_task,
            messaging_task,
        ],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    # Step 8: Print the final result
    print("\n=== FINAL OUTPUT ===\n")
    print(result)


if __name__ == "__main__":
    run_pipeline()