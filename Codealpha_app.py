from flask import Flask, render_template, request, jsonify
import json
import re
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = Flask(__name__)


# -----------------------------
# NLTK SETUP
# -----------------------------

try:
    stop_words = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords")
    stop_words = set(stopwords.words("english"))


try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")


# -----------------------------
# NLP PREPROCESSING
# -----------------------------

def preprocess_text(text):

    # Convert to lowercase
    text = text.lower()

    # Remove numbers, punctuation and special characters
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    # Tokenize
    try:
        tokens = word_tokenize(text)
    except LookupError:
        nltk.download("punkt")
        tokens = word_tokenize(text)

    # Remove stopwords
    tokens = [
        word for word in tokens
        if word not in stop_words
    ]

    return " ".join(tokens)


# -----------------------------
# LOAD FAQ DATA
# -----------------------------

with open("faqs.json", "r", encoding="utf-8") as file:
    faqs = json.load(file)


# -----------------------------
# TF-IDF VECTORIZATION
# -----------------------------

questions = [
    preprocess_text(faq["question"])
    for faq in faqs
]

vectorizer = TfidfVectorizer()

faq_vectors = vectorizer.fit_transform(questions)


# -----------------------------
# HOME PAGE
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# CHAT API
# -----------------------------

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_question = data.get("question", "").strip()

    if not user_question:
        return jsonify({
            "answer": "Please enter a question."
        })


    # Preprocess user's question
    processed_question = preprocess_text(user_question)


    # Convert question into TF-IDF vector
    user_vector = vectorizer.transform(
        [processed_question]
    )


    # Calculate cosine similarity
    similarities = cosine_similarity(
        user_vector,
        faq_vectors
    )[0]


    # Find best matching FAQ
    best_match_index = similarities.argmax()

    best_score = similarities[best_match_index]


    # Minimum similarity threshold
    if best_score < 0.20:

        return jsonify({
            "answer": "Sorry, I couldn't find a suitable answer. Please ask a question related to Artificial Intelligence."
        })


    # Get matching answer
    answer = faqs[best_match_index]["answer"]


    return jsonify({
        "answer": answer
    })


# -----------------------------
# RUN APPLICATION
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)
