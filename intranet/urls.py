"""intranet URL Configuration
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
"""

# -----------------------------------------------Importing modules------------------------------------------------------
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app.views import SearchEngineView, MultiSimView
from app import views

# -------------------------------------------------Global variables-----------------------------------------------------
urlpatterns = [
    path('', SearchEngineView.as_view(), name='search-engine'),  # association between the Search engine button and the Search engine class
    path('sim', MultiSimView.as_view(), name='multi-sim'),  # association between the multi sim button and search engine
    path('search/', views.SearchPage, name='search_result'),  # association between the search bar, similarities AND the search page function
    path('sim/', views.allsimilarities, name='SIMS'),  # association between the search bar AND the SIMS function
]
