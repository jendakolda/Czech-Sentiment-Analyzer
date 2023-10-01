import tkinter as tk
from tkinter import scrolledtext
from local import TranslatorSentimentAnalyzer

# Assuming TranslatorSentimentAnalyzer class is defined here or imported


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Translator Sentiment Analyzer')
        self.geometry('500x400')

        self.input_label = tk.Label(self, text="Enter the Czech text to analyze:")
        self.input_label.pack(pady=10)

        self.input_text = scrolledtext.ScrolledText(self, height=10, wrap=tk.WORD)
        self.input_text.pack(pady=10, padx=10, fill=tk.BOTH)

        self.translate_btn = tk.Button(self, text="Analyze Sentiment", command=self.analyze_sentiment)
        self.translate_btn.pack(pady=10)

        self.output_label = tk.Label(self, text="Results:")
        self.output_label.pack(pady=10)

        self.output_text = scrolledtext.ScrolledText(self, height=10, wrap=tk.WORD)
        self.output_text.pack(pady=10, padx=10, fill=tk.BOTH)

    def analyze_sentiment(self):
        text = self.input_text.get("1.0", tk.END)
        analyzer = TranslatorSentimentAnalyzer()

        result = analyzer.evaluate_and_report(text)
        translated_text = result['translated_text']
        sentiment_analysis = result['sentiment_analysis']

        display_text = f"Translated Text:\n{translated_text}\n\n"
        display_text += "Sentiment Analysis:\n"
        for key, value in sentiment_analysis.items():
            display_text += f"{key.capitalize()}: {value}\n"

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, display_text)

if __name__ == '__main__':
    app = App()
    app.mainloop()
