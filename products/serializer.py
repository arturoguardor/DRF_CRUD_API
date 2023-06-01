from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Product, Review


class UserSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(many=True, queryset=Product.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'product']


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('grade', 'author')


class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Product
        fields = ('title', 'price', 'reviews', 'owner')

    def create(self, validated_data):
        """
        Create and return a new `Product` instance, given the validated data.
        """
        return Product.objects.create(**validated_data)
