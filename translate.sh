#!/bin/bash

python manage.py makemessages -i env -a --settings=backoffice.settings --extension haml,html,txt,py
