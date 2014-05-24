#!/bin/bash
python manage.py test projectman.apps.admin.tests
python manage.py test projectman.apps.desarrollo.tests
python manage.py test projectman.apps.gestcambio.tests
read -p "Presione enter para cerrar .."
