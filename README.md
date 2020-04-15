1) Activate running enviroment:
    a) Install virtualenv by running 'pip install virtualenv'. You should run it only once
    b) run 'virtualenv venv'
    c) run 'source venv/bin/activate'
    d) at any time you can run 'deactivate' to deactivate the enviroment

2) Install requirements:
    run 'pip -r requirements.txt'

3) make sure mysql is install, user is created, and privilerges are granted
   As an example you can run the following:
    1) mysql -uroot
    2) CREATE USER 'genshopuser'@'localhost' IDENTIFIED BY 'GenShop_123';
    3) GRANT ALL PRIVILEGES ON * . * TO 'genshopuser'@'localhost';
    4) login as a created user: mysql -u genshopuser -p
    5) CREATE DATABASE dbname;

To run application:
python3 -m run -config=configs/config.yaml
