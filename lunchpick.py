import bs4
import random
import requests

URL = "https://www.yelp.com/user_details_bookmarks?userid={}&cc=US"


def get_html(url):
    r = requests.get(url)
    if not r.ok:
        raise r.text
    return bs4.BeautifulSoup(r.text, 'html.parser')


def parse_restaurants(html):
    restaurants = html.find_all('li', {'class': 'js-bookmark-row'})
    restaurants = [r.find_all('a', {'class': 'biz-name'})[0].text for r in restaurants]
    return restaurants


def get_next_url(html):
    next_btn = html.find_all('a', {'class': 'next'})
    if not next_btn:
        return None
    return next_btn[0].attrs['href']


def get_bookmarked_restaurants(url):
    html = get_html(url)
    next_url = get_next_url(html)
    restaurants = parse_restaurants(html)
    if next_url:
        return restaurants + get_bookmarked_restaurants(next_url)
    return restaurants


def random_restaurant(url):
    restaurants = get_bookmarked_restaurants(url)
    return random.choice(restaurants)


if __name__ == '__main__':
    user_id = input("What is your Yelp user id? ")
    print("Pulling down your bookmarked restaurants...")
    restaurant = random_restaurant(URL.format(user_id))
    print("Today you will eat lunch at:\n\n{}\n\nEnjoy!".format(restaurant))
