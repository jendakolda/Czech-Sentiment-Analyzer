# Czech-Sentiment-Analyzer
Skript for monitoring sentiments of social media posts
Use:
remote.py for text evaluation via chatGPT api. Requires apikey and paid subscription
local.py locally translates text to english and evaluates sentiment
gui_pyqt6.py Qt6 GUI wrapped on locally.py
gui_tkinter.py  Simpler GUI without the need to install dependencies
Note: if there are errors while trying to run Qt6, try: 
sudo apt-get install libxcb*

TODO:
 - monitoring of sentiment trends over time
 - connection to DB (sql) for storage of previously evaluated posts
 - Graphic interpretation of results and trends
 - Recreate the whole thing in jupyter nb or google colab
 - Introduce topic sorting for evaluated posts:
   1) general sentiment about the military's involvement,
   2) opinions about the refugees
   3) sentiment about the crisis as a whole