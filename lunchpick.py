import argparse
import bs4
import datetime
import json
import random
import requests
import os
from toolz import pipe
from urlparse import urljoin

URL = "https://www.yelp.com/user_details_bookmarks?userid={}&cc=US"
DAYS_IN_WEEK = 7
DATE_FORMAT = "%Y%m%d"


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
    print("Found {} restaurants.".format(len(restaurants)))
    return restaurants


def random_restaurant(restaurants):
    return random.choice(restaurants)


def random_restaurants(restaurants, n):
    random.shuffle(restaurants)
    return restaurants[:n]


def load_existing_picks(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as pick_file:
        data = json.load(pick_file)
    data["date_generated"] = datetime.datetime.strptime(data["date_generated"], DATE_FORMAT).date()
    days_til_expire = 7 - data["date_generated"].weekday()
    expire_day = data["date_generated"] + datetime.timedelta(days_til_expire)
    if datetime.date.today() >= expire_day:
        return None
    return data["picks"]


def write_picks(picks, filepath):
    data = {"date_generated": datetime.date.today().strftime(DATE_FORMAT),
            "picks": picks}
    with open(filepath, 'w') as pick_file:
        json.dump(data, pick_file)
    print("Wrote lunch picks for the next week to: {}".format(filepath))


def get_weekly_picks(url, filepath):
    restaurants = get_bookmarked_restaurants(url)
    picks = random_restaurants(restaurants, DAYS_IN_WEEK)
    if len(picks) < DAYS_IN_WEEK:
        raise ValueError("Not enough restaurants to generate a week. Try the --one option.")
    write_picks(picks, filepath)
    return picks


def get_todays_pick(picks):
    day_of_week = datetime.date.today().weekday()
    return picks[day_of_week]


def print_pick(pick):
    print("Today you will eat lunch at:\n\n{}: {}\n\nEnjoy!".format(*pick))


def single_main(args):
    picks = get_bookmarked_restaurants(args.url)
    if not picks:
        raise ValueError("No restaurants found from yelp")
    pipe(picks, random_restaurant, print_pick)


def weekly_main(args):
    picks = load_existing_picks(args.output_file)
    if not picks:
        print("Generating new weekly picks...")
        picks = get_weekly_picks(args.url, args.output_file)
    pipe(picks, get_todays_pick, print_pick)


def parse_args():
    parser = argparse.ArgumentParser(description='Pick a random lunch spot.')
    parser.add_argument('-u', '--user-id', type=str, required=True,
                        help='yelp user id')
    parser.add_argument('-f', '--output-file', type=str,
                        default=os.path.join(os.path.expanduser('~'), '.lunchpicks'),
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
