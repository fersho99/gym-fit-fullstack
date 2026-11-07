from django.urls import re_path

from countries import views

urlpatterns = [
    re_path(r'^soap/country/(?P<codigo_iso>[A-Za-z]{2})/$', views.PaisSoapView.as_view(), name='soap_country'),
]
