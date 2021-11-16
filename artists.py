
import pandas as pd
import bs4 as bs
import requests

from sqlalchemy import create_engine
from decouple import config

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


WIKIART_ROOT = 'https://www.wikiart.org'

GENRE_ENDPOINT = '/en/artists-by-genre'
FIELD_ENDPOINT = '/en/artists-by-field'
SCHOOL_ENDPOINT = '/en/artists-by-painting-school'
NATIONALITY_ENDPOINT = '/en/artists-by-nation'
CENTURY_ENDPOINT = '/en/artists-by-century'
INSTITUTION_ENDPOINT = '/en/artists-by-art-institution'

DIMENSIONS = [('genre', GENRE_ENDPOINT),
              ('field', FIELD_ENDPOINT),
              ('school', SCHOOL_ENDPOINT)]

DYNAMIC_DIMENSIONS = [('century', CENTURY_ENDPOINT),
                      ('nation', NATIONALITY_ENDPOINT),
                      ('institution', INSTITUTION_ENDPOINT)]


ALPHABET_LETTERS = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                    'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                    'w', 'x', 'y', 'z', 'ø'}


def create_artist_works_endpoint(artist_endpoint: str) -> str:
    artist_endpoint = artist_endpoint.replace(' ', '-')
    artist_endpoint = artist_endpoint.lower()

    return f'{artist_endpoint}/all-works/text-list'


def create_alphabet_letter_endpoint(alphabet_letter: str) -> str:
    if alphabet_letter not in ALPHABET_LETTERS:
        raise ValueError('invalid alphabet character')

    return f'/en/Alphabet/{alphabet_letter}/text-list'


def download_facts():
    for name, _ in DIMENSIONS:
        print(f'downloading {name} facts...')
        download_artist_facts_from_static_html(name)

    for name, _ in DYNAMIC_DIMENSIONS:
        print(f'downloading {name} facts...')
        download_artist_facts_from_dynamic_html(name)


def download_artist_facts_from_static_html(dimension_name):
    dimension_df = pd.read_csv(f'data/{dimension_name}.csv')

    fact_records = []

    for _, (url, member_name) in dimension_df.iterrows():
        print(f'\t | - {member_name}')

        text_list_url = url + '/text-list'

        member_page = requests.get(text_list_url).text
        member_page = bs.BeautifulSoup(member_page, 'html5lib')

        list_selector = {'class': 'masonry-text-view masonry-text-view-all'}
        fact_list = member_page.find('div', list_selector)
        fact_list = fact_list.find_all('li')

        for fact in fact_list:
            artist_link = fact.find('a')
            artist_link = artist_link['href']

            artist_link = WIKIART_ROOT + artist_link

            fact_records.append((url, artist_link))

    facts_df = pd.DataFrame(fact_records)
    facts_df.columns = (f'{dimension_name}_url', f'artist_url')

    facts_df.to_csv(f'data/{dimension_name}_artists.csv', index=False)


def download_artist_facts_from_dynamic_html(dimension_name):
    dimension_df = pd.read_csv(f'data/{dimension_name}.csv')

    fact_records = []

    profile = webdriver.FirefoxProfile()
    profile.add_extension(extension='ublock_origin-1.37.2-an+fx.xpi')

    options = webdriver.FirefoxOptions()
    options.headless = True

    driver = webdriver.Firefox(profile, options=options)

    print(f'beginning processing ({len(dimension_df)} members)')
    for _, (url, member_name) in dimension_df.iterrows():
        print(f'\t | - {member_name}')

        driver.get(url + '#!#resultType:text')

        header_selector = (By.TAG_NAME, 'h1')
        header_wait_condition = EC.text_to_be_present_in_element(header_selector, member_name)
        header = WebDriverWait(driver, 10).until(header_wait_condition)

        if not header:
            raise Exception('header not detected')

        while True:
            try:
                load_more_element = driver.find_element_by_class_name('masonry-load-more-button')
                class_name = load_more_element.get_attribute('class')
                class_name = class_name.replace('masonry-load-more-button', '').strip()

                if class_name == 'ng-hide':
                    break

                load_more_element.click()
                driver.implicitly_wait(2)
            except (NoSuchElementException, ElementClickInterceptedException):
                break
 
        selector = (By.CSS_SELECTOR, 'div[dynamic-html=artistsHtml] > ul > li')
        wait_condition = EC.presence_of_all_elements_located(selector)
        list_items = WebDriverWait(driver, 10).until(wait_condition)

        for item in list_items:
            link = item.find_element_by_tag_name('a')
            artist_url = link.get_attribute('href')
            
            fact_records.append((url, artist_url))

    driver.quit()

    df = pd.DataFrame(fact_records)
    df.columns = (f'{dimension_name}_url', f'artist_url')

    df.to_csv(f'data/{dimension_name}_artists.csv', index=False)


def download_dimensions():
    for name, endpoint in DIMENSIONS:
        print(f'downloading {name} dimension...')
        download_dimension(name, endpoint)

    for name, endpoint in DYNAMIC_DIMENSIONS:
        print(f'downloading {name} dimension...')
        download_dimension(name, endpoint)


def download_dimension(dimension_name, endpoint):
    profile = webdriver.FirefoxProfile()
    profile.add_extension(extension='ublock_origin-1.37.2-an+fx.xpi')

    options = webdriver.FirefoxOptions()
    options.headless = True

    driver = webdriver.Firefox(profile, options=options)
    driver.get(WIKIART_ROOT + endpoint)

    records = list()

    try:
        list_items = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'dottedItem')))

        for item in list_items:
            link = item.find_element_by_tag_name('a')
            url = link.get_attribute('href')
            name = link.text.split(' ')
            name = name[:len(name) - 1]
            name = ' '.join(name)

            records.append((url, name))

    finally:
        driver.quit()

    df = pd.DataFrame(records)
    df.columns = (f'{dimension_name}_url', f'{dimension_name}_name')

    df.to_csv(f'data/{dimension_name}.csv', index=False)


def download_artists():
    artist_records = []

    for letter in ALPHABET_LETTERS:
        print(f'downloading artists ({letter})...')
        letter_endpoint = create_alphabet_letter_endpoint(letter)
        letter_endpoint = WIKIART_ROOT + letter_endpoint

        letter_list_page = requests.get(letter_endpoint).text
        letter_list_page = bs.BeautifulSoup(letter_list_page, 'html5lib')

        list_selector = {'class': 'masonry-text-view masonry-text-view-all'}
        letter_list = letter_list_page.find('div', list_selector)
        letter_list = letter_list.find_all('li')

        for list_item in letter_list:
            artist_link = list_item.find('a')
            artist_url = WIKIART_ROOT + artist_link['href']
            artist_works_url = create_artist_works_endpoint(artist_url)
            artist_name = artist_link.text

            record = (artist_url, artist_works_url, artist_name)

            artist_records.append(record)


    artists_df = pd.DataFrame(artist_records)
    artists_df.columns = ('artist_url', 'artist_works_url', 'artist_name')

    artists_df.to_csv('data/artists.csv', index=False)


def download_artist_works():
    artists_df = pd.read_csv('artists.csv')

    work_records = []

    for _, artist in artists_df.iterrows():
        print('downloading ' + artist['artist_name'] + '...')
        artist_works_url = artist['artist_works_url']
        artist_works_page = requests.get(artist_works_url).text
        artist_works_page = bs.BeautifulSoup(artist_works_page, 'html5lib')

        work_selector = {'class': 'painting-list-text-row'}
        artist_works_list = artist_works_page.find_all('li', work_selector)

        for work_list_item in artist_works_list:
            work_link = work_list_item.find('a')

            if work_link is not None:
                work_url = WIKIART_ROOT + work_link['href']
                items = work_list_item.find_all('span')
                if len(items) == 2:
                    work_title = items[0].text
                    work_year = items[1].text
                elif len(items) == 1:
                    work_title = work_link.text
                    work_year = items[0].text

                if work_year:
                    work_year = work_year.replace(',', '').strip()
            else:
                work_url = None
                items = work_list_item.find_all('span')
                work_title = items[0].text
                work_year = items[1].text
                if work_year:
                    work_year = work_year.replace(',', '').strip()

            work_record = (artist_works_url, work_url, work_title, work_year)
            work_records.append(work_record)

    works_df = pd.DataFrame(work_records)
    works_df.columns = ('artist_works_url', 'work_url', 'work_title',
                        'year_created')

    works_df.to_csv('data/artist_works.csv', index=False)


def load_database():
    USER = config('USER')
    PASSWORD = config('PASSWORD')
    IP_ADDRESS = config('IP_ADDRESS')
    DATABASE = 'wikiart'

    conn_str = f'mysql+pymysql://{USER}:{PASSWORD}@{IP_ADDRESS}/{DATABASE}'
    mysql_conn = create_engine(conn_str)

    artists_df = pd.read_csv('data/artists.csv')
    artist_works_df = pd.read_csv('data/artist_works.csv')
    
    artists_df.to_sql('stg_artists', mysql_conn, if_exists='replace', index=False)
    artist_works_df.to_sql('stg_works', mysql_conn, if_exists='replace', index=False)

    for dimension, _ in DIMENSIONS + DYNAMIC_DIMENSIONS:
        dimension_df = pd.read_csv(f'data/{dimension}.csv')
        facts_df = pd.read_csv(f'data/{dimension}_artists.csv')

        dimension_df.to_sql(f'stg_{dimension}', mysql_conn, if_exists='replace', index=False)
        facts_df.to_sql(f'stg_{dimension}_artists', mysql_conn, if_exists='replace', index=False)
    

if __name__ == '__main__':
    # download_artists()
    # download_artist_works()
    # download_dimensions()
    # download_facts()

    load_database()
