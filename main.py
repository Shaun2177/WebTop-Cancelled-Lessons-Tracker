import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime
import urllib3

urllib3.disable_warnings()

# Load the subjects from the JSON file
with open('subjects.json', 'r', encoding='utf-8') as f:
    subjects = json.load(f)

# Load the rooms from the JSON file
with open('rooms.json', 'r', encoding='utf-8') as f:
	rooms = json.load(f)

# Get the current day as an integer (Sunday = 0)
current_day = datetime.now().isoweekday()

# Load environment variables and dotenv
load_dotenv()

URL = os.getenv("URL")
COOKIE = os.getenv("COOKIE")

headers = {
	"accept": "application/json, text/plain, */*",
	"accept-language": "en-US,en;q=0.9,he-IL;q=0.8,he;q=0.7",
	"content-type": "application/json",
	"cookie": COOKIE
}
data = {
	"institutionCode": 515502,
	"selectedValue": "10|1",
	"typeView": 2
}

# Send POST request to get the schedule
response = requests.post(URL, headers=headers, data=json.dumps(data), verify=False)
json_data = response.json()

# If data (days) exists and is a list
if 'data' in json_data and isinstance(json_data['data'], list):

	days = json_data['data']
	day = days[current_day]

	# If day is Sunday to Thursday
	if day.get("dayIndex") <= 5:

		# Iterate over the hours
		for hour in day.get("hoursData"):	

			# If hour of lesson is 1 to 10
			if hour.get("hour") >= 1 and hour.get("hour") <= 10:

				if hour.get("scheduale"):
					
					lesson = hour.get("scheduale")[0]
					lessonName = lesson.get("subject")
					lessonID = str(lesson.get("studyGroupID"))

					roomID = str(lesson.get("roomID"))

					# If not a valid lesson
					if lessonID not in subjects:
						continue

					if roomID not in rooms:
						continue

					# If there's changes to the lesson
					changes = lesson.get("changes")
					if changes:
						changes = changes[0]
						if changes.get("isClassCancel") is True:
							print(f"{lessonName} is cancelled")
						
else:
	print("'data' field is missing or is not a list")