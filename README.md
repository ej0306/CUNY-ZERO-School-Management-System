## Team K
# CUNY Zero

### A Graduate Program Management System
### Installation

    Open GitHub and clone the 'csc322' repository.

    Open the terminal/command prompt and navigate to the repository's path.

    To create a virtual environment, type:
        On Windows: python -m venv environment-name
        On Mac: python3 -m venv environment-name

    To activate the environment, use:
        On Mac: source env_name/bin/activate
        On Windows: env_name\scripts\activate

    Type pip install -r requirements.txt.

    Make migrations by running python manage.py migrate.

    Create a superuser by running python manage.py createsuperuser.

    To start the server, run python manage.py runserver.

    Copy the localhost link (http://127.0.0.1:8000/) and paste it into your browser.

    Go to the Django admin site (http://127.0.0.1:8000/admin). Log in using your superuser credentials and select "Registrar," then "Add Registrar." From the user dropdown, select the appropriate account (it may be displayed as ",") and click the pencil icon next to the dropdown menu. In the pop-up window, scroll down and check the "Is Registrar" box. Optionally, update the first name and last name, then click "Save."

    Click "Save" again in the initial window.

    Navigate to the "Courses" table and click "Sessions." Add a session and name it (e.g., Fall 2021). Set "Is Current Session" to "Yes." Optionally, adjust the period dates.

    Save the session.

    Click "View Site," located in the upper-right corner of the admin site. This link will take you directly to the website's homepage.

### Usage
### Registrar

    Accept/reject applications
    Assign classes to instructors
    Set up classes
    Cancel classes
    Review course evaluations
    Send general warnings to students or instructors
    De-register students
    Suspend students or instructors

### Student

    Register for classes
    Register for special classes
    Write reviews
    Report instructors or students
    Access their own personal page
    Drop classes
    View grades

### Instructor

    Admit students from the waitlist
    Assign grades
    Report students
    Access their own personal page

### Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
