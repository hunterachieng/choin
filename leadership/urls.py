from django.urls import path
from . views import add_reward, redeemed_items,search_student_by_admin, ajax_change_status, deactivate_ajax_change_status,search_redeemable_item, add_transaction,search_student,connect_node, delete_metric, edit_metric, get_chain, is_valid, profile_upload, replace_chain, reward, reward_confirm,trainer_profile_upload,addMetric, trans, redeemableItemsList,view_student_leaderboard,leadership_profile
urlpatterns =[
    path('get_chain/', get_chain, name="get_chain"),
    path('add_transaction/', add_transaction, name="add_transaction"), #New
    path('is_valid/', is_valid, name="is_valid"), #New
    path('connect_node/', connect_node, name="connect_node"), #New
    path('replace_chain/', replace_chain, name="replace_chain"), #New
    path('upload/',profile_upload,name='upload'),
    path('trainer-upload/',trainer_profile_upload,name='trainer-upload'),
    path('reward/',reward,name='reward'),
    path('reward_confirm/<int:id>/',reward_confirm,name='reward_confirm'),
    path('metrics/',addMetric,name='metrics'),
    path('delete_metric/<int:id>',delete_metric,name='delete'),
    path('edit_metric/<int:id>',edit_metric,name='edit'),
    path('trans/',trans,name='trans'),
    path('search/',search_student,name='search_student'),
    path('add-reward-item/',add_reward,name='add-reward-item'),
    path('redeemable-items/', redeemableItemsList, name='redeemable-items'),
    path('search_redeemable-items/',search_redeemable_item, name='search_redeemable_item'),
    path('search_student_by_admin/',search_student_by_admin,name='search_student_by_admin'),
    path('ajax/change_status/', ajax_change_status, name='ajax_change_status'),
    path('deactivate/ajax/change_status/', deactivate_ajax_change_status, name='deactivate_ajax_change_status'),
    path('leaderboard/',view_student_leaderboard, name='view_student_leaderboard'),
    path('redeemed_items/',redeemed_items, name='redeemed_items'),
    path('leadership-profile/',leadership_profile, name='leadership-profile'),


]