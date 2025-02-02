"""
FAQ Management System Serializers.
Created: 2025-02-02
Author: Raviikumar001
"""

from rest_framework import serializers
from .models import Category, FAQ, FAQTranslation


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for FAQ categories."""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at']


class FAQTranslationSerializer(serializers.ModelSerializer):
    """Serializer for FAQ translations."""
    
    class Meta:
        model = FAQTranslation
        fields = [
            'id', 'language_code', 'question_translated',
            'answer_translated', 'created_at'
        ]


class FAQSerializer(serializers.ModelSerializer):
    """Serializer for FAQs."""
    
    category_name = serializers.CharField(
        source='category.name',
        read_only=True
    )
    translations = FAQTranslationSerializer(many=True, read_only=True)

    class Meta:
        model = FAQ
        fields = [
            'id', 'category', 'category_name', 'question',
            'answer', 'is_published', 'created_at', 'translations'
        ]