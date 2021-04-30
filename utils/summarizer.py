from transformers import pipeline
from transformers import pipeline
from bs4 import BeautifulSoup
import requests

MAX_CHUNK_SIZE = 500
URL = "https://hackernoon.com/will-the-game-stop-with-gamestop-or-is-this-just-the-beginning-2j1x32aa"

class Summarizer:
    """
    A class that takes in text in different formats and summarizer them using transformers.pipeline('Summarization')
    """

    def __init__(self,
                 book=None, max_chunk_length = MAX_CHUNK_SIZE, url=URL):
        print('Started initializing Summarizer')
        if url:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            results = soup.find_all(['h1', 'p'])
            text = [result.text for result in results]
            self.book = ' '.join(text)
        else:
            if book is None:
                self.book = None
            else:
                self.book = book
        #self.text = None
        self.model = pipeline("summarization")
        self.chunks = []
        self.max_chunk_length = max_chunk_length
        print('Done initializing Summarizer')

    def chunk_book(self):
        sentences = self.text_to_sentences(self.book)
        current_chunk = 0
        chunks = []
        for sentence in sentences:
            if len(chunks) == current_chunk + 1:
                if len(chunks[current_chunk]) + len(sentence.split(' ')) <= self.max_chunk_length:
                    chunks[current_chunk].extend(sentence.split(' '))
                else:
                    current_chunk += 1
                    chunks.append(sentence.split(' '))
            else:
                chunks.append(sentence.split(' '))

        for chunk_id in range(len(chunks)):
            chunks[chunk_id] = ' '.join(chunks[chunk_id])
        self.chunks = chunks

    def summarize_chunks(self):
        print('Started summarizing chunks')
        summaries_chunks = self.model(self.chunks, max_length=120, min_length=30, do_sample=False)
        self.summary = '\n'.join(
            ['\n'.join(self.text_to_sentences(summary_chunk['summary_text'])) for summary_chunk in summaries_chunks]
        )
        print('Finished summarizing chunks')
        return self.summary

    def text_to_sentences(self, book):
        book = book.replace('.', '.<eos>')
        book = book.replace('?', '?<eos>')
        book = book.replace('!', '!<eos>')
        sentences = book.split('<eos>')
        return sentences

def test():
    summarizer = Summarizer()
    summarizer.chunk_book()
    return summarizer.summarize_chunks()

if __name__ == '__main__':
    summarizer = Summarizer()
    summarizer.chunk_book()
    summarizer.summarize_chunks()
