import tkinter as tk
from tkinter import scrolledtext, ttk
from local import TranslatorSentimentAnalyzer


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Translator Sentiment Analyzer')
        self.geometry('500x400')

        self.initUI()

    def initUI(self):
        # Input Text Widget
        self.input_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=5)
        self.input_text.insert(tk.INSERT, '')
        self.input_text.pack(pady=10)

        # Analyze Sentiment Button
        self.translate_btn = ttk.Button(self, text="Analyze Sentiment", command=self.analyze_sentiment)
        self.translate_btn.pack(pady=10)

        # Display translated text
        self.translated_text_display = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=5, state=tk.DISABLED)
        self.translated_text_display.insert(tk.INSERT, '')
        self.translated_text_display.pack(pady=10)

        # Display sentiment results
        self.result_label = ttk.Label(self, text="Sentiment Analysis:")
        self.result_label.pack()

        self.output_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=5, state=tk.DISABLED)
        self.output_text.insert(tk.INSERT, '')
        self.output_text.pack(pady=10)

    def analyze_sentiment(self):
        text = self.input_text.get("1.0", tk.END).strip()
        analyzer = TranslatorSentimentAnalyzer()

        results = analyzer.evaluate_and_report(text)
        result = results[0]

        translated_text = result['translated_text']
        self.translated_text_display.config(state=tk.NORMAL)
        self.translated_text_display.delete("1.0", tk.END)
        self.translated_text_display.insert(tk.INSERT, translated_text)
        self.translated_text_display.config(state=tk.DISABLED)

        sentiment_analysis = result['sentiment_analysis']
        display_text = "\n".join([f"{key.capitalize()}: {value}" for key, value in sentiment_analysis.items()])

        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.INSERT, display_text)
        self.output_text.config(state=tk.DISABLED)


if __name__ == '__main__':
    app = App()
    app.mainloop()
