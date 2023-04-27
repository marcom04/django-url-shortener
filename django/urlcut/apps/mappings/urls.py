from django.urls import path

from . import views

app_name = 'mappings'

urlpatterns = [
    path('<str:key>', views.ForwardToTargetView.as_view(), name='forward'),
]
