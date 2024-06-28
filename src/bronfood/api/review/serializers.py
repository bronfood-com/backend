from rest_framework import serializers
from bronfood.core.review.models import Review
from bronfood.core.restaurants.models import Restaurant


class ReviewSerializer(serializers.ModelSerializer):
    """ Сериалайзер для создания комментария и оценки ресторана.
    """
    comment = serializers.CharField(required=False)

    class Meta:
        model = Review
        fields = [
            'id',
            'client',
            'restaurant',
            'comment',
            'rating',
            'created_at',
        ]
        read_only_fields = ['created_at']


class SmallReviewSerializer(serializers.ModelSerializer):
    """ Сериалайзер для выдачи комментариев и оценок ресторану.
    """
    client_name = serializers.CharField(source='client.fullname', read_only=True)

    class Meta:
        model = Review
        fields = [
            'comment',
            'rating',
            'created_at',
            'client_name'
        ]

    # исключаем пустые комментарии из выдачи
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation.get('comment') is None:
            representation.pop('comment')
        return representation


class RestaurantReviewSerializer(serializers.ModelSerializer):
    """ Сериалайзер для предоставления сведений по рейтингу ресторана.
    """
    reviews = SmallReviewSerializer(many=True, read_only=True)
    restaurant_name = serializers.CharField(source='name', read_only=True)
    restaurant_rating = serializers.DecimalField(source='rating',
                                                 max_digits=2,
                                                 decimal_places=1,
                                                 read_only=True)
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = [
            'restaurant_name',
            'restaurant_rating',
            'review_count',
            'reviews'
        ]

    def get_review_count(self, obj):
        return obj.reviews.count()
