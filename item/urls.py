from django.urls import path
from .views import  get_data
from .views import user_favorite_items_api_view
from . import views

app_name = 'item'

urlpatterns = [
    path('', views.items, name='items'),
    path('new/', views.new, name='new'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('api/data/', get_data, name='get_data'),
    path('item/<int:pk>/favorite/', views.add_to_favorite, name='add_to_favorite'),
    path('favorites/', views.favorite_items, name='favorite_items'),
    path('api/<int:user_id>/favorite-items/', user_favorite_items_api_view, name='user_favorite_items_api'),

]
