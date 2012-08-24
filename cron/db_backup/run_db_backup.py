import os, sys

#--------------------------------
# common section to import paths
#--------------------------------
util_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(util_dir)
from util.msg_util import *
from util.project_paths import *
#--------------------------------

from mcb_website import settings
from django.core.management import setup_environ
setup_environ(settings)

# pull in "BackupMaker"
sys.path.append('/var/webapps/django/mcb_lib/poor-mans-db-backup')
from backupdb.backup_files import BackupMaker


if __name__ == '__main__':
    mb = BackupMaker(backup_name='Course Tracker')
    mb.make_backup()

