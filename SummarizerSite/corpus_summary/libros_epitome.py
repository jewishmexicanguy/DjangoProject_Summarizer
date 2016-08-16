"""
This script will use the following packages 
    NLTK,
    Beautiful Soup

It also uses the following python libraries
    urllib.request
"""

from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest

from urllib.request import urlopen
from bs4 import BeautifulSoup

class FrequencySummarizer:
    def __init__(self, min_cut=0.1, max_cut=0.9):
        """
        Initilize the text summarizer.
        Words that have a frequency term lower than min_cut 
        or higer than max_cut will be ignored.
        """
        self._min_cut = min_cut
        self._max_cut = max_cut 
        self._stopwords = set(stopwords.words('english') + list(punctuation))

    def _compute_frequencies(self, word_sent):
        """ 
        Compute the frequency of each of word.
        Input: 
        word_sent, a list of sentences already tokenized.
        Output: 
        freq, a dictionary where freq[w] is the frequency of w.
        """
        freq = defaultdict(int)
        for s in word_sent:
            for word in s:
                if word not in self._stopwords:
                    freq[word] += 1
        # frequencies normalization and filtering
        m = float(max(freq.values()))
        freq_list = list(freq.keys())
        for w in freq_list:
            freq[w] = freq[w]/m
            if freq[w] >= self._max_cut or freq[w] <= self._min_cut:
                del freq[w]
        return freq

    def summarize(self, text, n):
        """
        Return a list of n sentences 
        which represent the summary of text.
        """
        sents = sent_tokenize(text)
        #assert n <= len(sents) # we take this out because we want to see what the article is without this assertion triggering an error
        word_sent = [word_tokenize(s.lower()) for s in sents]
        self._freq = self._compute_frequencies(word_sent)
        ranking = defaultdict(int)
        for i,sent in enumerate(word_sent):
            for w in sent:
                if w in self._freq:
                    ranking[i] += self._freq[w]
        sents_idx = self._rank(ranking, n)    
        return [sents[j] for j in sents_idx]

    def _rank(self, ranking, n):
            """ return the first n sentences with highest ranking """
            return nlargest(n, ranking, key=ranking.get)

def get_only_text(url):
    """ 
    return the title and the text of the article
    at the specified url
    """
    page = urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(page)
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return soup.title.text, text

def find_xml_links(xml_map):
    """
    Check to make sure that to_summarize list was acutally able to find a body of text to parse.
    """
    to_summarize = list(
        map(
            lambda i: i.text,
            xml_map.find_all('guid')
        )
    )
    # if nothing was found with a tag of guid then search for link
    if len(to_summarize) < 1:
        to_summarize = list(
            map(
                lambda i: i.text,
                xml_map.find_all('link')
            )
        )
    return to_summarize
    print('request object intro spection:')
    methodList = [method for method in dir(request) if callable(getattr(request, method))]
    for i in methodList:
        print(i)

def summarize_from_rss_feeds(urls):
    """
    This function will accept a list of urls that are rss feeds served as xml and attempt to parse bodies of text and summarize them.
    """
    # open some object that allows us to write our analysis, for now just write out too a text file
    # later on we will want to wrtie an entry in a database of some sort
    f = open('rss_sumaries', 'a')
    for i in urls:
        f.write('<URL ' + i + ' />\r\n')
        feed = BeautifulSoup(urlopen(i).read().decode('utf8'), "html.parser")
        # we need a function that will try to find xml tags that has url of the text body to summarize.
        to_summarize = find_xml_links(feed)
        fs = FrequencySummarizer()
        for article_url in to_summarize[:5]:
            title, text = get_only_text(article_url)
            f.write('--------------------------------------------------------\r\n')
            f.write(title)
            f.write('\r\n')
            f.write(article_url)
            f.write('\r\n')
            f.write('\r\n')
            for s in fs.summarize(text, 2):
                f.write('* ' + s)
    f.close()

def summarize_from_raw_text(corpus, title, num_pages = 2):
    fs = FrequencySummarizer()
    summary = 'number of pages: ' + str(num_pages) + '\r\n\r\n'
    for s in fs.summarize(corpus, num_pages):
        summary += '/r/n* ' + s
    return summary

xml_feeds = [
    'http://feeds.bbci.co.uk/news/rss.xml',
    'http://www.nytimes.com/roomfordebate/topics/politics.rss.xml',
    'http://www.politico.com/rss/politics08.xml',
    'http://www.debate.org/rss/debates/Politics.xml',
    'http://www.debate.org/rss/debates/Technology.xml'
]

