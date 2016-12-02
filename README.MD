# Lunch Picker

Lunch group can't decide where to eat? This script will do it for you. Lunch picker uses a
user's bookmarked restaurants to choose. All you have to do is bookmark all your favorite
lunch spots and use your user id to run the script.

It will generate a random pick of restaurants for the week. The reason that it does generates for the whole week is to get some randomness without replacement. If you want one random pick from all your restaurants, there is an option for that.

## Finding Yelp userid

Navigate to your bookmarks page. In the url, you should see a keyword argument 'userid'.
Copy that. It will look something like:

`https://www.yelp.com/user_details_bookmarks?cc=US&userid=009ifonFOOBARojds=-2ei`

## Running the script

This script was written and only ran with python 3 though should run with python 2. It requires the `requests` and `beautifulsoup4` packages installed in the environment.

Run:

`python lunchpick.py -u USER_ID`

If your user id starts with a dash, you must call it with `-u='-USERinoinseFO23-fc'`.

Also, you can get one random pick by adding the `--one` option:

`python lunchpick.py -u USER_ID --one`

```
usage: lunchpick.py [-h] -u USER_ID [-f OUTPUT_FILE] [--one]

Pick a random lunch spot.

optional arguments:
  -h, --help            show this help message and exit
  -u USER_ID, --user_id USER_ID
                        yelp user id
  -f OUTPUT_FILE, --output-file OUTPUT_FILE
                        output file containing weekly picks
  --one                 random pick from all choices
```
