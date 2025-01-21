# Installation of bPortal on a virtualmin instance

This document describes how to install bPortal on a virtualmin server. 

Supported operating systems: Debian GNU/Linux 11.

## Requirements
Install the `SuitePY-service` in your SuiteCRM, check [SuitePY-Service README](https://github.com/btactic/SuitePY-service/blob/master/README.md).

## Install dependencies
The following dependencies are required to run bPortal. Install them with:

```bash
sudo apt install libapache2-mod-wsgi-py3 gettext git
```

It is recommended to use virtualenv and pip to manage Python dependencies. Install both with:

```bash
sudo apt install virtualenv python3-pip
```

## Clone the repository
Navigate to the home directory of the Virtualmin virtual server where the portal will be installed, and clone the bPortal repository:

```bash
git clone --recursive https://github.com/btactic/bPortal.git
```

## Prepare virtual environment

Once you have the `virtualenv` and `pip` tools ready, it is time to prepare the virtual environment to run the application.
The following steps will create a virtual environment and install all Python dependencies:

```bash
cd bPortal
virtualenv env
source env/bin/activate
pip install -r requirements.txt
pip install -r suitepy/requirements.txt
pip install -r dolibarrpy/requirements.txt
deactivate
```

## Configure bPortal settings
If the `bPortal/custom_settings.py` file does not exist, create it with:

```bash
cp bPortal/custom_settings.py.sample bPortal/custom_settings.py
```

Next, edit `bPortal/custom_settings.py` file and set the following parameters appropriately:

- `ALLOWED_HOSTS` List of IPs and servernames on which the portal must listen.
- `SECRET_KEY` A random generated key (do not share this key). By example: `ceigohhaihohm0eam7ielei1Vie4ea9u`.
- `EMAIL_HOST` SMTP server used to send automatic emails.
- `EMAIL_PORT` SMTP port.
- `EMAIL_HOST_USER` SMTP user.
- `EMAIL_HOST_PASSWORD` SMTP password.
- `EMAIL_USE_TLS` Set to `True` if `TLS` is to be used. Otherwise set it to `False`.
- `DEFAULT_FROM_EMAIL` Specify the `FROM` addres used when sending emails.

## Configure SuiteCRM instance
Configuration of SuiteCRM instance that will be connected to the portal.

bPortal uses `suitecrm api v8` for authentication. To use this API, you need to create a `Client Credentials client` in your SuiteCRM instance.

If `suitepy/suitepy.ini` does not exist, create it using this template and replace the placeholders with your API credentials:

```ini
[SuiteCRM API Credentials]
url = https://crm.example.org
client_id = your_client_id
client_secret = your_client_secret
application_name = SuitePY
suitecrmversion = 7
verify_ssl = True
```

Set the `suitecrmversion` parameter to **7** or **8**, depending on the SuiteCRM version you are using.

## Configure Dolibarr instance
Configuration of the Dolibarr instance that will be connected to the portal.

For the `Dolibarr API`, it is recommended to create a new user specifically for interacting with the portal. This is because the **api_token** is tied to the user account.

If `dolibarrpy/dolibarrpy.ini` does not exist, create it using this template and replace the placeholders with your API credentials:

```ini
[Dolibarr API Credentials]
url = https://dolibarr.example.net/api/index.php/
api_token = your_api_token
application_name = DolibarrPY
verify_ssl = True
```

## Configuring MySQL database
Install the following dependencies to connect the portal app to a MySQL database:

```bash
sudo apt install default-libmysqlclient-dev python3-dev
```

Install the MySQL client library in your virtual environment:
```bash
source env/bin/activate
pip install mysqlclient
deactivate
```

If `mysql_config.cnf` config file does not exist, create it with:

```bash
cp mysql_config.cnf.sample mysql_config.cnf
```

Next, edit `mysql_config.cnf` with your MySQL connection settings.

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
To deploy bPortal, edit the Apache2 configuration using one of the following options: Virtualmin or Apache Configuration via CLI.

### Option 1 - Virtualmin
#### Port 80 Configuration
To edit the apache2 configuration in port 80, you need to follow the next steps:
1. Access Virtualmin.
2. Select the virtual server for your bPortal.
3. Go to **Web Configuration** > **Configure Website** > **Edit Directives**.

Inside the `Edit directives` document first you need to remove the `DocumentRoot` directive.

If you are planning to use the portal with a **Let's Encrypt certificate** you need to add the following rule at the end of the `Edit directives` document:

```conf
Alias /.well-known/acme-challenge/ /home/{virtualserver_home}/public_html/.well-known/acme-challenge/
```

If you have SSL enabled you can redirect `HTTP` requests to `HTTPS` setting the following directive to the configuration of port `80` at the end of the `Edit directives` document:

```
Redirect permanent / https://{virtualserver_domain}/
```

Finally save the modifications.
#### Port 443 Configuration
To edit the apache2 configuration in port 80, you need to follow the next steps below:
1. Access Virtualmin.
2. Select the virtual server for your bPortal.
3. Go to **Web Configuration** > **Configure SSL Website** > **Edit Directives**.

Inside the `Edit directives` document, you need to remove the `DocumentRoot` directive.

At the end of the `Edit directives` add the following parameters:

```conf
WSGIDaemonProcess {virtualserver_user} user={virtualserver_user} python-path=/home/{virtualserver_home}/public_html/bPortal python-home=/home/{virtualserver_home}/public_html/bPortal/env
WSGIProcessGroup {virtualserver_group}
WSGIScriptAlias / /home/{virtualserver_home}/public_html/bPortal/bPortal/wsgi.py
Alias /static /home/{virtualserver_home}/public_html/bPortal/static
```

If you are planning to use the portal with a Let's Encrypt certificate you need to add the following rule at the end of the `Edit directives` document:

```conf
Alias /.well-known/acme-challenge/ /home/{virtualserver_home}/public_html/.well-known/acme-challenge/
```
Finally save the modifications.

#### Apply changes
Inside the `Configure Website` or `Configure SSL Website` click on `Apply Changes`, it applies the modifications for both ports.

### Option 2 - Apache Configuration via CLI
Edit `/etc/apache2/sites-available/{virtualserver}.conf` file and make the following updates:
1. Remove `DocumentRoot` directive from `80` and `443` port.
2. Add these configurations to the port `443` section:

    ```conf
    WSGIDaemonProcess {virtualserver_user} user={virtualserver_user} python-path=/home/{virtualserver_home}/public_html/bPortal python-home=/home/{virtualserver_home}/public_html/bPortal/env
    WSGIProcessGroup {virtualserver_group}
    WSGIScriptAlias / /home/{virtualserver_home}/public_html/bPortal/bPortal/wsgi.py
    Alias /static /home/{virtualserver_home}/public_html/bPortal/static
    ```

3. If you have SSL enabled you can redirect `HTTP` requests to `HTTPS` setting the following directive to the configuration of port `80`:

    ```
    Redirect permanent / https://{virtualserver_domain}/
    ```

4. If you are planning to use the portal with a Let's Encrypt certificate you need to add the following rule for both ports in the virtualserver configuration, so Let's Encrypt can validate the certificate correctly.

    ```
    Alias /.well-known/acme-challenge/ /home/{virtualserver_home}/public_html/.well-known/acme-challenge/
    ```

#### Apply changes

Finally reload apache2 configuration with:

```bash
service apache2 reload
```
## Cases module configuration
To be able to use the **cases** module, you can read [setup.md](setup.md).

## Progressive web app (PWA) configuration
To configure the PWA settings for your bPortal, you can read [pwa_setup.md](pwa_setup.md).

## Logging configuration
To configure the logs of your bPortal, you can read the [logging_setup.md](logging_setup.md).