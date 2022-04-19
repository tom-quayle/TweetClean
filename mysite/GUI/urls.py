from django.urls import path

from . import views

app_name = 'GUI'
urlpatterns = [
    path('', views.index, name='index'),
    path('FAQs/', views.FAQs, name='FAQs'),
    path('Manual/', views.Manual, name='Manual'),
    path('Results/', views.Results, name='Results'),
    path('Search/', views.Search, name='Search'),
    path('download/<str:filename>/', views.download_file, name='download_file'),
]