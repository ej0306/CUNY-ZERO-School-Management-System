# Team K
# CUNY Zero  

A graduate program management system

## Installation

1. Open github and clone 'csc322' repository

2. Open terminal/command prompt and go to the path of the repository

3. Type 'pyhton -m venv 'environment name' on the cmd for WINDOWS
 	'python3 -m venv 'environment name' on the terminal for MAC

4. Activate environment by using 'source env_name/bin/activate for MAC
				 'env_name\scripts\activate for WINDOWS

5. Type 'pip install -r requirements.txt

6. Make migrations by using 'python manage.py migrate'

7. After migration, createsuperuser 'python manage.py createsuperuser'

8. After creating super user, run 'python manage.py runserver'

9. Copy localhost link like 'http://127.0.0.1:8000/' and paste it to your browser.

10. Go to Django admin 'http://127.0.0.1:8000/admin', login using your superuser account
 	and select "Registrar", then add registrar,  select the account and click
	the pencil next to the dropdown menu.
	Scroll down the new window and check the box "is registrar" and mark it true
	(optional) can change name and last name.

11. Click Save

12. Go to "Courses" table and click "sessions", add session and give session a name
	Example: Fall 2021
	select "is current session" to yes
	(optional) change the dates of the periods.
	
13. Save the session


14. Click view site which is located on the upper right corner of the admin site
	the link will go directly to the homepage of the website.

#Usage

Registrar: 
	Accept/reject applications
	Assign classes to instructors
	set up classes
	Cancel class
	Review reviews 
	Send warning (general) to students or Instructors
	De-register students
	Suspend students/instructors

Student:
	Register for classes
	Register for classes (special registration)
	Write reviews
	Report instructors/students
	Has their own page (can see own info)
	Drop classes
	See grades

Instructor:
	Let in students in wait list
	Assign grades
	Report students
	Has their own page
	

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.