import spacy
from transformers import pipeline
from newspaper import Article
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator
from newspaper import Config

# Load necessary tools
nlp = spacy.load("en_core_web_sm")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
analyzer = SentimentIntensityAnalyzer()
translator = Translator()

def preprocess_text(text):
    """Clean and preprocess text using spaCy."""
    doc = nlp(text)
    return " ".join(token.lemma_ for token in doc if not token.is_stop and not token.is_punct)

def scrape_article(url):
    config = Config()
    config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    article = Article(url, config=config)
    article.download()
    article.parse()
    return article.text, article.title

#def scrape_title(url):
   # article = Article(url)
    #article.download()
    #article.parse()
    #return article.title

def analyze_sentiment(text):
    """Perform sentiment analysis using VADER and return both the sentiment label and score."""
    sentiment_scores = analyzer.polarity_scores(text)
    score = sentiment_scores["compound"]
    
    # Determine sentiment label based on score
    if score >= 0.1:
        sentiment = "Positive"
    elif score <= -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    return sentiment, score


def process_article(url, language):
    """End-to-end processing: scraping, preprocessing, summarizing, sentiment analysis, and translation."""
    # Step 1: Scrape and preprocess article text
    article_text, title = scrape_article(url)
    if not article_text.strip():
     return "The article could not be scraped. Try a different source.", "Neutral", "No Title"

    
    preprocessed_text = preprocess_text(article_text)
    
    summary = summarizer(article_text, max_length=200, min_length=150, do_sample=False)[0]["summary_text"]

    
    # Step 3: Translate summary if needed
    if language != "en":
        summary = translator.translate(summary, dest=language).text

    # Step 4: Perform sentiment analysis on the summary
    sentiment, score = analyze_sentiment(preprocessed_text)

    
    return summary, sentiment, title , score 