# F4MP Cloud Service (in development)

CloudService is a Python DRF for enabling services like a central authentication/identity service for the F4MP mod.

## Running locally

First install a tool for creating virtual python enviorments e.g https://pypi.org/project/virtualenv/

 1. Download the code
 2. Setup the virtual env ```virtualenv venv```
 3. Install the required packages ```pip install -r requirements.txt```
 4. Run database migrations ```python manage.py migrate```
 5. Collect static files ```python manage.py collectstatic```
 6. You need to register an API key here: https://steamcommunity.com/dev/apikey
 7. Rename ```example.env``` to ```.env``` and edit the values
	 a. ```DATABASE_URL=sqlite:///db.sqlite3```
	 b. ```SECRET_KEY=<replace with secure random string>```
	 c. ```STEAM_KEY=<replace with steam key provided in step 5>```
	 d. ```ADMIN_PATH=<replace with a random string>```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please made sure any changes or additions have adequate test coverage.

Tests can be run by simply running ```python manage.py test```