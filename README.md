Simple Polygon Triangulation
<br>

# Project Installation Guide for Windows

## Prerequisites

Before you begin, ensure that the following software is installed on your system:

- **Python** (Version 3.8 or higher): [Download Python](https://www.python.org/downloads/)
- **pip** (Python package manager): Comes with Python installation
- **Git** (For cloning the repository): [Download Git](https://git-scm.com/downloads)

## Step-by-Step Installation

### 1. Clone the Repository

Open Command Prompt (or your preferred terminal) and run:

```bash
git clone https://github.com/harisUOL/MScProject.git

Navigate to the cloned project directory:

cd MScProject

2. Set Up a Virtual Environment

Create a virtual environment to isolate dependencies:

python -m venv venv

Activate the virtual environment:

venv\Scripts\activate.bat

3. Install Dependencies

Install all the required dependencies from the requirements.txt file:

pip install -r requirements.txt

4. Create a New Django Project

Since the project was initially developed on Linux, you need to create a new Django project on Windows.

Run the following command to create a new Django project named mysite in the same directory as the cloned project:

django-admin startproject mysite .

5. Copy the polytria App

Now, copy the polytria app from the cloned project to your newly created mysite project:

1. Navigate to the cloned directory and locate the polytria app folder.


2. Copy the entire polytria folder into the ./mysite directory (inside the mysite project folder you just created).



6. Configure settings.py

In your new Django project (mysite), open the settings.py file (located in ./mysite/mysite/settings.py) and make the following changes:

Add 'polytria' to the INSTALLED_APPS list:



INSTALLED_APPS = [
    # Other apps
    'polytria',
]


7. Make Migrations and Update apps.py

Run the following commands to apply the migrations:

python manage.py makemigrations
python manage.py migrate

Additionally, ensure that the apps.py file in the polytria app is correctly set up to match your project structure. Verify that the PolytriaConfig class is properly configured.

8. Run the Development Server

Once everything is set up, run the Django development server:

python manage.py runserver

Now, open your browser and go to http://127.0.0.1:8000/ to view the app.

Troubleshooting

Virtual Environment Activation Issues: If you're having trouble activating the virtual environment in PowerShell, you may need to modify the execution policy:


Set-ExecutionPolicy Unrestricted -Scope Process

Migration Issues: If you run into migration issues, try running:


python manage.py makemigrations
python manage.py migrate

