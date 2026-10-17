from django.urls import path

from . import views

app_name = 'qastudio'

urlpatterns = [
    path('',                         views.studio,        name='studio'),
    path('s/<int:pk>/',              views.studio,        name='sample'),
    path('s/<int:pk>/frame/',        views.sim_frame,     name='sim_frame'),
    path('s/<int:pk>/question/',     views.sim_question,  name='sim_question'),
    path('s/<int:pk>/check/',        views.sim_check,     name='sim_check'),
    path('s/<int:pk>/draft/',        views.sim_draft,     name='sim_draft'),
    path('s/<int:pk>/vote/',         views.vote,          name='vote'),
    path('s/<int:pk>/proposal/',     views.save_proposal, name='proposal'),
    path('s/<int:pk>/comment/',      views.add_comment,   name='comment'),
    path('skill/<slug:slug>/ingest/',   views.ingest,        name='ingest'),
    path('skill/<slug:slug>/settings/', views.skill_settings, name='skill_settings'),
    path('team/',                    views.team,          name='team'),
    path('refresh/',                 views.refresh_all,   name='refresh'),
    path('export.<str:fmt>',         views.export,        name='export'),
]
