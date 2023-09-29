from transformers import MarianMTModel, MarianTokenizer
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import torch


class TranslatorSentimentAnalyzer:
    def __init__(self):
        # Setting up the translator
        self.model_name = 'Helsinki-NLP/opus-mt-cs-en'
        self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
        self.model = MarianMTModel.from_pretrained(self.model_name)

        # Setting up sentiment analysis with VADER
        nltk.download('vader_lexicon')
        self.sia = SentimentIntensityAnalyzer()

        # Initialize cache
        self.cache = {}

    def translate_to_english(self, texts):
        # Using cache
        translations = []
        for text in texts:
            if text in self.cache:
                translations.append(self.cache[text])
            else:
                try:
                    model_inputs = self.tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
                    translated = self.model.generate(**model_inputs)
                    translated_text = self.tokenizer.decode(translated[0], skip_special_tokens=True)
                    self.cache[text] = translated_text
                    translations.append(translated_text)
                except Exception as e:
                    print(f"Error translating text: {str(e)}")
                    translations.append("")
        return translations

    def analyze_sentiment(self, text):
        try:
            return self.sia.polarity_scores(text)
        except Exception as e:
            print(f"Error analyzing sentiment: {str(e)}")
            return {'pos': 0, 'neg': 0, 'neu': 1, 'compound': 0}

    def get_overall_sentiment(self, score):
        if score > 0.05:
            return "Positive"
        elif 0.05 >= score > -0.05:
            return "Neutral"
        elif -0.05 >= score > -0.6:
            return "Somewhat Negative"
        else:
            return "Very Negative"

    def evaluate_and_report(self, texts):
        if not isinstance(texts, list):
            texts = [texts]

        # Translate the texts
        translated_texts = self.translate_to_english(texts)

        # Get sentiment scores and construct reports
        reports = []
        for translated_text in translated_texts:
            sentiment_scores = self.analyze_sentiment(translated_text)

            report = {
                "translated_text": translated_text,
                "sentiment_analysis": {
                    "positive": f"{sentiment_scores['pos'] * 100:.2f}%",
                    "negative": f"{sentiment_scores['neg'] * 100:.2f}%",
                    "neutral": f"{sentiment_scores['neu'] * 100:.2f}%",
                    "overall_sentiment": self.get_overall_sentiment(sentiment_scores['compound'])
                }
            }

            reports.append(report)

        return reports


if __name__ == "__main__":
    analyzer = TranslatorSentimentAnalyzer()

    czech_texts = input("Enter the Czech text(s) to analyze (separate by '|'): ").strip().split('|')
    results = analyzer.evaluate_and_report(czech_texts)

    for idx, result in enumerate(results):
        print(f"Text {idx + 1}:")
        print("Translated Text:")
        print(result["translated_text"])
        print("\nSentiment Analysis:")
        for key, value in result["sentiment_analysis"].items():
            print(f"{key.capitalize()}: {value}")
        print("\n" + "-" * 50 + "\n")
