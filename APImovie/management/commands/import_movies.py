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



import csv
from django.core.management.base import BaseCommand
from APImovie.models import Crew  # "yourapp" yerine ilgili uygulamanızın adını kullanın

class Command(BaseCommand):
    help = 'Load a list of crew members from a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file to import')

    def handle(self, *args, **kwargs):
        file_path = kwargs['csv_file']

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # İlk satırı atlayarak başlayın (başlık satırı varsayılır)

            for row in reader:
                crew_member = Crew(
                    id=row[0],
                    name=row[1],
                    role=row[2]
                )
                crew_member.save()

        self.stdout.write(self.style.SUCCESS('Crew members imported successfully!'))
