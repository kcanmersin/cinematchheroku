from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import CommentForm
from rest_framework import viewsets, generics,status
from .models import Comment, Movie, MovieList, Vote
from django.views.generic import ListView, DetailView, CreateView
from .serializers import CommentSerializer, MovieSerializer, MovieListSerializer, VoteSerializer,RateSerializer,MovieSearchSerializer,UserSerializer,MovieSForYouSerializer, test,testGenre
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import render, get_object_or_404
from .models import Movie, Movie_Genre, Genre, Cast, Actor, Crew, MovieCrew,Rate
from rest_framework.permissions import AllowAny

from accounts.models import UserAccount, UserProfile
from django.db.models import F
from rest_framework import filters
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

class ActorMovieDetail(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk, format=None):
        # Ensure request is not None
        if request is None:
            return Response({"error": "Request object is None."}, status=status.HTTP_400_BAD_REQUEST)

        # Get all cast entries for the actor
        cast_entries = Cast.objects.filter(actor_id=pk)

        # Get all movie instances from these cast entries
        movies = [cast_entry.movie_id for cast_entry in cast_entries]

        # Serialize the movie data
        serializer = MovieSearchSerializer(movies, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
class CrewMovieDetail(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk, format=None):
        # Ensure request is not None
        if request is None:
            return Response({"error": "Request object is None."}, status=status.HTTP_400_BAD_REQUEST)

        # Get all movie crew entries for the crew member
        movie_crew_entries = MovieCrew.objects.filter(crew_id=pk)

        # Get all movie instances from these movie crew entries
        movies = [movie_crew_entry.movie for movie_crew_entry in movie_crew_entries]

        # Serialize the movie data
        serializer = MovieSearchSerializer(movies, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
class ForYouView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            # ID'si 2 olan kullanıcı profilini al
            #user_profile = UserProfile.objects.get(user__id=2)
            user_profile = UserProfile.objects.get(user=request.user)

            recommended_movie_ids = user_profile.get_for_you()  # Kullanıcının önerilen filmlerini alır

            # Önerilen filmleri serialize et
            recommended_movies = []
            for movie_id in recommended_movie_ids:
                try:
                    movie = Movie.objects.get(id=movie_id)
                    serializer = MovieSForYouSerializer(movie, context={'request': request})
                    recommended_movies.append(serializer.data)
                except Movie.DoesNotExist:
                    continue

            return Response(recommended_movies)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
class SearchBarCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Movie.objects.all()
    serializer_class = MovieSearchSerializer

    queryset1 = UserAccount.objects.all()
    serializer_class1 = UserSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['^title']
    search_fields1 = ['^username']

    def get_queryset(self):
        search_term = self.request.query_params.get('search', '')
        
        # Filter movies based on the search term
        movies = self.queryset.filter(title__istartswith=search_term)
        
        # Filter users based on the search term
        users = self.queryset1.filter(username__istartswith=search_term)

        return {'movies': movies, 'users': users}

    def list(self, request, *args, **kwargs):
        queryset_dict = self.get_queryset()

        # Serialize movies and users separately
        movies_serializer = self.get_serializer(queryset_dict['movies'], many=True)
        users_serializer = self.serializer_class1(queryset_dict['users'], many=True)

        # Combine serialized data into a single dictionary
        serialized_data = {
            'movies': movies_serializer.data,
            'users': users_serializer.data
        }

        return Response(serialized_data)
class MovieDetailView(APIView):
    permission_classes = [AllowAny]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get(self, request, pk, format=None):
        movie = self.queryset.filter(pk=pk).first()
        if movie:
            movie_serializer = self.serializer_class(movie, context={'request': request})
            movie_data = movie_serializer.data

            # Check if the user is authenticated
            if request.user.is_authenticated:
                user_rating = Rate.objects.filter(movie=movie, user=request.user).first()
                if user_rating:
                    rating_serializer = RateSerializer(user_rating)
                    movie_data['user_rating'] = rating_serializer.data
                else:
                    movie_data['user_rating'] = "User has not rated this movie."
            else:
                movie_data['user_rating'] = "User is not authenticated."

            return Response(movie_data)
        else:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
 
def movie_list(request):
    # Get all movies
    movieurl = 'http://127.0.0.1:8000/movie/movies/'

    movies = Movie.objects.all()
    render(request, 'movie_list.html')
    # Render the template with the list of movies
    return render(request, 'movie_list.html', {'movies': movies})

# def movie_detail(request, movie_id):
#     # Get the movie by its ID
#     movie = get_object_or_404(Movie, id=movie_id)

#     # Get genres associated with the movie
#     genres = Genre.objects.filter(movie_genre__movie=movie)

#     # Get cast and crew for the movie
#     cast = Cast.objects.filter(movie_id=movie)
#     actors = Actor.objects.filter(id__in=cast.values('actor_id'))
#     characters = Character.objects.filter(id__in=cast.values('character_id'))

#     crew = MovieCrew.objects.filter(movie=movie)
#     crew_members = Crew.objects.filter(id__in=crew.values('crew_id'))

#     # Combine actors and characters into a list of dictionaries
#     actors_characters = [
#         {'actor': actor, 'character': character}
#         for actor, character in zip(actors, characters)
#     ]

#     # Get comments for the movie
#     comments = Comment.objects.filter(movie=movie)

#     # Render the template with the movie data and comments
#     return render(
#         request,
#         'movie_detail.html',
#         {
#             'movie': movie,
#             'genres': genres,
#             'actors_characters': actors_characters,
#             'crew_members': crew_members,
#             'comments': comments,  # Pass comments to the template
#         }
#     )

class MovieViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieListViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]

    queryset = MovieList.objects.all()
    serializer_class = MovieListSerializer

from rest_framework.permissions import IsAuthenticated
class MovieListCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    queryset = MovieList.objects.all()
    serializer_class = MovieListSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Check if the movie list name is restricted
        restricted_names = ["watchlist", "watched_movies"]
        list_name = serializer.validated_data.get("title", "").lower()
        
        if list_name in restricted_names:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({"title": "This list name is not allowed."})
        

        # Proceed with creating the movie list
        serializer.save(user=self.request.user)

class MovieListDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]

    queryset = MovieList.objects.all()
    serializer_class = MovieListSerializer
class VoteView(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = VoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

from rest_framework.generics import ListAPIView
class GenreMovieListView(ListAPIView):
    serializer_class = testGenre

    def get_queryset(self):
        genre_slug = self.kwargs['genre_slug']
        # Assuming you have a 'genres' field in your Movie model
        return Movie.objects.filter(movie_genre__genre__genre_name=genre_slug)


from rest_framework.views import APIView
class MovieListRetrieveAddView(APIView):
    #permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        movie_lists = MovieList.objects.filter(user=request.user)
        serializer = MovieListSerializer(movie_lists, many=True)
        return Response(serializer.data)
    

    def post(self, request, *args, **kwargs):
        movie_list_id = request.data.get('movie_list_id')
        movie_id = request.data.get('movie_id')

        try:
            movie_list = MovieList.objects.get(id=movie_list_id, user=request.user)
            movie = Movie.objects.get(id=movie_id)

            # Check if the movie is already in the list
            if movie in movie_list.movies.all():
                movie_list.movies.remove(movie)
                movie_list.total_time_of_movies -= movie.runtime
                movie_list.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                movie_list.movies.add(movie)
                movie_list.total_time_of_movies += movie.runtime
                movie_list.save()
                return Response(status=status.HTTP_201_CREATED)
            
        except MovieList.DoesNotExist:
            return Response({"error": "Movie list does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        except Movie.DoesNotExist:
            return Response({"error": "Movie does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)    
    

class UsersMovieListView(generics.ListAPIView):
    permission_classes = [AllowAny]

    serializer_class = MovieListSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return MovieList.objects.filter(user=user_id)
    

class MovieCommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        movie_id = self.kwargs.get('movie_id')
        return Comment.objects.filter(movie_id=movie_id)
    def perform_create(self, serializer):
        movie_id = self.kwargs.get('movie_id')
        movie = get_object_or_404(Movie, id=movie_id)
        
        # Use the authenticated user or create an anonymous user
        user = self.request.user if self.request.user.is_authenticated else get_user_model().objects.get_or_create(username='anonymous_user')[0]

        serializer.save(user=user, movie=movie)
    

        

class MovieCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        comment_id = self.kwargs.get('comment_id')
        movie_id = self.kwargs.get('movie_id')

        comment = get_object_or_404(Comment, id=comment_id, movie_id=movie_id)
        return comment
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': 'Comment deleted'}, status=status.HTTP_204_NO_CONTENT)

class MovieRateListCreateView(generics.ListCreateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    permission_classes = [AllowAny]  

    def get_queryset(self):
        movie_id = self.kwargs.get('movie_id')
        return Rate.objects.filter(movie_id=movie_id)

    def perform_create(self, serializer):
        movie_id = self.kwargs.get('movie_id')
        movie = get_object_or_404(Movie, id=movie_id)
        
        # Check if the user is authenticated
        if self.request.user.is_authenticated:
            user = self.request.user
            username = user.username
        else:
            # Create or get an anonymous user
            user, created = get_user_model().objects.get_or_create(username='anonymous_user')
            username = 'anonymous_user'

        # Save the rate with the user
        serializer.save(user=user, movie=movie)

        # Update movie ratings
        movie.vote_count = F('vote_count') + 1
        movie.vote_average = (F('vote_average') * F('vote_count') + serializer.validated_data['rate_point']) / F('vote_count')
        movie.save()
    
class MovieRateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        rate_id = self.kwargs.get('rate_id')
        movie_id = self.kwargs.get('movie_id')

        rate = get_object_or_404(Rate, id=rate_id, movie_id=movie_id)
        return rate
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        movie = instance.movie
        movie.vote_count = F('vote_count') - 1
        movie.vote_average = (F('vote_average') * F('vote_count') - instance.rate_point) / F('vote_count')
        movie.save()

        self.perform_destroy(instance)

        return Response({'status': 'Rate deleted'}, status=status.HTTP_204_NO_CONTENT)
    def perform_update(self, serializer):
        movie_id = self.kwargs.get('movie_id')
        user = self.request.user if self.request.user.is_authenticated else get_user_model().objects.get_or_create(username='anonymous_user')[0]
        current_rate = get_object_or_404(Rate, user=user, movie_id=movie_id)

        # Update the rate
        serializer.save(user=user, movie=current_rate.movie)

        # Update movie vote count and average
        current_movie = current_rate.movie
        current_movie.vote_average = (F('vote_average') * F('vote_count') - current_rate.rate_point + serializer.validated_data['rate_point']) / F('vote_count')
        current_movie.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Movie_Genre
from django.db.models import Q

class MovieListFilterView(APIView):
    
    permission_classes = [AllowAny]
    def post(self, request, list_id, *args, **kwargs):
        try:
            movie_list = MovieList.objects.get(id=list_id)

            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')
            genres = request.data.get('genres')
            actors = request.data.get('actors')
            crews = request.data.get('crews')
            sort_by = request.data.get('sort_by', 'popularity')  # Default sorting by popularity


            # Your existing logic for filtering movies based on start_date, end_date, etc.
            #movies = movie_list.objects.filter(release_date__gte=start_date, release_date__lte=end_date)

            movies = movie_list.movies.all().filter(release_date__gte=start_date, release_date__lte=end_date)

            #print ("movies: " , movies)
            #print ("genres: " , genres)
            # Filter movies based on genres using Movie_Genre model
            if genres:
                genre_ids = Movie_Genre.objects.filter(genre__genre_name__in=genres).values_list('movie_id', flat=True)
                #print ("genre_ids: " , genre_ids)
                movies = movies.filter(id__in=genre_ids)
                #print ("movies: " , movies)

            if actors:
                # Strip whitespace from each actor name and filter out empty strings
                actors = [actor_name.strip() for actor_name in actors if actor_name.strip()]

                # Construct a query to match any actor name that contains any string from the actors list
                if actors:  # Check again in case the list becomes empty after stripping
                    actor_query = Q(actor_name__istartswith=actors[0])
                    for actor_name in actors[1:]:
                        actor_query |= Q(actor_name__istartswith=actor_name)

                    actor_ids = Actor.objects.filter(actor_query).values_list('id', flat=True)
                    cast_movie_ids = Cast.objects.filter(actor_id__in=actor_ids).values_list('movie_id', flat=True)
                    movies = movies.filter(id__in=cast_movie_ids)


            if crews:
    # Strip whitespace from each crew name and filter out empty strings
                crews = [crew_name.strip() for crew_name in crews if crew_name.strip()]

                # Construct a query to match any crew name that contains any string from the crews list
                if crews:  # Check again in case the list becomes empty after stripping
                    crew_query = Q(name__istartswith=crews[0])
                    for crew_name in crews[1:]:
                        crew_query |= Q(name__istartswith=crew_name)

                    crew_ids = Crew.objects.filter(crew_query).values_list('id', flat=True)
                    movie_crew_movie_ids = MovieCrew.objects.filter(crew_id__in=crew_ids).values_list('movie_id', flat=True)
                    movies = movies.filter(id__in=movie_crew_movie_ids)




            if sort_by == 'popularity':
                movies = movies.order_by('-popularity')
            elif sort_by == 'alphabetic':
                movies = movies.order_by('title')
            elif sort_by == 'rating':
                movies = movies.order_by('-vote_average')
            elif sort_by == 'user_rating':
                rates = Rate.objects.filter(movie__in=movies).order_by('-rate_point')
                movies = [rate.movie for rate in rates]
                # Implement your logic for sorting by user rating
                pass
            elif sort_by == 'length':
                movies = movies.order_by('runtime')
            elif sort_by == 'release_date':
                movies = movies.order_by('-release_date')

            # Manually construct the response data
            response_data = []
            for movie in movies:
                movie_data = {
                    'id': movie.id,
                    'imdb_id': movie.imdb_id,
                    'title': movie.title,
                    'poster_path': movie.poster_path,
                    'background_path': movie.background_path,
                    'original_language': movie.original_language,
                    'original_title': movie.original_title,
                    'overview': movie.overview,
                    'release_date': movie.release_date,
                    'runtime': movie.runtime,
                    'vote_average': movie.vote_average,
                    'vote_count': movie.vote_count,
                    'popularity': movie.popularity,
                }
                response_data.append(movie_data)

            return Response(response_data, status=status.HTTP_200_OK)

        except Movie.DoesNotExist:
            return Response({'detail': 'Movie list not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MovieListDeleteView(APIView):
    def delete(self, request, list_id, *args, **kwargs):
        try:
            movie_list = get_object_or_404(MovieList, id=list_id)
            if movie_list.user != request.user:
                return Response({'detail': 'You do not have permission to delete this movie list.'}, status=status.HTTP_403_FORBIDDEN)
            movie_list.delete()
            return Response({'detail': 'Movie list deleted successfully.'}, status=status.HTTP_200_OK)

        except MovieList.DoesNotExist:
            return Response({'detail': 'Movie list not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
