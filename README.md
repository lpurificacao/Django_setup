
<img align="right" src="python_django_logo/python_django_logo.webp">

${\huge{\textsf{\textcolor{#0A1589}{This is my Django starter}}}}$

I created this project generator script to automate the setting up a of new Django project.

${\large{\textsf{\textcolor{#0A1589}{How to use it?}}}}$

Just copy the script `django_starter.py` to the directory where you want to create your django project.

Run it from your shell or IDE. You will be prompted to name your project and app.

That's it.

${\large{\textsf{\textcolor{#0A1589}{What does it do?}}}}$

It creates the virtual environment in the current folder, project structure, files and configuration for your project.

It upgrades pip, installs Django and any other dependencies you want and migrates the database.

${\large{\textit{\textcolor{#0A1589}{I have my own way of structuring the folders... Can I customize it?}}}}$

Yes. Right at the beginning of the script you'll find 2 tuples: ${\textbf{\textsf{\textcolor{ProcessBlue}{'project\\_folders'}}}}$ and ${\textbf{\textsf{\textcolor{ProcessBlue}{'app\\_folders'}}}}$

A single string represents a directory.

A tuple of strings means a parent directory, a child directory, so on and so forth.

There is also a ${\textbf{\textsf{\textcolor{ProcessBlue}{'dependencies'}}}}$ dictionary. This is where you instruct it to install any libraries.

