from flask import Flask, render_template, request
from summarizer import process_article

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    sentiment = ""
    title = ""
    score = ""
    
    if request.method == "POST":
        url = request.form.get("url")
        language = request.form.get("language")
        
        # Process article to get summary and sentiment
        summary, sentiment, title, score= process_article(url, language)
        
    return render_template("index.html", summary=summary, sentiment=sentiment, title=title, score=score)

if __name__ == "__main__":
    app.run(debug=True) 