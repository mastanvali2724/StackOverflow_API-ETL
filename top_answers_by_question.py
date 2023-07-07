import requests

# Stack Overflow API endpoint parameters
api_params = {
    'site' : 'stackoverflow',
    'pagesize' : 10
}

def fetch_answers(questions):
    # Set up the API endpoint URL
    api_url = "https://api.stackexchange.com/2.3"

    all_ans = []
    for question in questions:
        api_params['pagesize'] = 3
        api_params['order'] = 'desc'
        api_params['sort'] = 'votes'
        api_params['ids'] = question['question_id']
        api_params['filter'] = '!nNPvSNXCix'

        try:
            # Send a GET request to the API endpoint
            response = requests.get(api_url + f"/questions/{question['question_id']}/answers" , params=api_params)

            # Check if the request was successful (status code 200)
            if(response.status_code == 200):
                # Extract the JSON data from the response
                answers = response.json().get("items", [])
                all_ans += answers
            else:
                print("Error: Request failed with status code:", response.status_code)

        except requests.exceptions.RequestException as e:
            print("Error: ", e)

    print(all_ans)
    return all_ans

