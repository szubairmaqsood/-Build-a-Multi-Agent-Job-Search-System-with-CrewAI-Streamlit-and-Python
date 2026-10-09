
# Import requests to send HTTP requests to the USAJobs API
import requests

# Import the USAJobs API key from our configuration file
from utils.config import USAJOBS_API_KEY


# Define a function to search for jobs using a keyword and location
def fetch_usajobs(keyword, location="remote", results_per_page=5):

    # USAJobs API endpoint used to search for job vacancies
    url = "https://data.usajobs.gov/api/search"

    # Headers provide authentication and identify the API request
    headers = {
        "Host": "data.usajobs.gov",
        "User-Agent": "szubair1833@gmail.com",
        "Authorization-Key": USAJOBS_API_KEY,
    }

    # Parameters define what jobs we want to search for
    params = {
        "Keyword": keyword,                  # Job title or search keyword
        "LocationName": location,            # Desired job location
        "ResultsPerPage": results_per_page,  # Maximum number of results
    }

    # Send a GET request to USAJobs with the headers and search parameters
    # timeout=30 means the request will stop waiting after 30 seconds
    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30,
    )

    # Display the HTTP status code to help diagnose API issues
    print("HTTP status:", response.status_code)

    # If the API request failed, print the error response and return an empty list
    if response.status_code != 200:
        print("API response:", response.text[:1000])
        return []

    # Convert the JSON response into a Python dictionary
    # Extract the list of job results from the response
    return response.json().get(
        "SearchResult", {}
    ).get("SearchResultItems", [])


# This block runs only when this file is executed directly
# It does not run when another Python file imports this module
if __name__ == "__main__":

    # Search for up to 10 Business Analyst jobs in New York
    jobs = fetch_usajobs(
        "business analyst",
        location="New York",
        results_per_page=10,
    )

    # Check whether the API returned any jobs
    if not jobs:
        print("No jobs returned. Check the status and API response above.")

    else:
        # Process each job returned by the API
        for job in jobs:

            # Get the main details for the current job
            details = job["MatchedObjectDescriptor"]

            # Extract the job title and organization name
            # Use a fallback value if either field is missing
            title = details.get("PositionTitle", "Unknown title")
            agency = details.get("OrganizationName", "Unknown agency")

            # Print the job title and organization
            print(f"{title} at {agency}")
