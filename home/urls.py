from django.urls import path

from . import views

app_name = 'home'
urlpatterns = [
    # path('rayout',views.rayout,name='rayout'),
    path('',  views.index, name='index'),
    path('category',views.category, name='category'),
    path('contact', views.contact, name='contact'), 
    path('contact/done', views.done, name='done'),
]