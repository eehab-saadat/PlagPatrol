from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Enter your custom search engine ID and API key here
SEARCH_ENGINE_ID = '22f500feeb8a446df'
API_KEY = ['AIzaSyAe34tm9-Og0El5ISwScopDSlYspE-XwO0','AIzaSyBOA0brUC0brGOUafT9-b9iRqNInGCAElw','AIzaSyD_HGYh0pQ3jk-VSVD-QSzR5Htf9at0p1E', 'AIzaSyBAfORIz0-AwPGogtQ9XX64qVx1xBJWj50', 'AIzaSyB-k9gC6MPO54Hfi68g7clbHXG3_OgoK9E', 'AIzaSyC0b1hAxFIDalgJNo5K7Uqx-__VqhckZpg', 'AIzaSyAPmdz598v1EwYZWEX_ip-EMHd4f2LCfVs']


def check_plagiarism(phrases, word_count):
    """
    Check the given list of phrases for plagiarism and return a tuple containing the
    percentage of plagiarized content and a dictionary with the original and plagiarism
    sources.
    Args:
        phrases: A list of phrases to check for plagiarism.
        word_count: Total number of words in the document to be checked
    Returns:
        A tuple containing a float and a dictionary with string-string key value pairs.
        The float represents the percentage of plagiarized content (as a value between 0
        and 1), and the dictionary has the original phrases as keys and the plagiarism
        sources as values.
    """

    # initializing key number
    key_number = 0

    # Initialize an empty dictionary to store the search results
    Dict = {}

    # initialize found variable
    found = 0
    # initializing loop control variable
    i = 0

    while i < len(phrases):
        #  adding qoutes to query for searching
        search = f'"{phrases[i]}"'
        try:
            # Build the service object for the Custom Search JSON API
            service = build('customsearch', 'v1', developerKey=API_KEY[key_number])
            # getting first search result
            response = service.cse().list(q=search, cx=SEARCH_ENGINE_ID, num=1).execute()
            # checking if any result was found
            if 'items' in response:
                first_url = response['items'][0]['link']
                # adding phrase plus url to dict
                Dict[phrases[i]] = first_url
                # adding number of words in phrase to found variable
                found += len(phrases[i].split())
            else:
                # adding null value if phrase not found
                Dict[phrases[i]] = ""
        except HttpError as error:
            print(f'An error occurred: {error}')
            print(error.status_code)
            if(error.status_code in [429]):
                # changing API key
                key_number += 1
                # deccrementing i to re run phrase
                i = i - 1
                if (key_number >= len(API_KEY)):
                    print('Querie limit reached')
                    break
            else : raise


        i += 1


    plag_index = format(found / word_count, ".3f")
    result = (plag_index, Dict)
    return result
