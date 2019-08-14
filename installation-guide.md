# youtube-crawler

### Installation Guide

##### Preparing environment (Python & Linux)

- Firstly ensure that you've the right version of python installed on your machine by the following command
`sudo apt install python2.7 python-pip`

- Then go to project directory and make python environment executable via this command `python -m virtualenv venv`

- Finally activate your environment by typing `. venv/bin/activate`


##### Configure your app (Flask)

- Ensure again you're in the project root and define your initial file for `Flask`, it falls normally under `flaskr` directory. Just type this command to do so `export FLASK_APP=flaskr`   

- (Optional) If you want to edit and debug in the run time. go and type `export FLASK_DEBUG=1`

- All set. Just launch your app using whether python's `python -m flask run` or flask's `flask run`

##### Configure your database (SQLite)

- This's the simplest part of the installation. All you want here is to run a pre-defined command that will create a database schema containing `videos` table. Type `flask init-db` 