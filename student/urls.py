from django.urls import path
from . views import *

# from core.views import Profile
urlpatterns =[
    path('profile/<int:id>/',view_profile,name='view-student-profile'),
    path('redeem/',redeem,name='redeem'),
    path('edit-student-profile/',student_profile,name='student-profile'),
    path('redeem_failed/',redeem_failed,name='redeem_failed'),
    # path('redeem_success/',redeem_success,name='redeem_success'),
    path('cart/',cart,name='cart'),
    path('student_transactions/',student_transactions,name='student_transactions'),
    path('update_item/',update_item,name='update_item'),
    # path('redeemed_items/',view_redeemed_items,name='redeemed_items'),
    path('student_dashboard/',student_dashboard,name='student_dashboard'),
    # path('redeem_success/',redeem_success,name='redeem_success'),
    path('student_redeem/',student_redeem,name='student_redeem'),
    path('my_items/',my_items,name='my_items'),

    ]