"""
ASGI config for smartpatrol project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

import django
# importing the routing file
# from channels.http import AsgiHandler for older versions
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartpatrol.settings')

application = ProtocolTypeRouter({
    # a list of protocols
    # "http" : AsgiHandler(),
    "http" : get_asgi_application(),


})
