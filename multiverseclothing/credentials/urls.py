from django.urls import path
from . import views
app_name="credentials"

urlpatterns = [
    path('',views.home,name="home"),
    path("demo/",views.demo,name="demo"),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

]