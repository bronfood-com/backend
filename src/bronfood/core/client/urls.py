# Создать эдпоинты для клиента в api/client (views, serializers, urls)
# интегрировать их в основное приложение проекта (пока пустые)
from rest_framework import urls
from django.urls import path, include
from .views import ClientAPIView, ClientLoginView, ClientLogoutView

app_name = 'client'

urlpatterns = [
    path('registration/', ClientAPIView.as_view(), name='index'),
    path('', include('rest_framework.urls')),
    path('my_login/', ClientLoginView.as_view(), name='my_login'),
    path('my_logout/', ClientLogoutView.as_view(), name='my_logout')
    # path('login/', views.group_posts, name='group_posts'),
    # path('logout/',views.group_list, name='group_list'),
    # path('get_detail/',views.group_list, name='group_list'),
    # path('update/',views.group_list, name='group_list'),
    ]