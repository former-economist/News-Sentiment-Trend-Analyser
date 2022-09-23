from gnews import GNews
from textblob import TextBlob


def create_search_string(topic: str, blocked_words: list):
    """Funcition to create the search from http request.

    Args:
        topic (str): The user searched topic.
        blocked_words (list): A list of words to that show not occur in returned results

    Returns:
        str: A string containing search topic, and excluded terms prefixed by a dash.
    """
    primary_search = str(topic)
    if len(primary_search) >= 1:
        excluded_terms = blocked_words
        for word in excluded_terms:
            str_word = str(word)
            if len(str_word) > 0:
                dash = ' -'
                dash += str_word
                primary_search += dash

        return primary_search
    else:
        raise Exception("Topic arguement must not be blank")


def create_instance():
    """A function that creates an instance object of a GNews

    Returns:
        GNews: A google news class object that will be used to carry out searches.
    """
    google_object = GNews(country="GB")
    return google_object


def search(topic: str, google_object: GNews):
    """A function that is used to search for article of the topics.

    Args:
        topic (str): The search topic including terms for exlcusion
        google_object (GNews): The object instance of GNews.

    Returns:
        list: A list of JSON objects containing 
    """
    make_string = str(topic)
    results = google_object.get_news(make_string)

    if len(results) < 1:
        raise Exception("Search could not find news for topic, try rephrasing")

    return results


def calculate_sentiment(article):
    """
    A function that finds the sentiment values of an article
    and adds the sentiment value to the article json.

    Args:
        search_results (_type_): _description_
    """
    string = article['title']
    string += " "
    string += article['description']
    blob = TextBlob(string)
    sentiment = blob.sentiment.polarity
    article['sentiment'] = sentiment
    return article['sentiment']
