from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Enter your custom search engine ID and API key here
SEARCH_ENGINE_ID = '05a0718899f664fda'
API_KEY = 'AIzaSyAe34tm9-Og0El5ISwScopDSlYspE-XwO0'


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
    # Build the service object for the Custom Search JSON API
    service = build('customsearch', 'v1', developerKey=API_KEY)

    # Initialize an empty dictionary to store the search results
    Dict = {}

    # initialize found variable
    found = 0

    for phrase in phrases:
        #  adding qoutes to query for searching
        search = f'"{phrase}"'
        try:
            # getting first search result
            response = service.cse().list(q=search, cx=SEARCH_ENGINE_ID, num=1).execute()
            # checking if any result was found
            if 'items' in response:
                first_url = response['items'][0]['link']
                # adding phrase plus url to dict
                Dict[phrase] = first_url
                # adding number of words in phrase to found variable
                found += len(phrase.split())
            else:
                # adding null value if phrase not found
                Dict[phrase] = ""
        except HttpError as error:
            print(f'An error occurred: {error}')
            Dict[phrase] = None

    plag_index = format(found / word_count, ".3f")
    result = (plag_index, Dict)
    return result

