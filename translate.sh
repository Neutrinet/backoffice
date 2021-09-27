#!/bin/bash

python manage.py makemessages -i ve -a --settings=backoffice.settings --extension haml,html,txt,py
