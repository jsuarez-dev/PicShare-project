# Platzigram-project
This repository has the result project of a Django course by Platzi


### class 1:
### class 2:
### class 3:
### class 4:
### class 5:
### class 6:
### class 7:
In this class we add a new field "is_admin" and I modify the field 
"birthdate" to "birth_date" to see how Django does these.
Then we use the Django Shell to add a object in to de data base. 
To open the shell we use `python manage.py shell`, this shell has 
all the Django app upload by default.

Notes:
- The **ORM** model by default add a ID column.
- When you add a new column and the table has data you should add default value or 

### Class 8:

In this class we use the User model that come with Django, and we
create super user with `python manage.py createsuperuser` and also
we delete the model user that we create tu use the user model that
django give to us.

### Class 9:

In this class we create new app named _users_ and in this app we
define a new model named Profile which is created with a proxy 
(like copy) from the user default model.