[![license](https://img.shields.io/github/license/btactic/bPortal.svg?style=flat-square)](LICENSE)
[![bPortal documentation](https://img.shields.io/badge/docs-passing-brightgreen.svg?style=flat-square)](https://github.com/btactic/bPortal/tree/master/docs)
[![GitHub (pre-)release](https://img.shields.io/github/release/btactic/bPortal/all.svg?style=flat-square)](https://github.com/btactic/bPortal/releases/latest)


# bPortal
bPortal is a SuiteCRM portal written using django project.

## Clone the repository
To clone the repository and all submodules simply run:
```
git clone --recursive https://github.com/btactic/bPortal.git
```
## Getting the development environment ready
In this section is described how to get the development environment ready on Debian based systems.

It's recommended to use `virtualenv` and `pip` packages. You can install this two dependencies runnig:
```
sudo apt update
sudo apt install virtualenv python3-pip
```

Once you have `virtualenv` and `pip` tools ready it's time to prepare the virtual environment to run the application.  
Following we create a virtual environment and install all Python dependencies:
```
cd bPortal
virtualenv env
source env/bin/activate
pip install -r requirements.txt
pip install -r suitepy/requirements.txt
```
The `virtualenv env` command could show an error because the versions of `distlib` and `virtualenv` are incompatible, to correct this:
```
pip uninstall distlib
pip install distlib==0.3.6
```

### Configuring SuiteCRM server
We need to edit `suitepy/suitepy.ini` file, in order to do it:

```ini
[SuiteCRM v4_1 API Credentials]
url = https://crm.example.org/custom/service/suitepy/rest.php
username = User_username
password = User_password
application_name = SuitePY
verify_ssl = True
```

Our development environment it's ready. Now we can create an admin account with:

### Setup Database type

#### Option 1: SQLITE
By default, without doing nothing, it uses an SQLITE database.
#### Option 2: MySQL

The following dependences are needed by the portal app to connect to the MySQL database. You can install the dependences with:

```
sudo apt install default-libmysqlclient-dev python3-dev
pip install mysqlclient
```
If mysql_config.cnf config file does not exist then create it with:

```
cp mysql_config.cnf.sample mysql_config.cnf
```

After, edit mysql_config.cnf with your MySQL connection settings.


### Initial setup

Every time suitepy.ini changes run this command and reload apache if you do not see changes.

```
python3 manage.py migrate
```

### Superuser creation

```
python3 manage.py createsuperuser
```

### Quit development environment

To deactivate our Python virtual environment simply run:
```
deactivate
```



## How to run the application using development environment
First of all we have to activate our virtual environment.  
Enter to root directory of the application (normally `bPortal`) and run:
```
source env/bin/activate
```

Now we can start `bPortal` on development mode running:
```
python3 manage.py runserver 0.0.0.0:8080
```

Once we have run the previous command, the application is listening on `http://localhost:8080`.

To stop the application press `CTRL-C` and run the command `deactivate` to deactivate the Python virtual environment.

## Installation on virtualmin

You can check [docs/installation_on_virtualmin.md](docs/installation_on_virtualmin.md) which explains how to install and configure bPortal on a Virtualmin server.
