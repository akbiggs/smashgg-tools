import requests
import sys

import tokenlib

# 12: 452940, https://smash.gg/tournament/google-tournament-12/event/singles/brackets/759972/1226109/
# 11: 437320, https://smash.gg/tournament/google-tournament-11/event/singles/brackets/733771/1181079/
# 10: 420846, https://smash.gg/tournament/google-tournament-10/event/singles/brackets/704764/1142226/
# 9: 396238, https://smash.gg/tournament/google-tournament-9/event/ultimate-singles/brackets/661226/1082336/
# 8: 386420, https://smash.gg/tournament/google-tournament-8/event/ultimate-singles/brackets/643956/1057682/

SMASHGG_API_URL = "https://api.smash.gg/gql/alpha"

TOURNAMENT_QUERY = """query TournamentQuery($slug: String!) {
	tournament(slug: $slug) {
  	  id
      name
      events {
        id
        name
      }
    }
}"""

EVENT_QUERY = """query EventQuery($id: ID!, $roundNumber: Int) {
  event(id: $id) {
    id
    name
    sets(filters: {
      roundNumber: $roundNumber,
    }) {
      nodes {
        round
        winnerId

        slots {
          entrant {
            id
            name
            seeds {
              seedNum
            }
          }
        }
      }
    }
  }
}"""

def fetch_singles_event_id(tournament_slug, token):
	"""Fetches the singles event inside of a given tourney.

	Args:
		tournament_slug: The identifier of the tourney in a URL.
		token: The smash.gg API token to authenticate the request.
	"""
	request = {
		"query": TOURNAMENT_QUERY,
		"variables": {
			"slug": tournament_slug
		}
	}
	response = requests.post(
		SMASHGG_API_URL,
		json = request,
		headers = {
		  "Authorization": "Bearer " + token
		})

	json = response.json()
	print('TOURNAMENT RESPONSE: ' + str(json))
	if not json or not json.get('data'):
		raise Exception("Failed to fetch data: " + str(json))

	events = json['data']['tournament']['events']
	singles_events = [
		e for e in events
		if "Singles" in e['name']]
	if not singles_events:
		print("Could not find a 'Singles' event in the tournament.")
		print("Make sure the name of your singles event is 'Singles'.")
		return None

	return singles_events[0]['id']

def fetch_round_sets(round_number, event_id, token):
	"""Fetches the sets from the round with the given round_number."""
	request = {
		"query": EVENT_QUERY,
		"variables": {
		  "id": event_id,
		  "roundNumber": round_number,
		}
	}
	response = requests.post(
		SMASHGG_API_URL,
		json = request,
		headers = {
		  "Authorization": "Bearer " + token
		})
	
	json = response.json()
	print('EVENTS RESPONSE: ' + str(json))
	if not json or not json.get('data'):
		raise Exception("Failed to fetch data: " + str(json))

	sets = json['data']['event']['sets']['nodes']
	return sets

def fetch_amateur_deciding_sets(event_id, token):
	"""Fetches the sets that are necessary to decide the amateur bracket.

	Args:
		event_id: The event to fetch sets from.
		token: The smash.gg API authorization token. 
	"""

	# Because I don't understand how loser round numbers are
	# chosen yet, let's fetch from -1 downwards until we find
	# the first loser round (up until a threshold to avoid going
	# nuts).
	THRESHOLD = -10
	relevant_sets = []
	handled_first_round = False
	for round in range(-1, THRESHOLD, -1):
		sets = fetch_round_sets(round, event_id, token)
		if sets:
			relevant_sets += sets
			if not handled_first_round:
				handled_first_round = True
			else:
				# We only care about two rounds of
				# results. Stop here.
				break

	return relevant_sets

def get_loser(set):
	"""Gets the loser from a given set."""
	winner_id = set['winnerId']
	slots = set['slots']
	loser_slots = [
		s for s in slots
		if s['entrant']['id'] != winner_id]

	# In Smash, there are only two entrants in a set:
	# the winner and the loser.
	return loser_slots[0]['entrant']

def get_seed(entrant):
	"""Gets an entrant's seed."""
	return entrant['seeds'][0]['seedNum']

def fetch_seed_sorted_amateurs(tournament_slug, token):
	"""Gets the amateurs, sorted by seed, from a tournament."""
	singles_event_id = fetch_singles_event_id(
		tournament_slug, token)
	amateur_sets = fetch_amateur_deciding_sets(
		singles_event_id, token)
	amateurs = [get_loser(s) for s in amateur_sets]
	return sorted(amateurs, key=get_seed)