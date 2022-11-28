# Bright Money Task

## Problem Statement
1. User signup, login , logout APIs. 
2. Token exchange API : An authenticated user can submit a plaid public token that he gets post link integration.
    * This public token is exchanged for access token on the backend.
    * This initiates an async job on the backend for fetching account and item metadata for the access token.
3. Expose a webhook for handling plaid transaction updates and fetch the transactions on receival of a webhook.
4. Expose an api endpoint for fetching all transaction and account data each for a user.
5. Do appropriate plaid error handling

## Project Explanation Video

[![Bright Money](https://user-images.githubusercontent.com/55273506/204193048-250ad671-9e94-4f53-af51-08a5ec74caa0.png)](https://www.youtube.com/watch?v=2YNCi_oUNCw)


</br>

## Frontend Setup
1. Clone the repo.
2. Move to the frontend directory.

        cd frontend
    
3. Run `npm install` to install all the dependencies.
    
        npm install

4. Start development server

        npm run dev
    

</br>

## Backend Setup
1. Clone the repo.
2. Move to the backend directory.

        cd projectBrightMoney

3. Create virtual environment and activate it.

        python3 -m venv env
        source env/bin/activate

4. Install the dependencies.

        pip install -r requirements.txt

5. Create a `.env` file in the root directory and add the following environment variables.

        djangoSecret="django-insecure-fk2xh0!q#tp((-u&ca-s_5)yi18#j1z%v99q(kmib3pvh2j$lo"
        plaidClientId="6380bf3279176400131389fd"
        plaidSecret="c29f73e180f92ba4cf0e8935b53b87"

6. Run the migrations.
    
        python manage.py makemigrations
        python manage.py migrate

7. Create Superuser to see the django admin panel
    
            python manage.py createsuperuser

8. Run the Django server.
        
            python manage.py runserver

9. By default your server will start on `http://127.0.0.1:8000/` and the admin panel will be available at `http://127.0.0.1:8000/admin/` login with the superuser credentials to see the dashboard.

10. Install and start redis server on port 6360 on a new terminal. Redis will act as a message broker between celery and django application.

        sudo apt install redis-server
        redis-server -6360
        
11. Start celery worker on a new terminal.
    
        python -m celery -A projectBrightMoney worker -l info

12. Now you can start using the APIs on frontend or [postman collection](./Bright%20Money.postman_collection.json).

</br>

### Postman Collection -> [Bright Money.postman_collection.json](./Bright%20Money.postman_collection.json)


</br>

## Challenges Faced
1. Integarting OAuth with plaid.
2. Handling plaid and django errors.
3. Integrating celery with django.
4. Integrating APIs with frontend.
5. Handling access and refresh tokens.

## Things to Improve
1. Add tests.
2. Add more error handling.
3. Writing cleaner code.
4. Logging.

## Things learned
1. Integrating OAuth with plaid.
2. How Celery works
3. How to use Redis as a message broker.
4. Dealing with access and refresh tokens on frontend.
5. Webhooks.
6. Exposing localhost to internet throught ngrok.