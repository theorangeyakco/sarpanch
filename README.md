# sarpanch

This repository contains the code for the Sarpanch API hosted at: `api.sarpanch.org` and the 
promotional website is hosted at `sarpanch.org`. The API is built using the Django Rest 
Framework deployed on Heroku and the promo webiste is built in Vue and deployed using 
Netlify. 

## API Documentation:
https://documenter.getpostman.com/view/11883658/TVzNJzGo

## Promo webiste instuctions: 
The code for the promo website is is `/landing`. `/landing/README.md` has more information. 

## API Build instructions: 

The dependencies are managed by Pipenv. To activate the 
virtual environment do the following: 

1. `pip install pipenv`
2. `pipenv install --dev`
3. `pipenv shell`

At this point you will need the `.env` file to get the app to run. To get this
file please contact Param at param@theorangeyak.co for further instructions. Or
if you have permission, you will be able to find all the credentials for this
project in the Orange Yak Google Drive folder. Look at: 
    `theorangeyakco/<active_projects|archived_projects>/
    sarpanch/notes/credentials.gsheet`.

You will also find the environment variables there.

Now you will need other pre-requisites:
1. `postgresSQL`
    * Please set it up on your machine and create a local database to connect to. Put
    this localhost URL in the `DATABASE_URL` environment variable.
2. `redis`
    * Not currently required.
    
Finally, you can run the app with:
`python manage.py runserver`

Which will start a server at `localhost:8000`.



## Notes
#### User Authentication Classes on an APIView
```python
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication

class SomeView(APIView):
    # ...
    permission_classes =  (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    # ...
```
