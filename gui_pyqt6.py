import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QLabel, QWidget
from PyQt6.QtCore import Qt
import os
from local import TranslatorSentimentAnalyzer


# Assuming TranslatorSentimentAnalyzer class is defined here or imported

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setFixedWidth(500)
        self.input_text = QTextEdit(self)
        self.input_text.setPlaceholderText("Enter the Czech text to analyze...")

        self.translate_btn = QPushButton("Analyze Sentiment", self)
        self.translate_btn.clicked.connect(self.analyze_sentiment)

        self.output_label = QLabel(self)
        self.output_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout.addWidget(self.input_text)
        layout.addWidget(self.translate_btn)
        layout.addWidget(self.output_label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setWindowTitle('Translator Sentiment Analyzer')
        self.setGeometry(100, 100, 500, 400)

    def analyze_sentiment(self):
        text = self.input_text.toPlainText()
        analyzer = TranslatorSentimentAnalyzer()

        result = analyzer.evaluate_and_report(text)
        translated_text = result['translated_text']
        sentiment_analysis = result['sentiment_analysis']

        display_text = f"Translated Text:\n{translated_text}\n\n"
        display_text += "Sentiment Analysis:\n"
        for key, value in sentiment_analysis.items():
            display_text += f"{key.capitalize()}: {value}\n"

        self.output_label.setText(display_text)


if __name__ == '__main__':
    os.environ['QT_QPA_PLATFORM'] = 'xcb'
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
