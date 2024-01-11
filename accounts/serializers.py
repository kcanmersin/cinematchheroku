from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import Follower, UserProfile

# class FollowerSerializer(serializers.ModelSerializer):
#     user = serializers.DictField(child=serializers.CharField(), source='get_user_info', read_only=True)
#     is_followed_by = serializers.DictField(child=serializers.CharField(), source='get_is_followed_by_info', read_only=True)

#     class Meta:
#         model = Follower
#         fields = ('user', 'is_followed_by')
#         read_only_fields = ('user', 'is_followed_by')

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         if data.get('user') and data.get('is_followed_by'):
# #            print(data)
#             #data['user']['profile_photo'] = instance.user.profile_photo.url if instance.user.profile_photo else None
#             return data
#         return None
from rest_framework import serializers
from .models import Follower

class FollowerSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    is_followed_by = serializers.SerializerMethodField()

    class Meta:
        model = Follower
        fields = ('user', 'is_followed_by')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data.get('user') and data.get('is_followed_by'):
            return data
        return None

    def get_user(self, instance):
        user = instance.user
        user_profile = user.profile.first()  

        return {
            'id': user.id,
            'username': user.username,
            'profile_picture': self.context['request'].build_absolute_uri(user_profile.profile_picture.url) if user_profile and user_profile.profile_picture else None,
        }

    def get_is_followed_by(self, instance):
        is_followed_by = instance.is_followed_by
        is_followed_by_profile = is_followed_by.profile.first()  # Access the UserProfile directly

        return {
            'id': is_followed_by.id,
            'username': is_followed_by.username,
            'profile_picture': self.context['request'].build_absolute_uri(is_followed_by_profile.profile_picture.url) if is_followed_by_profile and is_followed_by_profile.profile_picture else None,
        }


class UserProfileSerializer(serializers.ModelSerializer):

    match_rate = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    profile_picture_url = serializers.SerializerMethodField()
    best_matched_movie_poster = serializers.SerializerMethodField()
    watched_movie_count = serializers.SerializerMethodField()
    follow_status = serializers.SerializerMethodField()


    class Meta:
        model = UserProfile
        fields = '__all__'

    def get_follow_status(self, obj):
        current_user_profile = self.context['request'].user.profile.first()
        if current_user_profile:
            return current_user_profile.get_follow_status(obj.user)
        return False

    def get_watched_movie_count(self, obj):
#        current_user_profile = self.context['request'].user.profile.first()
        current_user_profile = obj.user.profile.first()
        if current_user_profile:
            # print(current_user_profile)
            return current_user_profile.get_watched_movie_count()
        return 0

    def get_best_matched_movie_poster(self, obj):
        current_user_profile = self.context['request'].user.profile.first()
        if current_user_profile:
            return current_user_profile.best_matched_movie_poster(obj.user)
        return None

    def get_match_rate(self, obj): # That is looking through user profile
        current_user_profile = self.context['request'].user.profile.first()  # Get the first profile 
        # print(current_user_profile)
        # print(" self.context['request']: " , self.context['request'].user.profile.first())
        # print("obj: ", obj)
        if current_user_profile:
            return current_user_profile.calculate_match_rate(obj)
    
    def get_follower_count(self, obj):
        current_user_profile = self.context['request'].user.profile.first()  # Get the first profile
        if current_user_profile:
            return current_user_profile.get_followers_count(obj.user)
        return 0
    
    def get_following_count(self, obj):
        current_user_profile = self.context['request'].user.profile.first()
        if current_user_profile:
            return current_user_profile.get_following_count(obj.user)
        return 0
    
    def get_profile_picture_url(self, obj):
        if obj.profile_picture:
            return self.context['request'].build_absolute_uri(obj.profile_picture.url)
        return None
    
    
class ChangeProfilePhotoSerializer(serializers.Serializer):
    profile_picture = serializers.ImageField()

    class Meta:
        model = UserProfile
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()
        return instance
    