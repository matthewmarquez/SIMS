from django.urls import path

from . import views

app_name='simslounge'
urlpatterns = [
    path('', views.index, name='index'),
    path('voteform/<int:proposal_id>', views.vote_form, name='voteform'),
    path('vote/<int:proposal_id>', views.vote, name='vote'),
    path('proposals/<int:lounge_id>', views.view_proposals, name='proposals'),
    path('login', views.login_handle, name='login'),
    path('login_page', views.login_page, name='login_page'),
    path('mylounges', views.my_lounges, name='my_lounges'),
    path('createproposal/<int:lounge_id>', views.create_proposal, name='createproposal'),
    path('proposalform/<int:lounge_id>', views.proposal_form, name='proposalform'),
    path('logout', views.logout_handle, name='logout'),
]

