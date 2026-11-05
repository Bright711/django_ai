from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import ContactForm, NewsletterForm
from .models import Competition, LeagueStanding, Match, NewsArticle, NewsletterSubscriber, Player


def home(request):
    if request.method == "POST" and "newsletter_email" in request.POST:
        email = request.POST.get("newsletter_email", "")
        if NewsletterSubscriber.objects.filter(email__iexact=email).exists():
            messages.info(request, "You are already subscribed to club news.")
        elif email:
            from django.core.validators import validate_email
            from django.core.exceptions import ValidationError
            try:
                validate_email(email)
                NewsletterSubscriber.objects.create(email=email)
                messages.success(request, "Welcome to the United family.")
            except ValidationError:
                messages.error(request, "Please enter a valid email address.")
        return redirect("home")
    return render(request, "home.html", {
        "upcoming_matches": Match.objects.filter(status="upcoming").order_by("date")[:3],
        "recent_matches": Match.objects.filter(status="finished").order_by("-date")[:1],
        "articles": NewsArticle.objects.all()[:3],
        "featured_players": Player.objects.filter(is_featured=True)[:4],
        "standings": LeagueStanding.objects.all()[:10],
        "newsletter_form": NewsletterForm(),
    })


def players(request):
    position = request.GET.get("position", "")
    qs = Player.objects.all()
    if position in dict(Player.POSITION_CHOICES):
        qs = qs.filter(position=position)
    return render(request, "players.html", {"players": qs, "position": position})


def player_detail(request, slug):
    player = get_object_or_404(Player, slug=slug)
    return render(request, "player_detail.html", {"player": player, "related_players": Player.objects.exclude(pk=player.pk).filter(position=player.position)[:3]})


def matches(request):
    match_filter = request.GET.get("filter", "upcoming")
    qs = Match.objects.select_related("competition").all()
    if match_filter == "upcoming":
        qs = qs.filter(status="upcoming").order_by("date")
    elif match_filter == "results":
        qs = qs.filter(status="finished").order_by("-date")
    return render(request, "matches.html", {"matches": qs, "match_filter": match_filter})


def news(request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")
    qs = NewsArticle.objects.all()
    if query:
        qs = qs.filter(Q(title__icontains=query) | Q(summary__icontains=query))
    if category:
        qs = qs.filter(category=category)
    categories = NewsArticle.objects.values_list("category", flat=True).distinct()
    return render(request, "news.html", {"articles": qs, "categories": categories, "query": query, "category": category})


def article_detail(request, slug):
    article = get_object_or_404(NewsArticle, slug=slug)
    related = NewsArticle.objects.exclude(pk=article.pk).filter(category=article.category)[:3]
    return render(request, "article_detail.html", {"article": article, "related": related})


def history(request):
    return render(request, "history.html")


def standings(request):
    standings = LeagueStanding.objects.all()
    return render(request, "standings.html", {"standings": standings, "sample_data": True})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you. Your message has been received.")
            return redirect("contact")
        messages.error(request, "Please correct the highlighted fields.")
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form})
