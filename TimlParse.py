from grab import Grab
from pathlib import *
from bs4 import BeautifulSoup
import re

def parse_serch_url(main_par):
    grab = Grab()
    grab.setup(timeout=30)

    line_search_system = draw_line_search_system(main_par)

    count_links = 0
    list_url_sites = []

    while count_links < int(main_par.get('links')):
        grab.setup(user_agent=None)
        grab.go(line_search_system.get('google') + str(count_links))
        for elem in grab.doc.select('//h3[@class="r"]/a/@href'):
            list_url_sites.append(elem.text())
        count_links = count_links + 10

    count_links = 0
    while count_links < int(main_par.get('links')):
        grab.setup(user_agent=None)
        grab.go(line_search_system.get('yandex') + str(count_links))
        for elem in grab.doc.select('//a[@class="link organic__url link link_cropped_no"]/@href'):
            list_url_sites.append(elem.text())
        count_links = count_links + 10

    list_url_sites = research_url_sites(list_url_sites)
    return list_url_sites


def draw_line_search_system(main_par):
    if main_par.get('date') == 'weak':
        date_search = {'google': 'qdr:w', 'yandex': '1'}
    elif main_par.get('date') == 'month':
        date_search = {'google': 'qdr:m', 'yandex': '2'}
    elif main_par.get('date') == 'all':
        date_search = {'google': '0', 'yandex': '0'}

    google_str = 'https://google.com/search?q=' + main_par.get('query') + '&hl=' + main_par.get('lan') + '&tbs=' + date_search.get('google') + '&start='
    yandex_str = 'https://yandex.ru/search/search/?text=' + main_par.get('query') + '&lang=' + main_par.get('lan') + '&within=' + date_search.get('yandex') + '&p='

    line_search_system = {'google': google_str, 'yandex': yandex_str}
    return line_search_system

def research_url_sites(list_url_sites):
    list_url_sites_result = []

    for elem in list_url_sites:
        for elem_tmp in list_url_sites:
            if elem == elem_tmp:
                list_url_sites.remove(elem)

    for elem in list_url_sites:
        if PurePosixPath(elem).suffix != ('.pdf' or '.doc' or '.docx' or '.xlsx' or '.pptx' or '.ppt' or '.zip'):
            list_url_sites_result.append(elem)

    return list_url_sites_result

def parse_html_site(list_url_sites):
    grab = Grab()
    grab.setup(timeout=30)

    html_data_site = []

    for url in list_url_sites:
        grab.setup(user_agent=None)
        grab.go(url)
        html = grab.doc.select('//body').html()
        html_data_site.append({'url': url, 'html': html})

    return html_data_site

def research_html_site(html_data_site):
    for elem in html_data_site:
        soup = BeautifulSoup(elem.get('html'), 'html.parser')

        # remove header
        [s.extract() for s in soup('header')]

        [s.extract() for s in soup.findAll(id=re.compile('head'))]

        [s.extract() for s in soup.findAll('', {'class': re.compile('head') })]

        # remove footer
        [s.extract() for s in soup('footer')]

        [s.extract() for s in soup.findAll(id=re.compile('footer'))]

        [s.extract() for s in soup.findAll('', {'class': re.compile('footer')})]

        # remove css
        [s.extract() for s in soup('style')]
        [s.extract() for s in soup('css')]

        # remove script
        [s.extract() for s in soup('script')]

        # remove menu
        [s.extract() for s in soup.findAll(id=re.compile('menu'))]

        [s.extract() for s in soup.findAll('', {'class': re.compile('menu')})]

        [s.extract() for s in soup.findAll(id=re.compile('nav'))]

        [s.extract() for s in soup.findAll('', {'class': re.compile('nav')})]

        # remove form
        [s.extract() for s in soup('form')]

        # remove other
        [s.extract() for s in soup.findAll(id=re.compile('side'))]

        [s.extract() for s in soup.findAll('', {'class': re.compile('side')})]

        [s.extract() for s in soup.findAll(id=re.compile('soc'))]

        [s.extract() for s in soup.findAll('', {'class': re.compile('soc')})]

        [s.extract() for s in soup.findAll(id=re.compile('fb'))]
        [s.extract() for s in soup.findAll(id=re.compile('vk'))]

        [s.extract() for s in soup.findAll('', {'class': re.compile('fb')})]
        [s.extract() for s in soup.findAll('', {'class': re.compile('vk')})]

        [s.extract() for s in soup.findAll(id=re.compile('copyright'))]
        [s.extract() for s in soup.findAll('', {'class': re.compile('copyright')})]

        [s.extract() for s in soup.findAll(id=re.compile('modal'))]
        [s.extract() for s in soup.findAll('', {'class': re.compile('modal')})]

        [s.extract() for s in soup('h1')]
        [s.extract() for s in soup('h2')]
        [s.extract() for s in soup('h3')]
        [s.extract() for s in soup('h4')]
        [s.extract() for s in soup('h5')]

        [s.extract() for s in soup('noindex')]

        [s.extract() for s in soup.findAll(id=re.compile('comment'))]
        [s.extract() for s in soup.findAll('', {'class': re.compile('comment')})]

        [s.extract() for s in soup.findAll(id=re.compile('widget '))]
        [s.extract() for s in soup.findAll('', {'class': re.compile('widget ')})]

        elem['soup'] = soup

    return html_data_site

def get_data_text(html_data_site):
    for elem in html_data_site:
        soup = elem.get('soup')
        data = soup.get_text()

        lines = (line.strip() for line in data.splitlines())
        lines = (line.expandtabs() for line in lines)
        chunks = (phrase.strip() for line in lines for phrase in line.split('  '))

        elem['text'] = ''.join(chunk for chunk in chunks if chunk)

    return html_data_site
