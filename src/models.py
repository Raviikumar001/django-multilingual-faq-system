"""
FAQ Management System Models.
Created: 2025-02-02
Author: Raviikumar001
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField


class Category(models.Model):
    """Category model for organizing FAQs."""
    
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text=_("Category name")
    )
    description = models.TextField(
        blank=True,
        help_text=_("Optional category description")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["name"]

    def __str__(self):
        return self.name


class FAQ(models.Model):
    """FAQ model containing questions and answers."""
    
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="faqs",
        help_text=_("Category this FAQ belongs to")
    )
    question = models.CharField(
        max_length=255,
        help_text=_("The frequently asked question")
    )
    answer = RichTextField(
        help_text=_("The answer to the question")
    )
    is_published = models.BooleanField(
        default=True,
        help_text=_("Whether this FAQ is visible to users")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")
        ordering = ["category", "-created_at"]

    def __str__(self):
        return self.question


class FAQTranslation(models.Model):
    """Store translations for FAQs."""
    
    faq = models.ForeignKey(
        FAQ,
        on_delete=models.CASCADE,
        related_name="translations",
        help_text=_("The FAQ this translation belongs to")
    )
    language_code = models.CharField(
        max_length=10,
        help_text=_("Language code (e.g., 'es' for Spanish)")
    )
    question_translated = models.CharField(
        max_length=255,
        help_text=_("Translated question")
    )
    answer_translated = RichTextField(
        help_text=_("Translated answer")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("FAQ Translation")
        verbose_name_plural = _("FAQ Translations")
        unique_together = ["faq", "language_code"]
        ordering = ["faq", "language_code"]

    def __str__(self):
        return f"{self.faq.question} ({self.language_code})"