Build:
[![Build Status](https://travis-ci.org/rnjane/Flight-Booking-API.svg?branch=develop)](https://travis-ci.org/rnjane/Flight-Booking-API)

Coverage:
[![Coverage Status](https://coveralls.io/repos/github/rnjane/Flight-Booking-API/badge.svg?branch=develop)](https://coveralls.io/github/rnjane/Flight-Booking-API?branch=develop)

# Flight-Booking-API
A Flight booking application backend API.

# Description

The application has the following features.
1. A user can create and log in to an account.
2. A user can upload passport photographs to their profiles.
3. A user can book ticket(s).
4. A user should receive tickets as an email.
5. A user can check the status of their flight.
6. A user can make flight reservations.
7. A user can purchase ticket(s).
8. A user receives a reminder email a day before their flight is due.

# Documentation
These are the available endpoints.
1. `login/` - User login. Requires Username and password.
2. `register/` - User registration. Requires username, email and password.
3. `remove-passport/` - Delete a Passport of the currently logged in user
4. `update-passport/` - Update Passport of the currently logged in user.
5. `upload-passport/` - Upload a Passport to your profile. You need to be logged in.
6. `flights/` - Check all available flights. Authentication not required.
7. `create-booking/<str:flight_name>/` - Book the specified flight.
8. `bookings/` - Check all your bookings. Needs user to be logged in.
9. `pay/<str:pk>/` - Pay for the specified flight. pk is flight number of the flight you want to pay for.
10. `reserve/<str:pk>/` - Pay for the specified flight. pk is flight number of the flight you want to pay for.
11. `flights-report/` - Check all the booked flights in the last 24 hours.

# Setup Instructions
1. Clone this repository
`git clone https://github.com/rnjane/Flight-Booking-API.git`
2. Create a python virtualenvironment.
`virtualenv -p python3 venv`
3. Activate it.
`source venv/bin/activate`
4. CD into the cloned project folder, and instal project requirements.
`cd Flight-Booking-API`
`pip install -r requirements.txt`
5. Create a .env file and add environment variables in the sampleenv. Add the values appropriately. You only need to update email and password.
6. Add the variables to your environment.
`source .env`
7. Run migrations.
`python manage.py migrate`
7. Seed flights.
`python manage.py loaddata fixtures`
8. Run the application.
`python manage.py runserver`
