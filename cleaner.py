from scraper import get_top_articles
from summa import keywords
from collections import Counter
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import itertools

lemmatizer = WordNetLemmatizer()

def clean(news, lang):
    keyword_mapping = []
    for index, block in enumerate(news):
        kwrds = []
        for i in block:
            kwrds.extend([lemmatizer.lemmatize(w) for w in word_tokenize(i['title'].lower()) if w not in stopwords.words(lang) and w not in string.punctuation + '«»``\'\'' and w not in string.digits and len(w) >= 2])
        c = Counter(kwrds)
        keyword_mapping.append((index, [i[0] for i in c.most_common(20)]))

    combos = list(itertools.combinations(keyword_mapping, 2))
    to_merge = []
    for combo in combos:
        intersection = set(combo[0][1]) & set(combo[1][1])
        if len(intersection) / len(combo[0][1]) > 0.2 or len(intersection) / len(combo[1][1]) > 0.2:
            to_merge.append((combo[0][0], combo[1][0]))

    out = []

    while len(to_merge)>0:
        first, *rest = to_merge
        first = set(first)

        lf = -1
        while len(first)>lf:
            lf = len(first)

            rest2 = []
            for r in rest:
                if len(first.intersection(set(r)))>0:
                    first |= set(r)
                else:
                    rest2.append(r)     
            rest = rest2

        out.append(first)
        to_merge = rest

    cleaned = []

    for group in out:
        temp = []
        for i in group:
            temp.extend(news[i])
        cleaned.append(temp)

    for index, block in enumerate(news):
        if index not in set.union(*out):
            cleaned.append(block)

    return cleaned