# PWP SPRING 2021
# Material Database
# Group information
* Student 1. Mohammad Bagheri Email: mohammad.bagheri@oulu.fi
* Student 2. Joni Barsk  Email: joni.barsk@outlook.com
* Student 3. Lasse Hyyryläinen Email: lasse.hyyrylainen@student.oulu.fi

# Database setup
## Requirements and Creating Database
This project requires `Flask`, `mongo`,`mongo-tools`,`flask-mongoengine`, `flask-restful`, `requests`,`wheel`,`idna`,`ipython`, `jsonschema` .   
We highly recommend to use a python virtual enviroment for instaling the requirements. to do this you can use this command:
`python3 -m venv mat-env`
then you should activate your virtual enviroment with following command:
`source Install_Dir/mat-env/bin/activate`
All dependencies can be installed using `pip install` command followed by the name of library, or alternatively execute this command in terminal to install all libraries needed:     
`pip install -r requirements.txt`

after installation run the app.py with Flask with this command:
`flask app.py`

for a new container docker desktop:
`$ docker run -d -p 27017:27017 --name mongo mongo:4.2`
`mongodump.exe -d db`
`mongorestore.exe -d db --drop c:{path to repository}\PWP-2021-MJL\tests\mongodump\db`


## Testing Datbase
After setting up database now you can test database, the file app.test.py contains the test cases for database testing. Test cases can be executed by typing python command (assuming that you are at app.test directory).
`python app.test.py`

After executing that command you can check all details in command window about test cases.




