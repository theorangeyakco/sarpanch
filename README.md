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

* Get the .env from Param Kapur.
* `pipenv install`
* `pipenv run python manage.py runserver` 

You're good to go!


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
