# Lunch Picker

Lunch group can't decide where to eat? This script will do it for you. Lunch picker uses a
user's bookmarked restaurants to choose. All you have to do is bookmark all your favorite
lunch spots and use your user id to run the script.

## Finding Yelp userid

Navigate to your bookmarks page. In the url, you should see a keyword argument 'userid'.
Copy that. It will look something like:

`https://www.yelp.com/user_details_bookmarks?cc=US&userid=009ifonFOOBARojds=-2ei`

## Running the script

This script was written and only ran with python 3 though should run with python 2. It requires the `requests` and `beautifulsoup4` packages installed in the environment.

Run:

`python lunchpick.py`

and enter the user id at the prompt.
