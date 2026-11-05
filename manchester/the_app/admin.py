from django.contrib import admin
from .models import *

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("number", "name", "position", "nationality", "is_featured")
    list_filter = ("position", "is_featured")
    search_fields = ("name", "nationality")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("opponent", "competition", "date", "venue", "status", "united_score", "opponent_score")
    list_filter = ("status", "venue", "competition")

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published_at", "is_featured")
    list_filter = ("category", "is_featured")
    search_fields = ("title", "summary")
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Competition)
admin.site.register(LeagueStanding)
admin.site.register(ContactMessage)
admin.site.register(NewsletterSubscriber)
