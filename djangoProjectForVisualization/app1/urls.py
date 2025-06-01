from django.urls import path

import app1.views as views

urlpatterns = [
    path('test', views.test, name='test'),
    path('getres', views.get_res, name='getres'),
    path('getTwo_week', views.getTwo_week, name='getTwo_week'),
    path('getOne_week', views.getOne_week, name='getOne_week')

]