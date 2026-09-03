import os
import sys

# Ensure the root directory of the project is added to sys.path
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studentproject.settings')

from studentproject.wsgi import application

# Vercel serverless WSGI handler
app = application
