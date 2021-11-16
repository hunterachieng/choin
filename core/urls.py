from django.contrib.auth.views import PasswordChangeDoneView
from django.urls import path
from . views import  *
from student.urls import *
from trainer.urls import *
from leadership.urls import *

urlpatterns=[
    path('',LoginView.as_view(),name='login'),
    path('home/',index,name='index'),
    path('profile/',Profile,name='user-profile'),
    path('navbar/',navbar,name='nav_bar'),
    path('change_password/',change_password, name='change_password'),
    path('forbidden/',forbidden, name='forbidden'),

    ]