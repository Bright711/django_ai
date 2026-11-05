from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from the_app.models import Competition, Match, NewsArticle, Player, LeagueStanding


class Command(BaseCommand):
    help = "Seed the website with development sample content"

    def handle(self, *args, **options):
        pl, _ = Competition.objects.get_or_create(name="Premier League")
        cl, _ = Competition.objects.get_or_create(name="UEFA Champions League")
        fa, _ = Competition.objects.get_or_create(name="FA Cup")

        if not Player.objects.exists():
            players = [
                ("Andre Onana", 24, "Goalkeepers", "Cameroon", True, 14, 0, 1),
                ("Harry Maguire", 5, "Defenders", "England", True, 19, 2, 0),
                ("Lisandro Martinez", 6, "Defenders", "Argentina", False, 16, 0, 1),
                ("Luke Shaw", 23, "Defenders", "England", False, 17, 0, 3),
                ("Bruno Fernandes", 8, "Midfielders", "Portugal", True, 25, 7, 8),
                ("Casemiro", 18, "Midfielders", "Brazil", True, 21, 3, 2),
                ("Rasmus Hojlund", 11, "Forwards", "Denmark", True, 23, 10, 2),
                ("Marcus Rashford", 10, "Forwards", "England", False, 24, 8, 5),
            ]
            for name, number, position, nationality, featured, apps, goals, assists in players:
                Player.objects.create(name=name, number=number, position=position, nationality=nationality,
                    is_featured=featured, appearances=apps, goals=goals, assists=assists,
                    image_url="https://images.unsplash.com/photo-1579952363873-27f3bade9f55?auto=format&fit=crop&w=800&q=85",
                    biography=f"{name} is a member of the Manchester United first-team squad, known for determination, technical quality and commitment on the pitch.")

        if not Match.objects.exists():
            now = timezone.now()
            Match.objects.create(competition=pl, opponent="Liverpool", opponent_badge="LIV", date=now+timedelta(days=7), venue="home", status="upcoming", stadium="Old Trafford")
            Match.objects.create(competition=cl, opponent="Atletico Madrid", opponent_badge="ATM", date=now+timedelta(days=14), venue="away", status="upcoming", stadium="Metropolitano Stadium")
            Match.objects.create(competition=fa, opponent="Chelsea", opponent_badge="CHE", date=now+timedelta(days=21), venue="home", status="upcoming", stadium="Old Trafford")
            Match.objects.create(competition=pl, opponent="Manchester City", opponent_badge="MCI", date=now-timedelta(days=7), venue="away", status="finished", united_score=2, opponent_score=1, stadium="Etihad Stadium")

        if not NewsArticle.objects.exists():
            now = timezone.now()
            articles = [
                ("United ready for the challenge ahead", "Match Preview", "The Reds turn their attention to a defining weekend at Old Trafford.", True),
                ("Inside training: Focus and intensity", "Training", "A closer look at the work behind the scenes as the squad prepares for the next match.", False),
                ("Academy talent making an impression", "Academy", "Promising young players continue their development within the Manchester United pathway.", False),
            ]
            for i, (title, category, summary, featured) in enumerate(articles):
                NewsArticle.objects.create(title=title, category=category, summary=summary,
                    content=f"{summary}\n\nManchester United players, staff and supporters look ahead to the next chapter with focus, pride and ambition. The club's commitment to entertainment, courage and development remains at the heart of everything it does.",
                    published_at=now-timedelta(days=i*2), is_featured=featured,
                    image_url=["https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&w=1200&q=85",
                               "https://images.unsplash.com/photo-1517927033932-b3d18e61fb3a?auto=format&fit=crop&w=1200&q=85",
                               "https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?auto=format&fit=crop&w=1200&q=85"][i])

        if not LeagueStanding.objects.exists():
            sample = [
                (1,"Arsenal","ARS",0,0,0,0,0,0),(2,"Liverpool","LIV",0,0,0,0,0,0),
                (3,"Manchester City","MCI",0,0,0,0,0,0),(4,"Chelsea","CHE",0,0,0,0,0,0),
                (5,"Newcastle United","NEW",0,0,0,0,0,0),(6,"Tottenham Hotspur","TOT",0,0,0,0,0,0),
                (7,"Manchester United","MUN",0,0,0,0,0,0),(8,"Aston Villa","AVL",0,0,0,0,0,0),
                (9,"Brighton","BHA",0,0,0,0,0,0),(10,"West Ham United","WHU",0,0,0,0,0,0),
            ]
            for pos, club, crest, played, won, drawn, lost, gd, points in sample:
                LeagueStanding.objects.create(position=pos, club=club, crest=crest, played=played,
                    won=won, drawn=drawn, lost=lost, goal_difference=gd, points=points)
        self.stdout.write(self.style.SUCCESS("Sample club data seeded successfully."))
