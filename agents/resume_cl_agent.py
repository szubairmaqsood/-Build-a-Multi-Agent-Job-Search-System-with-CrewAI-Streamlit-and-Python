from crewai import Agent, Task, LLM
from utils.config import OPENROUTER_API_KEY

llm = LLM(
    model="openrouter/openrouter/free",
    temperature=0.4,
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)


def get_resume_cl_agent():
    return Agent(
        role="Resume & Cover Letter Writer",
        goal="Customize application materials to match job descriptions",
        backstory=(
            "You're an expert in professional writing and tailoring "
            "resumes for job applications, especially in government "
            "and tech roles."
        ),
        llm=llm,
        verbose=True
    )


def create_resume_cl_task(agent, job_summary, resume_text):
    return Task(
        description=f"""
        Based on the job summary below, tailor the candidate's resume
        summary and generate a personalized cover letter.

        --- Job Summary ---
        {job_summary}

        --- Resume Text ---
        {resume_text}

        Your output should include:

        1. An updated professional summary for the resume.
        2. A personalized cover letter suitable for a government job.

        Do not invent qualifications, skills, experience, or achievements.

        Use these exact output markers:

        <<RESUME_SUMMARY>>
        [Your tailored 3-5 sentence resume summary here]

        <<COVER_LETTER>>
        [Your personalized cover letter here]
        """,
        agent=agent,
        expected_output=(
            "A tailored resume summary of 3-5 sentences and a "
            "personalized cover letter, separated by the exact "
            "markers <<RESUME_SUMMARY>> and <<COVER_LETTER>>."
        ),
        output_file="data/resume_agent_output.txt"
    )