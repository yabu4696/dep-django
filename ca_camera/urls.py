from django.urls import path

from . import views

app_name = 'ca_camera'
urlpatterns = [
    path('',  views.index, name='index'),
    path('item/<slug:slug>', views.detail, name='detail'),
    path('delete', views.delete, name='delete'),
    path('item/<slug:slug>/exclusion', views.exclusion, name='exclusion'),
    path('maker_index',views.maker_index, name='maker_index'),
    path('maker/<slug:slug>', views.maker_detail, name='maker_detail'),
    path('contact', views.contact, name='contact'), 
    path('contact/done', views.done, name='done'),
    path('search_result', views.search_result, name='search_result'),
    path('preturn', views.preturn, name="preturn"),
    # path('rayout',views.rayout,name='rayout'),
    # path('form', views.form, name='form'),
    # path('reload/',views.reload, name='reload'),
    # path('item/<slug:slug>/edit', views.edit,name='edit'),
    # path('item/<slug:slug>/reload_one', views.reload_one, name='reload_one'),
    # path('celery_test/', views.celery_test, name='celery_test'),
]