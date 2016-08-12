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

#We can finally apply our summarizer on a set of xml feeds that each have thier own set of articles

xml_feeds = [
    'http://feeds.bbci.co.uk/news/rss.xml',
    'http://www.nytimes.com/roomfordebate/topics/politics.rss.xml',
    'http://www.politico.com/rss/politics08.xml',
    'http://www.debate.org/rss/debates/Politics.xml',
    'http://www.debate.org/rss/debates/Technology.xml'
]
f = open('rss_sumaries', 'a')
for i in xml_feeds:
    f.write(i)
    feed = BeautifulSoup(urlopen(i).read().decode('utf8'), "html.parser")
    to_summarize = list(map(lambda p: p.text, feed.find_all('guid')))
    # not all rss feeds have guid keys, some use the link xml key instead
    if(len(to_summarize) < 1):
        to_summarize = list(map(lambda p: p.text, feed.find_all('link'),))

    fs = FrequencySummarizer()
    for article_url in to_summarize[:5]:
        title, text = get_only_text(article_url)
        f.write('--------------------------------------------------------\r\n')
        #print('----------------------------------')
        #print(title)
        f.write(title)
        f.write('\r\n')
        #print(article_url)
        f.write(article_url)
        f.write('\r\n')
        f.write('\r\n')
        for s in fs.summarize(text, 2):
            #print('*',s)
            f.write('* ' + s)
f.close()