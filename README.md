[![license](https://img.shields.io/github/license/btactic/bPortal.svg?style=flat-square)](LICENSE)
[![bPortal documentation](https://img.shields.io/badge/docs-passing-brightgreen.svg?style=flat-square)](https://github.com/btactic/bPortal/tree/master/docs)
[![GitHub (pre-)release](https://img.shields.io/github/release/btactic/bPortal/all.svg?style=flat-square)](https://github.com/btactic/bPortal/releases/latest)

# bPortal
bPortal is a SuiteCRM portal written using the Django framework.

## Clone the repository
To clone the repository and all submodules, run:
```
git clone --recursive https://github.com/btactic/bPortal.git
```
## Getting the development environment ready
This section describes how to set up the development environment on Debian-based systems.

It is recommended to use the `virtualenv` and `pip` packages. You can install these dependencies by running:
```
sudo apt update
sudo apt install virtualenv python3-pip
```

Once you have `virtualenv` and `pip` ready, prepare the virtual environment to run the application. The following steps will create a virtual environment and install all Python dependencies:
```
cd bPortal
virtualenv env
source env/bin/activate
pip install -r requirements.txt
pip install -r suitepy/requirements.txt
pip install -r dolibarrpy/requirements.txt
```

### Configuring SuiteCRM server
Edit the `suitepy/suitepy.ini` file as follows:

```ini
[SuiteCRM API Credentials]
url = https://crm.example.org
client_id = your_client_id
client_secret = your_client_secret
application_name = SuitePY
suitecrmversion = 7
verify_ssl = True
```

Set the `suitecrmversion` parameter to **7** or **8**, depending on your SuiteCRM version.

### Configuring Dolibarr instance
Edit the `dolibarrpy/dolibarrpy.ini` file as follows:

```ini
[Dolibarr API Credentials]
url = https://dolibarr.example.net/api/index.php/
api_token = your_api_token
application_name = DolibarrPY
verify_ssl = True
```

### Setting up the database

#### Option 1: SQLITE
By default, the application uses an SQLITE database.
#### Option 2: MySQL
To connect to a MySQL database, install the following dependencies:
```
sudo apt install default-libmysqlclient-dev python3-dev
pip install mysqlclient
```

If the `mysql_config.cnf` file does not exist, create it with:
```
cp mysql_config.cnf.sample mysql_config.cnf
```

Then, edit `mysql_config.cnf` with your MySQL connection settings.

### Initial setup
After modifying `suitepy.ini`, run the following command and reload Apache if you do not see changes:
```
python3 manage.py migrate
```

### Creating a superuser
Run the following command to create a superuser:
```
python3 manage.py createsuperuser
```

### Exiting the development environment
To deactivate the Python virtual environment, run:
```
deactivate
```

### Logging configuration
By default, **bPortal** generates log files to record errors and other relevant events. These log files are retained for seven days, after which the oldest log file is overwritten.

To customize the logging configuration, refer to [docs/logging_setup.md](docs/logging_setup.md) for detailed instructions on modifying log retention policies, file paths, logging levels, and more.

### PWA Configuration
To modify the default PWA settings, check [docs/pwa_setup.md](docs/pwa_setup.md).

## Running the application in the development environment
First, ensure your virtual environment is set up. Then, activate it by navigating to the root directory of the application (usually `bPortal`) and running:
```
source env/bin/activate
```

Start `bPortal` in development mode by running:
```
python3 manage.py runserver 0.0.0.0:8080
```

The application will be accessible at `http://localhost:8080`.

To stop the application, press `CTRL-C` and run `deactivate` to deactivate the Python virtual environment.

## Installation on Virtualmin
Refer to [docs/installation_on_virtualmin.md](docs/installation_on_virtualmin.md) for instructions on installing and configuring bPortal on a Virtualmin server.

## Installing bPortal as an application
Refer to [docs/pwa_installation.md](docs/pwa_installation.md) for instructions on installing bPortal as an application on your mobile or desktop devices.
