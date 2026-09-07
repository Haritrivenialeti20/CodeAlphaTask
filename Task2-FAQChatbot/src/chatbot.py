import json
import re
from pathlib import Path

import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Make sure required NLTK resources are available
try:
    STOP_WORDS = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords")
    STOP_WORDS = set(stopwords.words("english"))


# Locate the FAQ dataset
BASE_DIR = Path(__file__).resolve().parent.parent
FAQ_FILE = BASE_DIR / "data" / "faqs.json"


def load_faqs():
    """Load FAQs from the JSON knowledge base."""
    with open(FAQ_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def preprocess_text(text):
    """Clean and normalize user text."""
    text = text.lower()

    # Keep only letters and spaces
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # Split into words
    words = text.split()

    # Remove common English stop words
    words = [
        word for word in words
        if word not in STOP_WORDS
    ]

    return " ".join(words)


class FAQChatbot:
    """FAQ chatbot using TF-IDF and cosine similarity."""

    def __init__(self, threshold=0.20):
        self.faqs = load_faqs()
        self.threshold = threshold

        # Extract FAQ questions
        self.questions = [
            faq["question"]
            for faq in self.faqs
        ]

        # Preprocess FAQ questions
        self.processed_questions = [
            preprocess_text(question)
            for question in self.questions
        ]

        # Create TF-IDF model
        self.vectorizer = TfidfVectorizer()

        # Convert FAQ questions into vectors
        self.question_vectors = self.vectorizer.fit_transform(
            self.processed_questions
        )

    def get_response(self, user_question):
        """Find the most relevant FAQ answer."""

        if not user_question or not user_question.strip():
            return {
                "answer": "Please enter a question.",
                "score": 0.0,
                "matched_question": None
            }

        # Preprocess user's question
        processed_question = preprocess_text(user_question)

        # Convert user's question into a TF-IDF vector
        user_vector = self.vectorizer.transform(
            [processed_question]
        )

        # Calculate similarity with every FAQ
        similarities = cosine_similarity(
            user_vector,
            self.question_vectors
        )[0]

        # Find the best match
        best_index = similarities.argmax()
        best_score = float(similarities[best_index])

        # Get the matching FAQ
        matched_faq = self.faqs[best_index]

        # Check similarity threshold
        if best_score < self.threshold:
            return {
                "answer": (
                    "Sorry, I couldn't find a relevant answer "
                    "to your question. Please try asking in a "
                    "different way."
                ),
                "score": best_score,
                "matched_question": None
            }

        return {
            "answer": matched_faq["answer"],
            "score": best_score,
            "matched_question": matched_faq["question"]
        }


# Simple command-line test
if __name__ == "__main__":
    chatbot = FAQChatbot()

    print("FAQ Chatbot")
    print("Type 'exit' to quit.")
    print("-" * 40)

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break

        result = chatbot.get_response(user_input)

        print("Chatbot:", result["answer"])
        print(
            f"Similarity score: {result['score']:.2f}"
        )
        print()