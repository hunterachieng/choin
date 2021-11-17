from django.urls import path
from . views import *
urlpatterns =[
    path('get_chain/', get_chain, name="get_chain"),
    path('add_transaction/', add_transaction, name="add_transaction"), #New
    path('is_valid/', is_valid, name="is_valid"), #New
    path('connect_node/', connect_node, name="connect_node"), #New
    path('replace_chain/', replace_chain, name="replace_chain"), #New
    path('trainer_reward/',reward,name='trainer_reward'),
    path('reward_confirm/<int:id>/',reward_confirm,name='trainer_reward_confirm'),
    path('trainer_trans/',trans,name='trainer_trans'),
    path('search/',search_student,name='trainer_search_student'),
    path('trainer-home/',trainer_home,name='trainer-home'),
    path('trainer-profile/',trainer_profile,name='trainer-profile'),
    path('view-trainer-profile/<int:id>/',view_trainer_profile,name='view-trainer-profile'),
    path('trainer_dashboard/',trainer_dashboard,name='trainer_dashboard'),
    ]

