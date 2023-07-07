import requests
from datetime import datetime, timedelta

# Stack Overflow API endpoint parameters
api_params = {
    "site": "stackoverflow",
    "pagesize": 100
}

def fetch_top_questions(tags):
    # Set up the API endpoint URL
    api_url = "https://api.stackexchange.com/2.3"

    # Code to fetch top 3 questions for the given tag from Stack Overflow API
    all_q = []
    to_date = datetime.now().strftime("%Y-%m-%d")
    from_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    for tag in tags:
        # fetch
        api_params["order"] = "desc"
        api_params["pagesize"] = 3
        api_params["sort"] = "votes"
        api_params["tagged"] = tag['name']
        api_params["fromdate"] = from_date
        api_params["todate"] = to_date
        

        try:
            # Send a GET request to the API endpoint
            response = requests.get(api_url + "/questions", params=api_params)
            

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Extract the JSON data from the response
                questions = response.json().get("items", [])
                all_q+=questions
                
            else:
                print("Error: Request failed with status code", response.status_code)

        except requests.exceptions.RequestException as e:
            print("Error:", e)
    print(all_q)
    return all_q
