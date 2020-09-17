"""Model forms."""

# Django
from django import forms

# Models
from posts.models import Post, Location, Hashtag, PostProfileTag
from users.models import User
# Utils
import re
from PIL.ExifTags import TAGS


class PostForm(forms.Form):
    """Post model form."""
    caption = forms.CharField(max_length=255)
    people_tag = forms.CharField(max_length=255, required=False)
    location = forms.CharField(required=False)
    photo = forms.ImageField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(PostForm, self).__init__(*args, **kwargs)

    def clean_photo(self):
        """clean the location"""
        ret = {}
        photo = self.cleaned_data['photo']
        info = photo.image.getexif()
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value

        if ret.get('GPSInfo', None):
            self.cleaned_data['photo_gps'] = ret['GPSInfo']

        return photo

    def clean_caption(self):
        """extract the hashtags in the caption"""
        data = self.cleaned_data['caption']
        # hashtags
        regex_hashtags = re.compile(r'#([a-zA-Z0-9]{1,})')
        hashtags_names = regex_hashtags.findall(data)
        if hashtags_names:
            self.cleaned_data['hashtags'] = hashtags_names

        return data

    def clean_people_tag(self):
        """extract people tag in the caption and add to the"""
        caption = self.cleaned_data['caption']
        data = self.cleaned_data['people_tag']
        new_data = []

        if data:
            for username in re.split(r'[,\s\n\r\-]', data):
                if User.objects.filter(username=username).exists() and self.request.user.username != username:
                    new_data.append(username)
        # people from caption
        regex_people = re.compile(r'@([a-zA-Z0-9]{1,})')
        people_usernames = regex_people.findall(caption)
        if people_usernames:
            for people_username in people_usernames:
                if User.objects.filter(
                        username=people_username).exists() and self.request.user.username != people_username:
                    new_data.append(people_username)

        return new_data

    def clean_location(self):
        """Extract al the location"""
        data = self.cleaned_data['location']
        regex_location = re.compile(r'[\w\s]{2,},?[\w\s]{2,}')
        if not regex_location.match(data):
            return None

        return data

    def save(self):
        """create the post, hashtags and locations"""
        data = self.cleaned_data
        # save hashtag
        hashtags = []
        if data.get('hashtags', None):
            for hashtag_name in data['hashtags']:
                hashtag = Hashtag.objects.filter(name=hashtag_name)
                if hashtag:
                    hashtags.append(hashtag)
                else:
                    hashtag = Hashtag(name=hashtag_name)
                    hashtag.save()
                    hashtags.append(hashtag)

        # save location

        if data.get('location', None):
            data_location = {
                'name': data['location'],
                'coordinates': data['location']
            }
            location = Location.objects.create(**data_location)
        else:
            location = None

        # save post

        data_post = {
            'user': self.request.user,
            'profile': self.request.user.profile,
            'caption': data['caption'],
            'photo': data['photo'],
            'location': location
        }
        post = Post.objects.create(**data_post)
        if hashtags:
            for hashtag in hashtags:
                post.tags.add(hashtag)
            post.save()

        # save people_tag
        if data.get('people_tag', None):
            for username in data['people_tag']:
                data_post_profile_tag = {
                    'profile': User.objects.get(username=username).profile,
                    'post': post
                }
                PostProfileTag.objects.create(**data_post_profile_tag)
