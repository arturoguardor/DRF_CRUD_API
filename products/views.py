from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .serializer import ProductSerializer
from products.serializer import UserSerializer
from django.contrib.auth.models import User
from .models import Product, Review
from rest_framework import status, generics
from django.http import Http404
from rest_framework import permissions
from products.permissions import IsOwnerOrReadOnly


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProductView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request, pk, format=None):
        try:
            get_queryset = self.objects.get(pk)
            if request.method == 'GET':
                serializer_class = ProductSerializer(get_queryset, many=True)
                # Calculate average grade & total count of all reviews for each product
                for product in get_queryset:
                    reviews = product['reviews']
                    total_grade = sum([review['grade'] for review in reviews])
                    count = len(reviews)
                    avg_grade = round(total_grade/count, 1) if count != 0 else 0
                    product['average_grade'] = avg_grade
                    product['number_of_reviews'] = count
                    # Set author_review to None by default
                    product['author_review'] = None
                    # Get the author review for the product if available
                    author_review = Review.objects.filter(
                        product_id=product['id'],
                        author=request.author).first()

                    if author_review:
                        product['author_review'] = author_review.author
                return Response(serializer_class.data)
        except Product.DoesNotExist:
            raise Http404

    def create(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
