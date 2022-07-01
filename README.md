![PicShare App](https://github.com/jadry92/PicShare-project/workflows/PicShare%20App/badge.svg)

# PicShare Project

This repository has the result project of a [Django](https://platzi.com/clases/django/) course by Platzi.

This Web Application allow user registers to watch, upload, comment and share pictures with friends

To use this web project. You must have:

- Python 3

To install I recommend to create a virtual environment.
Installation process :

```shell script
virtualenv .env
source .env/bin/activate
pip install -r requirements.txt
```

To create teh database:

```shell script
python manage.py makemigrations
python manage.py migrate
```

To run the serve:

```shell script
python manage.py runserver
```
