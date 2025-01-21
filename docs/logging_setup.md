# Logging Setup

This document explains how to configure the logging settings for `bPortal`, including changing the log level, modifying log retention, and adjusting log handlers to suit your needs.

## Change Log Level

To change the log level in `bPortal`, locate the `LOGGING` dictionary in `settings.py`. By default, it is configured as follows:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'timed_rotating_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'django_error.log'),
            'when': 'midnight',
            'interval': 1,
            'backupCount': 7,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['timed_rotating_file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'bPortal': {
            'handlers': ['timed_rotating_file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
```

## Core Loggings Settings

These are the essential logging settings that define how bPortal handles log messages:

1. `LOGGING['loggers']['django']['level']` - `LOGGING['loggers']['bPortal']['level']` - `LOGGING['handlers']['timed_rotating_file']['level']`
    - Specifies the logging level for **Django** and **bPortal** related logs.
    - Specifies the logging level for the handler.
    - Default: `ERROR`
    - Available options:
        - `DEBUG`: Shows detailed debug information.
        - `INFO`: General operational information.
        - `WARNING`: Potential issues that don't interrupt execution.
        - `ERROR`: Errors that need immediate attention.
        - `CRITICAL`: Severe errors causing premature termination.

2. `LOGGING['handlers']['timed_rotating_file']['filename']`
    - Defines the file where logs are stored.
    - Default: `django_error.log` in the base directory.
    - Update this path to customize the log file location.

3. `LOGGING['handlers']['timed_rotating_file']['when']`
    - Configures when logs rotate (e.g., daily, weekly).
    - Default: `midnight`
    - Options: `midnight`, `daily`, `hourly`, etc.

4. `LOGGING['handlers']['timed_rotating_file']['backupCount']`
    - Specifies the number of log files to retain.
    - Default: `7` (one week of logs).
    - Adjust this value based on storage or compliance needs.

5. `LOGGING['formatters']['verbose']['format']`
    - Defines the format of log messages.
    - Default: `{levelname} {asctime} {message}`

## How to Modify Logging
### Changing Log Levels
To adjust the log level for bPortal or Django logs:

1. Open `bPortal/settings.py`.
2. Locate the `LOGGING` dictionary.
3. Update the level value for the desired logger.
    - Example: To enable debug logs for bPortal:
        ```python
        LOGGING = {

            'handlers': {
                'timed_rotating_file': {
                    'level': 'DEBUG',  # Change this to 'DEBUG'
                    ...
                },
            },
            'loggers': {
                'django': {
                    'handlers': ['timed_rotating_file'],
                    'level': 'DEBUG',  # Change this to 'DEBUG'
                    'propagate': True,
                },
                'bPortal': {
                    'handlers': ['timed_rotating_file'],
                    'level': 'DEBUG',  # Change this to 'DEBUG'
                    'propagate': False,
                },
            },
        }
        ```
### Rotating and Retaining Logs
- To modify the log rotation interval, change the `when` key under the `timed_rotating_file` handler.
Example: Rotate logs every hour instead of daily:
    ```python
    'when': 'H',
    ```

- To adjust log retention, update the backupCount key.
Example: Keep 30 days of logs:
    ```python
    'backupCount': 30,
    ```

## Applying Changes
- Local Development: Changes take effect immediately after saving settings.py.
- Deployed Server: Restart your web server (e.g., Apache) for the changes to take effect:
    ```
    service apache2 reload
    ```

For more information on Django logging, see the [Django Logging Documentation](https://docs.djangoproject.com/en/stable/topics/logging/).
