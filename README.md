# Django-School-Management
A fullstack school management project in django, bootstrap-4 and javascript.

# Installation:
1. go to the project folder
2. run `pipenv install`
3. create `.env` under config folder and give credentials following `.env.example` template
3.1. See additional resources section to setup/get more info.
4. run `python manage.py migrate`
5. then `python manage.py runserver`
for testing, create a superuser too.

# Celery-redis setup:
1. Celery is installed, install redis as well. <br>
2. for linux users: 
- run redis server with `redis-server` command.
3. for windows users:
- Download redis (https://github.com/microsoftarchive/redis/releases/tag/win-3.0.504)
- Run redis-server.exe and redis-cli.exe.

And finally, while django server is running, run this command on another terminal <br>
`celery -A config worker -l INFO`

# Additional Resources:
+ Create braintree sandbox account from: https://sandbox.braintreegateway.com/login

# Usage/testing
Use provided [fixtures](https://docs.djangoproject.com/en/3.1/howto/initial-data/) for each applications. <br>
*Provided Fixtures:*
- teachers/teacher_fixtures.json
*How to load fixtures?* <br>
*For example, you want to load `teachers/teacher_fixtures.json` <br>
you have to simply run this management command on your terminal:*
`python manage.py loaddata teachers/teacher_fixtures.json`
<br>
this command will load initial data for teachers app.
Follow the same pattern to install initial data for other applications.

* APPLY CARD INFO AT `admission` link
`card number: 5555555555554444`
`expiracy: any valid future date` 

# Working Components:
* Create application for admission manually (it will save candidate as offline admission candidate)
* Online application for admission (payment and admission process handled automatically)
* Handle payment, admission, rejection, update candidate's status after communication
* Assign student to an academic batch, class
* Manage counseling (admission) dashboard with data visualization (download/view pdf reports)
* CRUD departments, subjects, teachers, academic session, semester; import subjects from csv file
* Teacher list view, students list view, designation CRUD
* Create users, users list, view user groups and permissions


<br>

# Contact me:
- [Facebook](https://www.facebook.com/tareqmonwer1/)
- [Linkedin](linkedin.com/in/tareqmonwer)
- [Twitter](https://twitter.com/TareqMonwerDPI)
- [Github](https://github.com/TareqMonwer)
- [Website](www.tareqmonwer.com)
- email: tareqmonwer137@gmail.com