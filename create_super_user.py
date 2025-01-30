import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rest.settings")
django.setup()

SUPER_USER_LOGIN = os.getenv("SUPER_USER_LOGIN", "admin")
SUPER_USER_EMAIL = os.getenv("SUPER_USER_EMAIL", "")
SUPER_USER_PASSWORD = os.getenv("SUPER_USER_PASSWORD", "admin")

User = get_user_model()
if not User.objects.filter(username=SUPER_USER_LOGIN).exists():
    User.objects.create_superuser(SUPER_USER_LOGIN, SUPER_USER_EMAIL, SUPER_USER_PASSWORD)
    print(f"Superuser {SUPER_USER_LOGIN} created")
else:
    print(f"Superuser {SUPER_USER_LOGIN} already exists")
