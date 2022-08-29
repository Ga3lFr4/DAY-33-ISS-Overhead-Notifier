import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 48.835733 # Your latitude
MY_LONG = 2.324716 # Your longitude

MY_EMAIL = "jndjrdn12345@gmail.com"
MY_PASSWORD = ""

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude =  float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.

def is_iss_close():
    lat_close = MY_LAT-5 <= iss_latitude <= MY_LAT+5
    long_close = MY_LONG-5 <= iss_longitude <= MY_LONG+5
    return lat_close and long_close

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response_time = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response_time.raise_for_status()
    data_time = response.json()
    sunrise = int(data_time["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data_time["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now()
    now_hour = time_now.hour
    return now_hour <= sunrise or now_hour >= sunset


# If the ISS is close to my current position
while True:
    time.sleep(60)
    if is_iss_close():
        # and it is currently dark
        if is_night():
            # Then send me an email to tell me to look up.
            with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                connection.sendmail(to_addrs="gael.francoise@gmail.com", from_addr=MY_EMAIL,
                                    msg="Subject:Look Up !\n\nISS might be visible overhead!")
# BONUS: run the code every 60 seconds.



