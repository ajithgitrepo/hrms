import os
import sys
from django.core.wsgi import get_wsgi_application

# sys.path.append('/var/www/hrms/core')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()
