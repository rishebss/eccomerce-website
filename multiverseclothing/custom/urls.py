from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
app_name="custom"

urlpatterns = [
    path('uploaddesign/',views.uploaddesign,name="uploaddesign"),
    path('view-designs/', views.view_designs, name='view_designs'),


]
