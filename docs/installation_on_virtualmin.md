# Installation of bPortal on a virtualmin instance

This document describes how to install bPortal on a virtualmin server. 

Supported operating systems: Debian GNU/Linux 11.

## Requirements
Install the `SuitePY-service` in your SuiteCRM, check [SuitePY-Service README](https://github.com/joelbtactic/SuitePY-service/blob/improvements-v3/README.md).

## Install dependencies
The following dependencies are needed to run bPortal. You can install all dependences with:

```bash
sudo apt install libapache2-mod-wsgi-py3 gettext git
```

It's recommended to use `virtualenv` and `pip` packages to manage Python dependences. You can install both dependences with:

```bash
sudo apt install virtualenv python3-pip
```

## Clone the repository
Go to home directory of the virtualserver in which the portal will be installed and clone the repository of bPortal with:

```bash
git clone --recursive https://github.com/btactic/bPortal.git
```

## Prepare virtual environment

Once you have `virtualenv` and `pip` tools ready it's time to prepare the virtual environment to run the application.  
Following we create a virtual environment and install all Python dependencies:

```bash
cd bPortal
virtualenv env
source env/bin/activate
pip install -r requirements.txt
pip install -r suitepy/requirements.txt
deactivate
```
The `virtualenv env` command could show an error because the versions of `distlib` and `virtualenv` are incompatible, to correct this:
```
pip uninstall distlib
pip install distlib==0.3.6
```

## Configure bPortal settings
If `bPortal/custom_settings.py` config file does not exist then create it with:

```bash
cp bPortal/custom_settings.py.sample bPortal/custom_settings.py
```

After, edit `bPortal/custom_settings.py` file and set the following parameters conveniently:

- `ALLOWED_HOSTS` list of IPs and servernames on which the portal must listen.
- `SECRET_KEY` a random generated key (do not share this key). By example: `ceigohhaihohm0eam7ielei1Vie4ea9u`.
- `EMAIL_HOST` SMTP server used to send automatic emails.
- `EMAIL_PORT` SMTP port.
- `EMAIL_HOST_USER` SMTP user.
- `EMAIL_HOST_PASSWORD` SMTP password.
- `EMAIL_USE_TLS` left it to `True` if `TLS` is gone to be used. Otherwise set it as `False`.
- `DEFAULT_FROM_EMAIL` specify `FROM` used when sending emails.

## Configure SuiteCRM instance
Configuration of SuiteCRM instance that will be connected to the portal.

It is recommended to create a new user used exclusively to interact with the portal. As we use `suitecrm api v4_1` we will use it's credentials to autenticate.

Create `suitepy/suitepy.ini` file if it is not created, using the following template. Replace the API credentials given as example by the ones that you are going to use:

```ini
[SuiteCRM API Credentials]
url = https://example.org/custom/service/suitepy/rest.php
username = api
password = 123456
application_name = SuitePY
verify_ssl = True
```

## Configuring MySQL database
The following dependences are needed by the portal app to connect to the MySQL database. You can install the dependences with:

```bash
sudo apt install default-libmysqlclient-dev python3-dev
```

```bash
source env/bin/activate
pip install mysqlclient
deactivate

```

If `mysql_config.cnf` config file does not exist then create it with:

```bash
cp mysql_config.cnf.sample mysql_config.cnf
```

After, edit `mysql_config.cnf` with your MySQL connection settings.

Finally create the DB structure with:

```bash
source env/bin/activate
python3 manage.py migrate
deactivate
```

## Creating superuser account
Create a superuser account to manage the portal configuration:

```bash
source env/bin/activate
python3 manage.py createsuperuser
deactivate
```

## Compile static files and translations
You have to compile static files and translations. You can do it running the following commands inside `bPortal` directory:

```bash
source env/bin/activate
python3 manage.py collectstatic
./compile_messages.sh
deactivate
```

## Edit apache2 configuration
Modify `/etc/apache2/sites-available/{virtualserver}.conf` file and add the following parameters to the port `443` port:

```conf
WSGIDaemonProcess {virtualserver_user} user={virtualserver_user} python-path=/home/{virtualserver_home}/public_html/bPortal python-home=/home/{virtualserver_home}/public_html/bPortal/env
WSGIProcessGroup {virtualserver_group}
WSGIScriptAlias / /home/{virtualserver_home}/public_html/bPortal/bPortal/wsgi.py
Alias /static /home/{virtualserver_home}/public_html/bPortal/static
```

Comment/remove `DocumentRoot` directive from `80` and `443` port.

If you have SSL enabled you can redirect `HTTP` requests to `HTTPS` setting the following directive to the configuration of port `80`:

```
Redirect permanent / https://{virtualserver_domain}/
```

### apache2 configuration to support Let's Encrypt certificates
If you are planning to use the portal with a Let's Encrypt certificate you need to add the following rule in the virtualserver configuration, so Let's Encrypt can validate the certificate correctly.

```
Alias /.well-known/acme-challenge/ /home/{virtualserver_home}/public_html/.well-known/acme-challenge/
```

### Apply changes

Finally reload apache2 configuration with:

```bash
service apache2 reload
```
## Cases module configuration
To be able to use the **cases** module, you can read [setup.md](setup.md).
