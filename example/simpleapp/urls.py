# -*- coding: utf-8 -*-
"""

"""
from django.urls import path

from .views import NewsSearch


urlpatterns = [
    path('', NewsSearch.as_view()),
]
