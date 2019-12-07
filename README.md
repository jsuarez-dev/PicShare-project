# Platzigram-project
This repository has the result project of a Django course
by Platzi


### Class 1:
### Class 2:
### Class 3:
### Class 4:
### Class 5:
### Class 6:
### Class 7:
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

### Class 10 and 11

In these classes we work with admin interface that django give to
us to create and modify data objects from the data base. Also we
customize the admin interface to create profiles in an easier way

### Class 12
In this class, we created the Post model and configure the a
static folder to allocate the pictures. Also we created views for
for the post page and use a few images.

### Class 13
In this class, we created the login for our application.

### Class 14 and 15

In this class, we created the logout and sing up for our
application.

### class 16
In this class we study middleware and we created one to redirect
to "update profile" if the profile of the user has't completed.

### class 17
In this class we create the form to update the profile of the
user using django forms.

### Class 18
In this class we create a form from the post model to
create posts and views for each url.

### class 19
In this class, we create a form validation for a the signup form

### Class 20 and 21
In this class, we organize the main urls file in urls file for 
each application. Then we create a new view base in class to check
the user profile. in the twenty first class we fix some bug create
because of the new urls configuration. Then we add the Login Recuaried
in the user detail's view. And at the end I create a detail link for
each post.

### Class 22

In this class, we use CreateView Class to re-write the view of "post/new"
.Then, we use FormView Class to re-write the view of "users/signup".
Then, we use UpdateView Class to re-write the view of "update_profile".
And we create the "pagination.html" to re-use.

### Class 23

In this class we use LoginView and LogoutView class to re-write the views and
improve in general the code. Also add the file to deploy in Google Cloud. 