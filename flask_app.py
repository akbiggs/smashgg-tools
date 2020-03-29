from flask import Flask
from flask import render_template

import amateurlib
import tokenlib

app = Flask(__name__)

def parse_tournament_slug(tournament_url):
	"""Parses the "slug" (URL ID) of a tournament URL."""
	parts = tournament_url.split('smash.gg/tournament/')
	if len(parts) == 2:
		# The next section of the URL is the slug.
		return parts[1].split('/')[0]
	else:
		# If there are no slashes in the URL, assume the
		# slug was passed directly.
		maybe_slug = parts[0]
		if '/' not in maybe_slug:
			return maybe_slug
		return None

@app.route('/')
def hello_world():
	return render_template("index.html")

@app.route('/amateur', methods=["POST"])
def create_amateur_bracket():
	from flask import request

	token = tokenlib.read_token()

	tournament_url = request.form['tournament-url']
	tournament_slug = parse_tournament_slug(
		tournament_url)
	amateurs = amateurlib.fetch_seed_sorted_amateurs(
		tournament_slug, token)
	print(amateurs)

	return render_template(
		"amateur.html", amateurs=amateurs)