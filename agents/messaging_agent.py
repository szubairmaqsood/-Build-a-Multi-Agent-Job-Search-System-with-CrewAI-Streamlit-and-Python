from crewai import Agent, Task, LLM
from utils.config import OPENROUTER_API_KEY

# Configure the LLM using OpenRouter
llm = LLM(
    model="openrouter/openrouter/free",
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0.5,
)


def get_messaging_agent():
    """Create an agent specialized in professional outreach messages."""
    return Agent(
        role="Professional Job Outreach Specialist",
        goal=(
            "Write concise, personalized outreach messages that help "
            "job seekers connect professionally with recruiters "
            "and hiring managers."
        ),
        backstory=(
            "You are an experienced career communication specialist. "
            "You write engaging, professional messages tailored to "
            "job opportunities, agencies, and candidate backgrounds."
        ),
        llm=llm,
        verbose=True,
    )


def create_messaging_task(agent, job_summary, agency_name, user_bio):
    """Create a task to write a personalized outreach message."""
    return Task(
        description=f"""
        Write a brief, professional outreach message expressing the
        candidate's interest in the job opportunity.

        JOB SUMMARY:
        {job_summary}

        AGENCY OR ORGANIZATION:
        {agency_name}

        CANDIDATE BIO:
        {user_bio}

        Instructions:
        - Personalize the message using the job and candidate details.
        - Highlight relevant skills or experience from the candidate bio.
        - Express genuine interest in the opportunity.
        - Keep the tone professional, friendly, and natural.
        - Make the message suitable for LinkedIn or email.
        - Do not invent experience, qualifications, or achievements.
        - Keep the entire message under 150 words.
        """,
        expected_output=(
            "One personalized, professional outreach message under "
            "150 words, suitable for sending to a recruiter or "
            "hiring manager through LinkedIn or email."
        ),
        agent=agent,
        output_file="data/messaging_agent_output.txt",
    )