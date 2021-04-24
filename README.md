# PWP SPRING 2021
# Material Database
# Group information
* Student 1. Mohammad Bagheri Email: mohammad.bagheri@oulu.fi
* Student 2. Joni Barsk  Email: joni.barsk@outlook.com
* Student 3. Lasse Hyyryläinen Email: lasse.hyyrylainen@student.oulu.fi

# Database setup
## Requirements and Creating Database
This project requires `Flask`, `mongo`,`mongo-tools`,`flask-mongoengine`, `flask-restful`, `requests`,`wheel`,`idna`,`ipython`, `jsonschema`, `coverage` . 

We highly recommend to use a python virtual enviroment for instaling the requirements. to do this you can use this command:

`python3 -m venv mat-env`
then you should activate your virtual enviroment with following command:

`source Install_Dir/mat-env/bin/activate`
All dependencies can be installed using `pip install` command followed by the name of library, or alternatively execute this command in terminal to install all libraries needed: 

`pip install -r requirements.txt`

after installation run the app.py with Flask with this command:

`flask app.py`

for a new container install docker desktop:
https://www.docker.com/products/docker-desktop
Then create a new mongo container. 

`$ docker run -d -p 27017:27017 --name mongo mongo:4.2`

After your mongo container runs correctly
Initialize the database for testing and usage:
`python populatedb.py`


## Testing Datbase
After setting up database now you can test database, the file app.test.py contains the test cases for database testing. Test cases can be executed by typing python command

if you have used database before tests, reset the data to run tests successfully

`python populatedb.py`

Then run the tests

`coverage run -m unittest discover -v`

After running tests you can create report from them
on terminal
`coverage report`
or by html report
`coverage html`





