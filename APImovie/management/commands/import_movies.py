# import csv
# from django.core.management.base import BaseCommand

# from APImovie.models import Movie
#   # "myapp" yerine kendi uygulamanızın adını kullanın

# class Command(BaseCommand):
#     help = 'Load a list of movies from a CSV file into the database'

#     def add_arguments(self, parser):
#         parser.add_argument('csv_file', type=str, help='The CSV file to import')

#     def handle(self, *args, **kwargs):
#         file_path = kwargs['csv_file']

#         with open(file_path, 'r', encoding='utf-8') as file:
#             reader = csv.reader(file)
#             next(reader)  # İlk satırı atlayarak başlayın (başlık satırı varsayılır)

#             for row in reader:
#                 movie = Movie(
#                     id=row[0],
#                     imdb_id=row[1],
#                     title=row[2],
#                     original_title=row[3],
#                     original_language=row[4],
#                     overview=row[5],
#                     release_date=row[6],
#                     runtime=row[7],
#                     vote_average=row[8],
#                     vote_count=row[9],
#                     popularity=row[10],
#                     background_path=row[11],
#                     poster_path=row[12]
#                 )
#                 movie.save()

#         self.stdout.write(self.style.SUCCESS('Movies imported successfully!'))
# import csv
# from django.core.management.base import BaseCommand

# from APImovie.models import Genre
#  # "yourapp" yerine ilgili uygulamanızın adını kullanın

# class Command(BaseCommand):
#     help = 'Load a list of genres from a CSV file into the database'

#     def add_arguments(self, parser):
#         parser.add_argument('csv_file', type=str, help='The CSV file to import')

#     def handle(self, *args, **kwargs):
#         file_path = kwargs['csv_file']

#         with open(file_path, 'r', encoding='utf-8') as file:
#             reader = csv.reader(file)
#             next(reader)  # İlk satırı atlayarak başlayın (başlık satırı varsayılır)

#             for row in reader:
#                 genre = Genre(
#                     id=row[0],
#                     genre_name=row[1]
#                 )
#                 genre.save()

#         self.stdout.write(self.style.SUCCESS('Genres imported successfully!'))



# import csv
# from django.core.management.base import BaseCommand
# from APImovie.models import Crew  # "yourapp" yerine ilgili uygulamanızın adını kullanın

# class Command(BaseCommand):
#     help = 'Load a list of crew members from a CSV file into the database'

#     def add_arguments(self, parser):
#         parser.add_argument('csv_file', type=str, help='The CSV file to import')

#     def handle(self, *args, **kwargs):
#         file_path = kwargs['csv_file']

#         with open(file_path, 'r', encoding='utf-8') as file:
#             reader = csv.reader(file)
#             next(reader)  # İlk satırı atlayarak başlayın (başlık satırı varsayılır)

#             for row in reader:
#                 crew_member = Crew(
#                     id=row[0],
#                     name=row[1],
#                     role=row[2]
#                 )
#                 crew_member.save()

#         self.stdout.write(self.style.SUCCESS('Crew members imported successfully!'))

# import csv
# from django.core.management.base import BaseCommand
# from APImovie.models import Movie_Genre, Movie, Genre  # Replace 'yourapp' with the name of your app

# class Command(BaseCommand):
#     help = 'Load a list of movie-genre associations from a CSV file into the database'

#     def add_arguments(self, parser):
#         parser.add_argument('csv_file', type=str, help='The CSV file to import')

#     def handle(self, *args, **kwargs):
#         file_path = kwargs['csv_file']

#         with open(file_path, 'r', encoding='utf-8') as file:
#             reader = csv.reader(file)
#             next(reader)  # Skip the first line if it's a header

#             for row in reader:
#                 movie_id = row[0]
#                 genre_id = row[1]

#                 movie = Movie.objects.get(id=movie_id)
#                 genre = Genre.objects.get(id=genre_id)

#                 movie_genre, created = Movie_Genre.objects.get_or_create(
#                     movie=movie,
#                     genre=genre
#                 )

#         self.stdout.write(self.style.SUCCESS('Movie-Genre associations imported successfully!'))

# import csv
# from django.core.management.base import BaseCommand
# from APImovie.models import MovieCrew, Movie, Crew  # "yourapp" yerine ilgili uygulamanızın adını kullanın

# class Command(BaseCommand):
#     help = 'Load a list of movie-crew associations from a CSV file into the database'

#     def add_arguments(self, parser):
#         parser.add_argument('csv_file', type=str, help='The CSV file to import')

#     def handle(self, *args, **kwargs):
#         file_path = kwargs['csv_file']

#         with open(file_path, 'r', encoding='utf-8') as file:
#             reader = csv.reader(file)
#             next(reader)  # İlk satırı atlayarak başlayın (başlık satırı varsayılır)

#             for row in reader:
#                 crew_id = row[1]
#                 movie_id = row[2]

#                 movie = Movie.objects.get(id=movie_id)
#                 crew = Crew.objects.get(id=crew_id)

#                 movie_crew, created = MovieCrew.objects.get_or_create(
#                     movie=movie,
#                     crew=crew
#                 )

#         self.stdout.write(self.style.SUCCESS('Movie-Crew associations imported successfully!'))
# import csv
# from django.core.management.base import BaseCommand
# from APImovie.models import Actor  # Replace 'yourapp' with the name of your app

# class Command(BaseCommand):
#     help = 'Load a list of actors from a CSV file into the database'

#     def add_arguments(self, parser):
#         parser.add_argument('csv_file', type=str, help='The CSV file to import')

#     def handle(self, *args, **kwargs):
#         file_path = kwargs['csv_file']

#         with open(file_path, 'r', encoding='utf-8') as file:
#             reader = csv.reader(file)
#             next(reader)  # Skip the first line if it's a header

#             for row in reader:
#                 actor_name = row[0]
#                 actor_id = row[1]
#                 profile_path = row[2]

#                 actor, created = Actor.objects.get_or_create(
#                     id=actor_id,
#                     defaults={
#                         'actor_name': actor_name,
#                         'profile_path': profile_path
#                     }
#                 )

#         self.stdout.write(self.style.SUCCESS('Actors imported successfully!'))
import csv
from django.core.management.base import BaseCommand
from APImovie.models import Cast, Actor, Movie  # Replace 'APImovie' with your app's name

class Command(BaseCommand):
    help = 'Load a list of cast members from a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file to import')

    def handle(self, *args, **kwargs):
        file_path = kwargs['csv_file']

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the first line if it's a header

            for row in reader:
                id=row[0]
                actor_id = row[1]
                movie_id = row[2]
                character_name = row[3]

                # Fetch the related Actor and Movie instances
                actor = Actor.objects.get(id=actor_id)
                movie = Movie.objects.get(id=movie_id)

                # Create or update the Cast instance
                cast, created = Cast.objects.get_or_create(
                    id=id,
                    actor_id=actor,
                    character_name=character_name,
                    movie_id=movie
                )

        self.stdout.write(self.style.SUCCESS('Cast members imported successfully!'))

# Example CSV format: actor_id,character_name,movie_id
