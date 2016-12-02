import argparse
import bs4
import random
import requests
import os
from urlparse import urljoin

URL = "https://www.yelp.com/user_details_bookmarks?userid={}&cc=US"


def get_html(url):
    r = requests.get(url)
    if not r.ok:
        raise requests.HTTPError("Page not found, check user_id: {}".format(url))
    return bs4.BeautifulSoup(r.text, 'html.parser')


def parse_restaurant_name(html):
    return html.find_all('a', {'class': 'biz-name'})[0].text


def parse_restaurant_url(html):
    return urljoin(URL, html.find_all('a', {'class': 'biz-name'})[0]['href'])


def parse_restaurants(html):
    restaurants = html.find_all('li', {'class': 'js-bookmark-row'})
    restaurants = [(parse_restaurant_name(r), parse_restaurant_url(r)) for r in restaurants]
    return restaurants


def get_next_url(html):
    next_btn = html.find_all('a', {'class': 'next'})
    if not next_btn:
        return None
    return next_btn[0].attrs['href']


def get_bookmarked_restaurants(url):
    print("Pulling down your bookmarked restaurants...")
    html = get_html(url)
    next_url = get_next_url(html)
    restaurants = parse_restaurants(html)
    if next_url:
        return restaurants + get_bookmarked_restaurants(next_url)
    return restaurants


def random_restaurant(restaurants):
    return random.choice(restaurants)


def random_restaurants(restaurants, n):
    random.shuffle(restaurants)
    return restaurants[:n]


def load_existing_picks(filepath):
    pass


def get_weekly_picks(url):
    pass


def single_main(args):
    picks = get_bookmarked_restaurants(args.url)
    if not picks:
        raise ValueError("No restaurants found from yelp")
    print("Found {} restaurants.".format(len(restaurants)))
    restaurant = random_restaurant(restaurants)
    print("Today you will eat lunch at:\n\n{}: {}\n\nEnjoy!".format(*restaurant))


def weekly_main(args):
    picks = load_existing_picks(args.output_file)
    if not picks:
        print("Generating new weekly picks...")
        picks = get_weekly_picks(args.url)
    pick = get_todays_pick(picks)


def parse_args():
    parser = argparse.ArgumentParser(description='Pick a random lunch spot.')
    parser.add_argument('-u', '--user-id', type=str, required=True,
                        help='yelp user id')
    parser.add_argument('-f', '--output-file', type=str,
                        default=os.path.join(os.path.expanduser('~'), 'lunchpicks.csv'),
                        help='output file containing weekly picks')
    parser.add_argument('--one', action='store_true', help="random pick from all choices")
    return parser.parse_args()


def main():
    args = parse_args()
    args.url = URL.format(args.user_id)
    if args.one:
        single_main(args)
    else:
        weekly_main(args)


if __name__ == '__main__':
    main()
