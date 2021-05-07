# nlp_algorythm
This project creates a local Flask app and lets your summarize text. It will also do a sentiment analysis and try to visualize it.

The first field will accept any raw text.

The second field will accept an url that goes to an html document like this one: https://www.gutenberg.org/files/103/103-h/103-h.htm

You can find many such html files on https://www.gutenberg.org
# Execution

Just run app.py and the local Flask app will launch.

# Create an environment with Anaconda

Create conda env

    - `conda create -n nlp_becode python=3.6`
 
 
 Activate env:
 
     - `conda activate nlp_becode`


Install flair:

     - `pip install flair`
 
 
Installing spacy

    - `conda install -c conda-forge spacy`

    - `python -m spacy download en_core_web_sm`

Installing Flask:

    - `conda install -c anaconda flask`

Installing Pandas:

    - `conda install -c anaconda pandas`

Installing vadersentiment:

    -  `conda install -c conda-forge vadersentiment`

Installing beautifulsoup4:

    -   `conda install -c anaconda beautifulsoup4`
