# smash.gg tools

These are some tools I created to interact with smash.gg tournaments.
Website at: akbiggs.pythonanywhere.com

## Running the website

To run the website locally, you'll need to:

1. Go to [developer.smash.gg](http://developer.smash.gg) and sign up for dev access
   by filling out the form under Authentication (ugh). This should take a day to get
   approved.
2. Once you've received dev access, create a token. Copy that token into a file
   in this folder named `apikey.txt`. The only line in this file should be your
   API token.
3. Get [Python 3](https://www.python.org/downloads/).
4. Create a virtual environment: `python3 -m venv myenv`
5. Activate your virtual environment:
   - On Windows: `myenv\Scripts\activate.bat`
   - On Mac / Unix: `./myenv/Scripts/activate`
6. Install the following libraries:

```
pip install requests
pip install flask
```

7. Set up the `FLASK_APP` environment variable:
  - On Windows: `set FLASK_APP flask_app.py`
  - On Mac / Unix: `export FLASK_APP=flask_app.py`
8. Run the flask app: `flask run`
9. You're good to go, follow flask's instructions to see the website.

## Amateur Bracket Generator

Unfortunately, due to limitations of the smash.gg API, this tool will not actually
create the amateur bracket for you. UGH.

But it will tell you who should be entered into the amateur bracket and how to seed
them based on the original tournament.

To run it:

1. Find your tournament's "slug", i.e. the identifier of the tournament in a URL.
   For example, in the tournament
   [https://smash.gg/tournament/google-tournament-12/events](
   https://smash.gg/tournament/google-tournament-12/events), this would be
   `google-tournament-12`.
2. Run `python3 create_amateur_bracket.py <tournament_slug>`.

Example session:

```
(test) C:\Users\Alex\src\sggtool>python create_amateur_bracket.py google-tournament-12
Here's how I think your amateur bracket should look:

1. TenSpeed
2. Jett The Jenga God
3. Gz
4. Frost
5. Roverto999
6. humz
7. damndaniel
8. CrOS | JZ
9. divadavid
10. seanb
11. jeb

Unfortunately, due to limitations in smash.gg's API,
I can't create this bracket for you right now. :(    
```
