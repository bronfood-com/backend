from django.urls import path

from .views import ReviewCreateAPIView, RestaurantReviewAPIView

app_name = 'review'

urlpatterns = [
    path('create_rating/<int:restaurant_id>',
         ReviewCreateAPIView.as_view(),
         name='review-create'),
    path('get_restaurant_rating/<int:restaurant_id>',
         RestaurantReviewAPIView.as_view(),
         name='reviews-get'),
]
