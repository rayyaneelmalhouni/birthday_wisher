
from datetime import datetime
from smtplib import SMTP
from random import randint
import pandas as pd
import os

# Email
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")

# Get the current time
current_time = datetime.now().strftime("%d/%m/%Y")

# Get the People on the Birthdays file
birthdays_df = pd.read_csv("birthdays.csv")
birthdays_dict = birthdays_df.to_dict(orient="records")


# Filter them to get who are celebrated today
people_to_celebrate = []
for person in birthdays_dict:
    if person["Date"] == current_time:
        people_to_celebrate.append(person)


# Send a celebration message
for person in people_to_celebrate:
    with open(f"./letter_templates/letter_{randint(1, 3)}.txt", "r") as file:
        letter = file.read().replace("[NAME]", person["Name"])
    with SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=person["Email"],
            msg=f"Subject:Happy Birthday!\n\n{letter}"
        )

