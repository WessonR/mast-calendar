import os
import requests
from ics import Calendar, Event
import hashlib
from datetime import datetime


LICENSE_KEY = os.environ["MAST_LICENSE_KEY"]


response = requests.get(
    "https://www.mast.today/api/v1/status",
    headers={
        "x-mast-license-key": LICENSE_KEY
    },
    params={
        "countryCode": "US",
        "stateCode": "MO"
    }
)


data = response.json()


calendar = Calendar()


for item in data["calendar"]["events"]:

    event = Event()

    # Event title
    event.name = item["title"]


    # Convert MAST date format into calendar dates
    start = datetime.fromisoformat(
        item["effectiveFrom"].replace("Z", "+00:00")
    )

    end = datetime.fromisoformat(
        item["effectiveUntil"].replace("Z", "+00:00")
    )


    event.begin = start
    event.end = end


    # Create a permanent ID
    uid_text = (
        item["title"]
        + item["effectiveFrom"]
        + item["effectiveUntil"]
    )

    event.uid = hashlib.sha256(
        uid_text.encode()
    ).hexdigest()


    # Add extra information to the calendar entry
    event.description = (
        f"Authority: {item.get('authority', '')}\n"
        f"Reason: {item.get('reason', '')}\n"
        f"Source: {item.get('source', '')}"
    )


    calendar.events.add(event)



with open("mast.ics", "w") as f:
    f.writelines(calendar)