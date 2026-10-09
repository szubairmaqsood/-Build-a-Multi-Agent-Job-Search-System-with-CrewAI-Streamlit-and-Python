from crewai import Crew, Process
from agents.jd_analyst import get_jd_analyst_agent, create_jd_analysis_task
from agents.resume_cl_agent import get_resume_cl_agent, create_resume_cl_task
from usajobs_api import fetch_usajobs

def load_resume(path="data/sample_resume.txt"):
    with open(path, "r") as file:
        return file.read()

def run_pipeline():
    # Step 1: Fetch job post
    job_posts = fetch_usajobs("business analyst", location="New York")
    if not job_posts:
        print("No job posts found.")
        return

    job_data = job_posts[0]['MatchedObjectDescriptor']
    job_summary = job_data['UserArea']['Details']['JobSummary']

    # Step 2: Load resume
    resume_text = load_resume()

    # Step 3: Initialize agents
    jd_agent = get_jd_analyst_agent()
    resume_agent = get_resume_cl_agent()

    # Step 4: Create tasks
    jd_task = create_jd_analysis_task(jd_agent, job_summary)
    resume_task = create_resume_cl_task(resume_agent, job_summary, resume_text)

    # Step 5: Create and run the crew
    crew = Crew(
        agents=[jd_agent, resume_agent],
        tasks=[jd_task, resume_task],
        process=Process.sequential
    )
    result = crew.kickoff()

    print("\n=== FINAL OUTPUT ===\n")
    print(result)

if __name__ == "__main__":
    run_pipeline()