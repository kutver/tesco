from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:category>/<str:second_category>/<str:third_category>/<int:page>', views.details, name='details'),
    path('<str:category>/<str:second_category>/<str:third_category>/<int:page>/export', views.export, name='export'),
    path('search', views.search_url, name='search-by-url'),
]
