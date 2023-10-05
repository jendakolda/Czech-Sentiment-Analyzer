import json
from transformers import MarianMTModel, MarianTokenizer
import nltk
import re
import string
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer
from pathlib import Path

class Translator:
    def __init__(self, model_name):
        self.model_name = model_name
        self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
        self.model = MarianMTModel.from_pretrained(self.model_name)
        self.cache = {}

    def translate(self, text):
        if text in self.cache:
            return self.cache[text]
        model_inputs = self.tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
        translated = self.model.generate(**model_inputs)
        translated_text = self.tokenizer.decode(translated[0], skip_special_tokens=True)
        self.cache[text] = translated_text
        return translated_text

class SentimentAnalyzer:
    def __init__(self):
        nltk.download('vader_lexicon')
        self.sia = SentimentIntensityAnalyzer()

    def analyze(self, text):
        return self.sia.polarity_scores(text)

class TranslatorSentimentAnalyzer:
    def __init__(self, translator_model_name='Helsinki-NLP/opus-mt-cs-en', input_file='input.txt'):
        self.translator = Translator(translator_model_name)
        self.sentiment_analyzer = SentimentAnalyzer()
        self.input_file = Path(input_file)
        self.texts = []

    def get_input_texts(self):
        if self.input_file.exists():
            with self.input_file.open("r") as file:
                self.texts = file.read().strip().split("\n\n")
        else:
            self.texts = input("Enter the Czech text(s) to analyze (separate by '|'): ").strip().split('|')

    def process_texts(self):
        results = self.evaluate_texts()

        if self.input_file.exists():
            self.save_results_to_json(results)
        else:
            for idx, result in enumerate(results):
                print(f"Text {idx + 1}:")
                print("Translated Text:")
                print(result["translated_text"])
                print("\nSentiment Analysis:")
                for key, value in result["sentiment_analysis"].items():
                    print(f"{key.capitalize()}: {value}")
                print("\n" + "-" * 50 + "\n")

            self.visualize_sentiments(results)

    def evaluate_texts(self):
        reports = []
        for idx, text in enumerate(self.texts):
            translated_text = self.translator.translate(text)
            sentiment_scores = self.sentiment_analyzer.analyze(translated_text)
            report = {
                "text_index": idx + 1,
                "original_text": text,
                "translated_text": translated_text,
                "sentiment_analysis": {
                    "pos": f"{sentiment_scores['pos'] * 100:.2f}%",
                    "neg": f"{sentiment_scores['neg'] * 100:.2f}%",
                    "neu": f"{sentiment_scores['neu'] * 100:.2f}%",
                    "overall_sentiment": self.get_overall_sentiment(sentiment_scores['compound'])
                }
            }
            reports.append(report)
        return reports

    @staticmethod
    def get_overall_sentiment(score):
        if score > 0.6:
            return "Very Positive"
        elif 0.6 >= score > 0.1:
            return "Somewhat Positive"
        elif 0.1 >= score > -0.1:
            return "Neutral"
        elif -0.1 >= score > -0.6:
            return "Somewhat Negative"
        else:
            return "Very Negative"

    @staticmethod
    def save_results_to_json(results):
        with open("output.json", "w") as file:
            json.dump(results, file, indent=4)

    def visualize_sentiments(self, sentiments):
        positive_scores = [x["sentiment_analysis"]["pos"] for x in sentiments]
        negative_scores = [x["sentiment_analysis"]["neg"] for x in sentiments]
        neutral_scores = [x["sentiment_analysis"]["neu"] for x in sentiments]

        plt.plot(positive_scores, label="Positive", color="green")
        plt.plot(negative_scores, label="Negative", color="red")
        plt.plot(neutral_scores, label="Neutral", color="blue")
        plt.ylabel('Score')
        plt.title('Sentiment Scores')
        plt.legend()
        plt.show()

if __name__ == "__main__":
    analyzer = TranslatorSentimentAnalyzer()
    analyzer.get_input_texts()
    analyzer.process_texts()
