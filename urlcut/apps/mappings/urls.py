from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'mappings'

urlpatterns = [
    path('', views.shorten_url, name='index'),
    path('<str:key>', views.ForwardToTargetView.as_view(), name='forward'),
]
