# Code
/var/webapps/django/Course-Tracker

# wsgi
/var/www/course-tracker/course-tracker/wsgi_course_tracker.wsgi

# .htaccess 
at /var/wwww/course-tracker/.htaccess

# manually move prod_fas.py

# run django project basics
python manage.py validate
python manage.py syncdb
sudo python manage.py collectstatic

# getting mod_wsgi to work
* ExecCGI missing in conf file
sudo vim /etc/apache2/sites-enabled/20-mcb-adminapps.unix.fas.harvard.edu.conf 

sudo /etc/init.d/apache2 restart