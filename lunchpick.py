import argparse
import bs4
import random
import requests

URL = "https://www.yelp.com/user_details_bookmarks?userid={}&cc=US"


def get_html(url):
    r = requests.get(url)
    if not r.ok:
        raise requests.HTTPError("Page not found, check user_id: {}".format(url))
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


def random_restaurant(restaurants):
    return random.choice(restaurants)


def format_url(args):
    url = URL.format(args.user_id)
    if args.label:
        url += '&label={}'.format(args.label)
    return url


def parse_args():
    parser = argparse.ArgumentParser(description='Pick a lunch spot.')
    parser.add_argument('-u', '--user_id', type=str, required=True,
                        help='yelp user id')
    parser.add_argument('-l', '--label', type=str, help='bookmark label')
    return parser.parse_args()


def main():
    args = parse_args()
    url = format_url(args)
    print("Pulling down your bookmarked restaurants...")
    restaurants = get_bookmarked_restaurants(url)
    if not restaurants:
        raise ValueError("No restaurants found!")
    print("Found {} restaurants.".format(len(restaurants)))
    restaurant = random_restaurant(restaurants)
    print("Today you will eat lunch at:\n\n{}\n\nEnjoy!".format(restaurant))


if __name__ == '__main__':
    main()
