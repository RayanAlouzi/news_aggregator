import requests
from bs4 import BeautifulSoup
import spacy



# show the entire article as text from the url
def fetch_full_article(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request succeeded
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # You may need to adjust the selector depending on the HTML structure of the webpage
    content = soup.find_all(['p', 'h1', 'h2', 'h3'])  # Assuming the text is within these tags
    full_text = ' '.join([tag.get_text() for tag in content])
    return full_text


# Function to fetch news from the News API
def fetch_news(query):
    base_url = "https://newsapi.org/v2/everything?"
    api_key = "c0dfeafa5a984f4eb3a64f894a961093"
    params = {
        'q': query, 
        'apiKey': api_key,
        'language': 'en',
    }
    response = requests.get(base_url, params=params)
    return response.json()



# Function to fetch the Wikidata item
def get_wikidata_item(item_id):
    url = "https://www.wikidata.org/w/api.php"
    params = {
        'action': 'wbgetentities',
        'ids': item_id,
        'format': 'json'
    }
    response = requests.get(url, params=params)
    return response.json()


def main(): 
    query = input("Enter a search term: ")
    news = fetch_news(query)
    news_articles = news['articles']
    first_article = news_articles[0]
    print(first_article)
    text = fetch_full_article(first_article["url"])
    # Load English tokenizer, tagger, parser and NER
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    # Analyze syntax
    print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
    print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

    # Find named entities, phrases and concepts
    for entity in doc.ents:
        print(entity.text, entity.label_)

main()