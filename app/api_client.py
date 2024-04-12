import requests





def get_random_word_and_definition():
    url = f"{WORDS_API_URL}?hasDetails=definitions&random=true"
    headers = {
        "X-RapidAPI-Key": WORDS_API_KEY,
        "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            word = data["word"]
            definition = data["results"][0]['definition']
            pronunciation = data.get('pronunciation', {"all": "Unknown"})['all']
            return word, definition, pronunciation
        else:
            return None, f"Failed to retrieve word: {response.status_code}"
    except Exception as e:
        return None, f"Error: {str(e)}"
