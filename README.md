1) Activate running enviroment:
    a) Install virtualenv by running 'pip install virtualenv'. You should run it only once
    b) execute 'virtualenv venv'
    c) execute 'source venv/bin/activate' or on Windows 'venv\Scripts\activate'
    d) at any time you can run 'deactivate' to deactivate the enviroment

2) Install requirements:
    execute 'pip -r install requirements.txt' or 'pip install -r requirements.txt' for Windows

3) make sure mysql is install, user is created, and privilerges are granted
   As an example you can run the following:
    1) mysql -uroot, mysql -u root -p for Windows
    2) CREATE USER 'genshopuser'@'localhost' IDENTIFIED BY 'GenShop_123';
    3) GRANT ALL PRIVILEGES ON * . * TO 'genshopuser'@'localhost';
    4) exit as root user with '\q'
    5) login as a created user: mysql -u genshopuser -p
    6) CREATE DATABASE dbname;

4) Open configs/config.yaml and add valid path to log file to path_to_log_file param

To run application:
python3 -m run -config=configs/config.yaml
