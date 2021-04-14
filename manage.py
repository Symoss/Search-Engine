#!/usr/bin/env python

# Importing modules
import os
import sys


def main():
    # Running Administrative task
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intranet.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError() from exc
    execute_from_command_line(sys.argv)


# main
if __name__ == '__main__':
    main()
