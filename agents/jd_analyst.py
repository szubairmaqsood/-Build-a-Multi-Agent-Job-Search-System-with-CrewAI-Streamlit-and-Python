
from crewai import Agent, Task, LLM
from utils.config import OPENROUTER_API_KEY

# Connect CrewAI to a free model through OpenRouter
llm = LLM(
    model="openrouter/openrouter/free",
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0.2,
)


def get_jd_analyst_agent():
    # Define the AI agent responsible for analyzing job descriptions
    return Agent(
        role="JD Analyst",
        goal="Understand and summarize government job postings",
        backstory=(
            "You're an expert in job market analysis "
            "with a focus on US federal job listings."
        ),
        llm=llm,
        verbose=True,
    )


def create_jd_analysis_task(agent, job_description):
    # Define the task the agent must complete
    return Task(
        description=f"""
        Analyze the following USAJobs job posting and extract:
        - A summary of the role
        - Key skills required
        - Specific qualifications or eligibility requirements

        Job Description:
        {job_description}
        """,
        expected_output=(
            "A structured Markdown report with sections for "
            "Qualifications, Required Skills, and Responsibilities."
        ),
        agent=agent,
        output_file="data/report.md",
    )
