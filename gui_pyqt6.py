import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QPushButton,
                             QVBoxLayout, QWidget, QGroupBox, QHBoxLayout)
from PyQt6.QtCore import Qt
from local import TranslatorSentimentAnalyzer

# Assuming TranslatorSentimentAnalyzer class is defined here or imported


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        self.input_text = QTextEdit(self)
        self.input_text.setPlaceholderText("Enter the Czech text to analyze...")

        self.translate_btn = QPushButton("Analyze Sentiment", self)
        self.translate_btn.clicked.connect(self.analyze_sentiment)

        # Display translated text
        self.translated_text_display = QTextEdit(self)
        self.translated_text_display.setReadOnly(True)
        self.translated_text_display.setPlaceholderText("Translated Text...")

        # Group box for results
        self.result_box = QGroupBox("Results", self)
        result_layout = QVBoxLayout()

        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)

        result_layout.addWidget(self.output_text)
        self.result_box.setLayout(result_layout)

        # Add widgets to main layout
        main_layout.addWidget(self.input_text)
        main_layout.addWidget(self.translate_btn)
        main_layout.addWidget(self.translated_text_display)  # Add translated text display
        main_layout.addWidget(self.result_box)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.setWindowTitle('Translator Sentiment Analyzer')
        self.setGeometry(100, 100, 500, 400)

    def analyze_sentiment(self):
        text = self.input_text.toPlainText()
        analyzer = TranslatorSentimentAnalyzer()

        result = analyzer.evaluate_and_report(text)
        translated_text = result['translated_text']  # todo
        self.translated_text_display.setPlainText(translated_text)  # Display translated text

        sentiment_analysis = result['sentiment_analysis']
        display_text = "Sentiment Analysis:\n"
        for key, value in sentiment_analysis.items():
            display_text += f"{key.capitalize()}: {value}\n"

        self.output_text.setPlainText(display_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
