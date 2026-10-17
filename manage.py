import os
import sys

sys.dont_write_bytecode = True


def main():
    from dotenv import load_dotenv
    from django.core.management import execute_from_command_line

    load_dotenv()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    if sys.argv[1:] == ['runserver']:
        sys.argv.append(f"{os.getenv('HOST', '0.0.0.0')}:{os.getenv('PORT', '3000')}")

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
