from django.contrib import admin
from .models import Card

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'box', 'next_due', 'owner')
    search_fields = ('question', 'answer', 'category', 'owner__username')
    list_filter = ('box', 'next_due')
