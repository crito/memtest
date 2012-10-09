import requests
from BeautifulSoup import BeautifulSoup as Soup
import copy


results = []


def application(environ, start_response):
    def recurse_links(content):
        soup = Soup(content)
        for link in soup.findAll('a'):
            try:
                # yield '<li>Requesting %s</li>' % link.get('href')
                resp = requests.get(link.get('href'))
                if resp.status_code == 200:
                    results.append(resp.content)
                    r = copy.deepcopy(results)
                    for i in r:
                        results.append(i)
                    recurse_links(resp.content)
            except:
                pass
        raise Exception
    start_response('200 OK', [('Content-Type', 'text/html')])
    resp = requests.get('http://news.ycombinator.com')
    results.append(resp.content)
    try:
        recurse_links(resp.content)
    except:
        pass
    yield 'done'
