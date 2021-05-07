from transformers import pipeline

MAX_CHUNK_SIZE = 500
URL = "https://hackernoon.com/will-the-game-stop-with-gamestop-or-is-this-just-the-beginning-2j1x32aa"

class Summarizer:
    """
    A class that takes in text in different formats and summarizer them using transformers.pipeline('Summarization')
    """

    def __init__(self,
                 book=None, max_chunk_length = MAX_CHUNK_SIZE, url=URL):
        print('Started initializing Summarizer')
        if book is None:
            self.book = None
        else:
            self.book = book
        self.model = pipeline("summarization", model='facebook/bart-large-cnn')
        self.chunks = []
        self.max_chunk_length = max_chunk_length
        print('Done initializing Summarizer')

    def set_book(self, book, url=False):
        self.book = book

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
        l = len(self.chunks)
        summaries_chunks = []
        for i, chunk in enumerate(self.chunks):
            if i > 3:
                break
            print(f'{i+1} of {l}')
            res = self.model(chunk, max_length=120, min_length=30, do_sample=False)
            print(res)
            summaries_chunks.append(res[0])

        print('summaries_chunks')
        print(summaries_chunks)
        self.summary = '\n'.join(
            ['\n'.join(self.text_to_sentences(summary_chunk['summary_text'])) for summary_chunk in summaries_chunks]
        )
        print('Finished summarizing chunks')
        return self.summary

    def summarize_chunk(self, chunk):
        summary = self.model(chunk, max_length=120, min_length=30, do_sample=False)
        return summary

    def text_to_sentences(self, book):
        book = book.replace('.', '.<eos>')
        book = book.replace('?', '?<eos>')
        book = book.replace('!', '!<eos>')
        sentences = book.split('<eos>')
        return sentences

from utils.scraper import scrape_url
if __name__ == '__main__':
    url = 'https://www.gutenberg.org/files/103/103-h/103-h.htm'
    summarizer = Summarizer()
    book = scrape_url(url)
    summarizer.set_book(book)
    summarizer.chunk_book()
    summ = summarizer.summarize_chunks()
    print(summ)
