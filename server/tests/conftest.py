"""
Pytest configuration for Django tests.
This file ensures Django is properly configured before any tests run.
"""

import os
import django
from django.conf import settings

# Configure Django settings before importing any Django modules
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

# Setup Django
django.setup() 