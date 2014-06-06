#instalacion de paquetes
apt-get install python_setuptools -y
easy_install pip
pip install django
apt-get install python-psycopg2 -y

# OJO
cp /etc/apache2/apache2.conf.orig /etc/apache2/apache2.conf
rm -rf /var/www/*

#descarga de la versió indicada
cd /var/www/
wget https://github.com/nelsondspy/projectmn/archive/v$1.tar.gz
tar xvfz v$1.tar.gz

#fix para archivos estáticos

cd /var/www/projectmn-$1/projectman/projectman/static
mkdir base
mv admin bootstrap images logos jquery-1.10.2.min.js panel.css -t base

#configuración del apache
echo "Alias /static/ /var/www/projectmn-$1/projectman/projectman/static/" >> /etc/apache2/apache2.conf
echo "<Directory /var/www/projectmn-$1/projectman/projectman/static>" >> /etc/apache2/apache2.conf
echo "Require all granted" >> /etc/apache2/apache2.conf
echo "</Directory>" >> /etc/apache2/apache2.conf
echo "WSGIScriptAlias / /var/www/projectmn-$1/projectman/projectman/wsgi.py" >> /etc/apache2/apache2.conf

# configuracion wsgi.py
echo "import os" > /var/www/projectmn-$1/projectman/projectman/wsgi.py
echo "import sys" >> /var/www/projectmn-$1/projectman/projectman/wsgi.py
echo "path = '/var/www/projectmn-$1/projectman'" >> /var/www/projectmn-$1/projectman/projectman/wsgi.py
echo "if path not in sys.path:" >> /var/www/projectmn-$1/projectman/projectman/wsgi.py
echo "    sys.path.append(path)" >> /var/www/projectmn-$1/projectman/projectman/wsgi.py
echo "os.environ.setdefault(\"DJANGO_SETTINGS_MODULE\", \"projectman.settings\")" >> /var/www/projectmn-$1/projectman/projectman/wsgi.py
echo "from django.core.wsgi import get_wsgi_application" >> /var/www/projectmn-$1/projectman/projectman/wsgi.py
echo "application = get_wsgi_application()" >> /var/www/projectmn-$1/projectman/projectman/wsgi.py

# base de datos
python /var/www/projectmn-$1/projectman/manage.py syncdb
/var/www/projectmn-$1/projectman/run_poblar.sh

service apache2 restart

chmod 777 -R /var/www/
