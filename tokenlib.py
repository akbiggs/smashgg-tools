def read_token(filename="apikey"):
	with open("apikey.txt") as f:
		if not f:
			print("API key not setup. Put it in apikey.txt.")
			return None

		return f.readline().strip()