import requests
from bs4 import BeautifulSoup
from newspaper import Article
from multiprocessing import Pool
import time
import warnings

warnings.filterwarnings("ignore")

en_url = 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen'
ru_url = 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FuSjFHZ0pTVlNnQVAB?hl=ru&gl=RU&ceid=RU%3Aru'

# gets all links from the google news "stories" (full coverage / related news)
def extract_story(link):
    soup = BeautifulSoup(requests.get(link).text, 'lxml')
    result = ['https://news.google.com' + i.get('href')[1:] for i in soup.find_all('a') if i.get('href') != None and './articles' in i.get('href')]
    return result

def get_link_batch(batch):
    articles = []
    for i in enumerate(batch):
        try:
            art = Article(requests.get(i, verify=False, timeout=3).url)
            art.download()
            art.parse()
            art_dict = {
                'url': art.url,
                'gurl':  i,
                'title': art.title,
                'text': art.text,
                'pub_date': str(art.publish_date)
            }
            articles.append(art_dict)
        except Exception as e:
            print(e)
        time.sleep(1)
    return articles

# gets news.google.com last 70 article blocks 
def get_top_articles(url):
    print('[INFO] STARTED GOOGLE.NEWS SCRAPER')
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    link_groups = []
    for article_block in soup.find_all('div', class_ = 'xrnccd'):
        link_groups.append(['https://news.google.com' + i.get('href')[1:] for i in article_block.find_all('a') if i.get('href') != None and ('./article' in i.get('href') or './stories' in i.get('href'))])
    print('[INFO] GOT %s ARTICLE BLOCKS' % len(link_groups))
    
    for index, block in enumerate(link_groups):
        link_groups[index] = list(set(block))
        
    for index, block in enumerate(link_groups):
        for link in block:
            if link.startswith('https://news.google.com/stories'):
                link_groups[index].remove(link)
                link_groups[index].extend(extract_story(link))
    
    for index, block in enumerate(link_groups):
        link_groups[index] = list(set(block))
    
    print('[INFO] FINISHED GETTING LINKS')
    print('[INFO] STARTING REDIRECTING')

    p = Pool(len(link_groups))

    redirected_link_blocks = p.map(get_link_batch, link_groups)

    return [i for i in redirected_link_blocks if i != []]

def get_mirror(url):
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    block = [i.get('href') for i in soup.find_all('a') if i.get('href') != None and './articles' in i.get('href')]
    print('GOT %s ARTICLES IN MIRROR' % (str(len(block))))
    
    articles = get_link_batch(block)

    return articles