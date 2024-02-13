import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime
import urllib3

urllib3.disable_warnings()

def load_json(filename):
	with open(filename, 'r', encoding='utf-8') as f:
		return json.load(f)

def load_env_vars():
	load_dotenv()
	return os.getenv("URL"), os.getenv("COOKIE")

def main():
	subjects = load_json('subjects.json')
	rooms = load_json('rooms.json')
	URL, COOKIE = load_env_vars()

	current_day = datetime.now().isoweekday()

	headers = {
		"accept": "application/json, text/plain, */*",
		"accept-language": "en-US,en;q=0.9,he-IL;q=0.8,he;q=0.7",
		"cookie": COOKIE
	}
	data = {
		"institutionCode": 515502,
		"selectedValue": "10|1",
		"typeView": 2
	}

	with requests.Session() as session:
		response = session.post(URL, headers=headers, json=data, verify=False)
		json_data = response.json()

		if 'data' in json_data and isinstance(json_data['data'], list):
			day = json_data['data'][current_day]

			if day.get("dayIndex") <= 5:
				for hour in day.get("hoursData"):
					if 1 <= hour.get("hour") <= 10 and 'scheduale' in hour and len(hour['scheduale']) > 0:
						lesson = hour['scheduale'][0]
						lessonName = lesson.get("subject")
						lessonID = str(lesson.get("studyGroupID"))
						roomID = str(lesson.get("roomID"))

						if lessonID not in subjects or roomID not in rooms:
							continue

						changes = lesson.get("changes")
						if changes and changes[0].get("isClassCancel"):
							print(f"{lessonName} is cancelled")
		else:
			print("'data' field is missing or is not a list")

if __name__ == "__main__":
	main()