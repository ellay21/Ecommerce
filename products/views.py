import os
import requests
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from users.permissions import IsOwnerOrAdmin

class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing product instances.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve', 'search']: # Added 'search' here for later
            permission_classes = [permissions.AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy', 'generate_description']: # Added our new action
            permission_classes = [IsOwnerOrAdmin]
        else: 
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """
        Ensure the creator of the product is set as the owner.
        And only admins or merchants can create.
        """
        if self.request.user.role not in ['admin', 'merchant']:
            self.permission_denied(
                self.request,
                message="You must be an Admin or Merchant to create products."
            )
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def generate_description(self, request, pk=None):
        """
        An AI-powered action to generate a product description using Gemini.
        """
        product = self.get_object()
        api_key = os.getenv('GEMINI_API_KEY')

        if not api_key:
            return Response(
                {"error": "GEMINI_API_KEY is not configured."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        prompt = (f"Generate a compelling, short e-commerce product description for the following item. "
                  f"Do not include the product name or category in the description itself. "
                  f"Product Name: {product.name}, Category: {product.category}.")

        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
        try:
            response = requests.post(
                api_url,
                json={"contents": [{"parts": [{"text": prompt}]}]},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

            # Parse the Gemini API response
            data = response.json()
            description = data['candidates'][0]['content']['parts'][0]['text'].strip()

            # Update the product and save it
            product.description = description
            product.save()

            # Return the updated product data
            serializer = self.get_serializer(product)
            return Response(serializer.data)

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Failed to connect to AI service: {e}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except (KeyError, IndexError) as e:
            return Response(
                {"error": f"Could not parse AI response: {e}", "raw_response": data},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
