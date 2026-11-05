from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Competition(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    POSITION_CHOICES = [
        ("Goalkeepers", "Goalkeepers"),
        ("Defenders", "Defenders"),
        ("Midfielders", "Midfielders"),
        ("Forwards", "Forwards"),
    ]
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    number = models.PositiveIntegerField()
    position = models.CharField(max_length=20, choices=POSITION_CHOICES)
    nationality = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    biography = models.TextField(blank=True)
    image = models.ImageField(upload_to="players/", blank=True)
    image_url = models.URLField(blank=True)
    appearances = models.PositiveIntegerField(default=0)
    goals = models.PositiveIntegerField(default=0)
    assists = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["number"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("player_detail", args=[self.slug])

    def __str__(self):
        return self.name


class Match(models.Model):
    STATUS_CHOICES = [("upcoming", "Upcoming"), ("finished", "Finished")]
    VENUE_CHOICES = [("home", "Home"), ("away", "Away")]
    competition = models.ForeignKey(Competition, on_delete=models.PROTECT, related_name="matches")
    opponent = models.CharField(max_length=100)
    opponent_badge = models.CharField(max_length=20, blank=True, help_text="Short initials or badge text")
    date = models.DateTimeField()
    venue = models.CharField(max_length=10, choices=VENUE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="upcoming")
    united_score = models.PositiveIntegerField(blank=True, null=True)
    opponent_score = models.PositiveIntegerField(blank=True, null=True)
    stadium = models.CharField(max_length=100, blank=True)
    details = models.TextField(blank=True)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"Manchester United vs {self.opponent}"


class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=50, default="Club News")
    summary = models.TextField(max_length=500)
    content = models.TextField()
    image = models.ImageField(upload_to="news/", blank=True)
    image_url = models.URLField(blank=True)
    published_at = models.DateTimeField()
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["-published_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("article_detail", args=[self.slug])

    def __str__(self):
        return self.title


class LeagueStanding(models.Model):
    position = models.PositiveIntegerField(unique=True)
    club = models.CharField(max_length=100)
    crest = models.CharField(max_length=20, blank=True)
    played = models.PositiveIntegerField(default=0)
    won = models.PositiveIntegerField(default=0)
    drawn = models.PositiveIntegerField(default=0)
    lost = models.PositiveIntegerField(default=0)
    goal_difference = models.IntegerField(default=0)
    points = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return f"{self.position}. {self.club}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}: {self.subject}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
