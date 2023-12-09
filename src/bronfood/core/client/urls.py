# Создать эдпоинты для клиента в api/client (views, serializers, urls)
# интегрировать их в основное приложение проекта (пока пустые)

from django.urls import path
from .views import ClientAPIView

app_name = 'client'

urlpatterns = [
    path('registration/', ClientAPIView.as_view(), name='index'),
    # path('login/', views.group_posts, name='group_posts'),
    # path('logout/',views.group_list, name='group_list'),
    # path('get_detail/',views.group_list, name='group_list'),
    # path('update/',views.group_list, name='group_list'),
    ]