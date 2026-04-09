from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('',                                           views.index,                  name='index'),
    path('register/',                                  views.register_view,          name='register'),
    path('login/',                                     views.login_view,             name='login'),
    path('logout/',                                    views.logout_view,            name='logout'),
    path('quiz/<int:quiz_id>/',                        views.playground,             name='playground'),
    path('quiz/<int:quiz_id>/q/<int:q_index>/',        views.question_partial,       name='question_partial'),
    path('quiz/<int:quiz_id>/submit/<int:q_index>/',   views.submit_answer,          name='submit_answer'),
    path('quiz/<int:quiz_id>/score/',                  views.scoreboard,             name='scoreboard'),
    path('quiz/<int:quiz_id>/review/<int:q_pk>/',      views.review_question_partial,name='review_question'),
    path('practice/<slug:topic>/',                     views.practice_page,          name='practice_page'),
    path('practice/<slug:topic>/next/',                views.practice_next,          name='practice_next'),
    path('practice/<slug:topic>/check/',               views.practice_check,         name='practice_check'),
    path('progress/',                                  views.dashboard,              name='progress'),
    path('dashboard/',                                 views.dashboard,              name='dashboard'),
    path('prizes/',                                    views.prizes_view,            name='prizes'),
    path('profile/',                                   views.profile_view,           name='profile'),
    # Parent / guardian routes
    path('parent/',                                    views.parent_dashboard_view,  name='parent_dashboard'),
    path('parent/register/',                           views.parent_register_view,   name='parent_register'),
    path('parent/assign/',                             views.assign_topic_view,      name='assign_topic'),
    path('parent/unassign/',                           views.unassign_topic_view,    name='unassign_topic'),
    path('assignments/complete/',                      views.complete_assignment_view, name='complete_assignment'),
]
