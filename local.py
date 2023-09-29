from transformers import MarianMTModel, MarianTokenizer
from transformers import pipeline
import torch


class TranslatorSentimentAnalyzer:
    def __init__(self):
        # Setting up the translator
        self.model_name = 'Helsinki-NLP/opus-mt-cs-en'
        self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
        self.model = MarianMTModel.from_pretrained(self.model_name)

        # Setting up sentiment analysis
        self.sentiment_pipeline = pipeline("sentiment-analysis")

    def translate_to_english(self, text):
        translated = self.model.generate(**self.tokenizer.prepare_seq2seq_batch([text], return_tensors="pt"))
        translated_text = self.tokenizer.decode(translated[0], skip_special_tokens=True)
        return translated_text

    def analyze_sentiment(self, text):
        return self.sentiment_pipeline(text)

    def evaluate_and_report(self, text):
        # Translate the text
        translated_text = self.translate_to_english(text)

        # Get sentiment scores
        sentiment_scores = self.analyze_sentiment(translated_text)

        # Construct a meaningful report
        report = {
            "translated_text": translated_text,
            "sentiment_analysis": sentiment_scores
        }

        return report


if __name__ == "__main__":
    analyzer = TranslatorSentimentAnalyzer()

    czech_text = input("Enter the Czech text to analyze: ").strip()
    result = analyzer.evaluate_and_report(czech_text)

    print("\nTranslated Text:")
    print(result["translated_text"])

    print("\nSentiment Analysis:")
    for analysis in result["sentiment_analysis"]:
        print(f"Label: {analysis['label']}, Confidence: {analysis['score'] * 100:.2f}%")
