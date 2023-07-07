import requests


# Stack Overflow API endpoint parameters

api_params = {
    "site": "stackoverflow",
    "pagesize": 100
}
def fetch_popular_tags():
    # Set up the API endpoint URL
    api_url = "https://api.stackexchange.com/2.3"

    try:
        # Send a GET request to the API endpoint
        # Set the query parameters
        api_params["sort"] = "popular"
        api_params["pagesize"] = 3
        response = requests.get(api_url + "/tags", params=api_params)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract the JSON data from the response
            tags = response.json().get("items", [])
            # Extract the top 10 popular tags from the response data
            print(tags)
            return tags
        else:
            print("Error: Request failed with status code", response.status_code)

    except requests.exceptions.RequestException as e:
        print("Error:", e)
