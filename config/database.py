import os


def database():
    client = os.getenv('DB_CLIENT', 'mysql')

    if client == 'sqlite':
        return {
            'ENGINE' : 'django.db.backends.sqlite3',
            'NAME'   : os.getenv('DB_NAME', 'database.sqlite'),
        }

    return {
        'ENGINE'               : f'django.db.backends.{client}',
        'HOST'                 : os.getenv('DB_HOST', ''),
        'PORT'                 : os.getenv('DB_PORT', '3306'),
        'USER'                 : os.getenv('DB_USER', ''),
        'PASSWORD'             : os.getenv('DB_PASSWORD', ''),
        'NAME'                 : os.getenv('DB_NAME', ''),
        'CONN_MAX_AGE'         : 60,
        'CONN_HEALTH_CHECKS'   : True,
        'OPTIONS'              : {
            'charset'          : 'utf8mb4',
        },
    }
