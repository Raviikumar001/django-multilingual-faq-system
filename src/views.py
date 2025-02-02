"""
FAQ Management System Views.
Created: 2025-02-02
Author: Raviikumar001
"""

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

from .models import Category, FAQ, FAQTranslation
from .serializers import (
    CategorySerializer,
    FAQSerializer,
    FAQTranslationSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing FAQ categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    @action(detail=True)
    def faqs(self, request, pk=None):
        """Get all FAQs for a specific category."""
        category = self.get_object()
        faqs = FAQ.objects.filter(
            category=category,
            is_published=True
        )
        serializer = FAQSerializer(faqs, many=True)
        return Response(serializer.data)


class FAQViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing FAQs.
    """
    queryset = FAQ.objects.filter(is_published=True)
    serializer_class = FAQSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['question', 'answer']

    @action(detail=True, methods=['get'])
    def translations(self, request, pk=None):
        """Get all translations for a specific FAQ."""
        faq = self.get_object()
        translations = FAQTranslation.objects.filter(faq=faq)
        serializer = FAQTranslationSerializer(translations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def get_translation(self, request, pk=None):
        """Get FAQ in specific language."""
        faq = self.get_object()
        language_code = request.query_params.get('lang', None)

        if not language_code:
            return Response(
                {'error': _('Language code is required')},
                status=status.HTTP_400_BAD_REQUEST
            )

        translation = get_object_or_404(
            FAQTranslation,
            faq=faq,
            language_code=language_code
        )
        serializer = FAQTranslationSerializer(translation)
        return Response(serializer.data)