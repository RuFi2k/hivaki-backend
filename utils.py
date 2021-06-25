import os

cfgstring = 'host=potgres dbname=postgres user=postgres password=Hrvlgu_#!08'
SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')

def mapKeys(key, value):
  return '''{} = {}'''.format(key, value)