import os, sys

sys.path.append('/var/webapps/django/Course-Tracker')
sys.path.append('/var/webapps/django/Course-Tracker/course_tracker')

from course_tracker import settings
from django.core.management import setup_environ
setup_environ(settings)

# pull in "BackupMaker"
sys.path.append('/var/webapps/django/mcb_lib/poor-mans-db-backup')
from backupdb.backup_files import BackupMaker


if __name__ == '__main__':
    mb = BackupMaker(backup_name='Course Tracker')
    mb.make_backup()

