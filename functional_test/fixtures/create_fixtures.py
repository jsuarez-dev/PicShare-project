""" This script create all the fixtures data for the functional test"""
# Data lib
import json
import csv
import random
import string
# Time
from datetime import datetime
import time
# OS libraries
import os
import shutil
# Log configuration
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def random_n_int_number(n):
    str_num = ''
    for i in range(n):
        num = random.randint(0, 9)
        str_num += str(num)

    return str_num


def random_about(n):
    """
    This function create a random about, it's base it in
    https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
    :return: str[N]
    """
    about = """Lorem Ipsum is simply dummy text of the printing and typesetting
    industry. Lorem Ipsum has been the industry's standard dummy text ever
    since the 1500s, when an unknown printer took a galley of type and scrambled
    it to make a type specimen book. It has survived not only five centuries,
    but also the leap into electronic typesetting, remaining essentially unchanged.
    It was popularised in the 1960s with the release of Letraset sheets containing Lorem
    Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker
    including versions of Lorem Ipsum. """
    while n > len(about):
        about += about

    return about[:n]


def str_time_prop(start, end, format, prop):
    """
    This function create a random date, it's base it in
    https://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates
    :return: str[N]
    """
    start_time = time.mktime(time.strptime(start, format))
    end_time = time.mktime(time.strptime(end, format))
    selected_time = start_time + prop * (end_time - start_time)

    return datetime.fromtimestamp(time.mktime(time.localtime(selected_time)))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%d/%m/%Y', prop)


def get_random_phone_number():
    result_str = ''.join(str(random.randint(0, 9)) for i in range(8))
    return '+61-04' + result_str


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def save_in_json(data_list, path, filename):
    with open(path + filename, 'w') as fp:
        json.dump(data_list, fp, indent=4)


def create_user_and_profile(username, pk, img_number):
    date_joined = random_date("1/1/2019", "31/12/2019", random.random())

    data_user = {
        "model": "users.user",
        "pk": pk,
        "fields": {
            "password": "pbkdf2_sha256$180000$8p4oybBJgJyb$6mDkGp7SschLUF0dk23yg7ntgI+4u+QK2RA9kdThoiA=",
            "last_login": random_date("1/1/2020", "1/2/2020", random.random()).isoformat() + 'Z',
            "is_superuser": False,
            "username": username,
            "first_name": get_random_string(8),
            "last_name": get_random_string(8),
            "is_staff": False,
            "is_active": True,
            "date_joined": date_joined.isoformat() + 'Z',
            "email": username + "@test.com",
            "is_verified": True,
            "phone_number": get_random_phone_number(),
            "birthday": random_date("1/1/1980", "1/1/1992", random.random()).date().isoformat(),
            "groups": [],
            "user_permissions": []
        }
    }

    data_profile = {
        "model": "users.profile",
        "pk": pk,
        "fields": {
            "user": pk,
            "website": "https://{}.com".format(username),
            "biography": random_about(500),
            "picture": "users/pictures/img_test.{}.png".format(str(img_number).zfill(3)),
            "gender": "R",
            "created": date_joined.isoformat() + 'Z',
            "modified": date_joined.isoformat() + 'Z'
        }
    }
    return [data_user, data_profile]


def create_hashtag(pk, name):
    hashtag = {
        "model": "posts.hashtag",
        "pk": pk,
        "fields": {
            "name": name
        }
    }

    return hashtag


def create_post_profile_tag(pk, profile_pk, post_pk):
    person_tag = {
        "model": "posts.postprofiletag",
        "pk": pk,
        "fields": {
            "profile": profile_pk,
            "post": post_pk
        }
    }

    return person_tag


def create_location(pk, place):
    location_data = {
        "model": "posts.location",
        "pk": pk,
        "fields": {
            "name": place,
            "coordinates": place
        }
    }

    return location_data


def create_post(pk, caption, pk_user, pk_profile, img_number, tags_pk_list, locations_pk):
    post = {
        "model": "posts.post",
        "pk": pk,
        "fields": {
            "user": pk_user,
            "profile": pk_profile,
            "caption": caption,
            "photo": "posts/photos/img_test.{}.png".format(str(img_number).zfill(3)),
            "created": datetime.now().isoformat() + 'Z',
            "modified": datetime.now().isoformat() + 'Z',
            "tags": tags_pk_list,
            "location": locations_pk
        }
    }

    return post


def create_hashtags_dic(number_of_items, list_items, items_used, data):
    list_of_pk = []
    list_uid = random_list_of_int(number_of_items, 0, len(list_items) - 1)
    for uid in list_uid:
        name = list_items[uid]
        if name in items_used.keys():
            list_of_pk.append(items_used[name])
        else:
            pk = max(items_used.values() or [0]) + 1
            # save in the main dic
            data.append(create_hashtag(pk, name))
            # save in local dic
            items_used[name] = pk
            # save pk
            list_of_pk.append(pk)
            pk += 1

    return list_of_pk


def create_location_dic(list_items, items_used, data):
    l_id = random.randint(0, len(list_items) - 1)
    name = list_items[l_id]

    if name in items_used.keys():
        return items_used[name]
    else:
        pk = max(items_used.values() or [0]) + 1
        # save in the main dic
        data.append(create_location(pk, name))
        # save in local dic
        items_used[name] = pk

        return pk


def random_list_of_int(n, min_n, max_in):
    order = []
    i = 0
    while i < n:
        temp = random.randint(min_n, max_in)
        if temp not in order:
            order.append(temp)
            i += 1

    return order


def create_usernames(number_of_users):
    usernames = []
    i = 0
    while i < number_of_users:
        username = 'robot.{}'.format(random_n_int_number(3))
        if username not in usernames:
            usernames.append(username)
            i += 1

    return usernames


def save_username_and_passwd(usernames, path, filename):
    with open(path + filename, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['username', 'password'])
        for username in usernames:
            writer.writerow([username, '123456789'])


def create_post_profile_tag_dic(number_of_people_tag, username, usernames, pk_post, pk_post_profile_tag, data):
    for i in range(0, number_of_people_tag):
        if usernames[i] != username:
            data.append(create_post_profile_tag(pk_post_profile_tag, i + 1, pk_post))


def check_img_files(origin, destiny):
    """check all teh images files"""
    if os.path.isdir(origin) and os.path.isdir(destiny):
        list_images = os.listdir(origin)
        if list_images:
            list_images_in_destiny = os.listdir(destiny)
            images_to_copy = [file for file in list_images if file not in list_images_in_destiny]
            if images_to_copy:
                for img in images_to_copy:
                    shutil.copy(origin + img, destiny)
                    logger.info('{} copy to {}'.format(img, destiny))
        else:
            logger.error('There are not images in the flooder {}'.format(origin))
    else:
        logger.error('The flooder {} does not exist'.format(origin))
        logger.error('Or the flooder {} does not exist'.format(destiny))


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__)) + '/'
    main_path = os.path.dirname(os.path.dirname(base_dir))
    # posts
    post_img_origin = os.path.join(base_dir, 'img/posts/')
    post_img_destiny = os.path.join(main_path, 'media/posts/photos/')
    check_img_files(post_img_origin, post_img_destiny)
    # profile
    profile_img_origin = os.path.join(base_dir, 'img/profile/')
    profile_img_destiny = os.path.join(main_path, 'media/users/pictures/')
    check_img_files(profile_img_origin, profile_img_destiny)

    locations = ['Orlando, Florida', 'Rome, Italy', 'Tel Aviv, Israel', 'Hamburg, Germany', 'Milan, Italy',
                 'Barcelona, Spain', 'Atlanta, Georgia', 'Seoul, South Korea', 'Tokyo, Japan', 'Singapore, Singapore']

    hashtags = ['love', 'instagood', 'photooftheday', 'fashion', 'beautiful', 'happy', 'cute', 'tbt', 'like4like',
                'followme', 'picoftheday', 'follow', 'me', 'selfie', 'summer', 'art', 'instadaily', 'friends', 'repost',
                'nature', 'girl', 'fun', 'style', 'smile', 'food', 'instalike', 'likeforlike', 'family', 'travel',
                'fitness', 'igers', 'tagsforlikes', 'follow4follow', 'nofilter', 'life', 'beauty', 'amazing',
                'instamood', 'instagram', 'photography']

    number_of_users = 5
    number_of_post = 4

    data = []
    # Global PK
    pk_user = 1
    pk_post_profile_tag = 1
    pk_post = 1
    pk_location = 1
    pk_hashtag = 1

    hashtags_used = {}  # {'name': pk}
    location_used = {}  # {'name': pk}
    usernames = create_usernames(5)

    for username in usernames:

        user_data = create_user_and_profile(username, pk_user, pk_user)
        # list of post
        order = random_list_of_int(number_of_post, 1, 12)

        for post in range(0, number_of_post):
            # meta data about the post
            # people tag
            number_of_people_tag = random.randint(0, len(usernames) - 1)
            # locations
            if_locations = random.randint(0, 1)
            locations_pk = None
            # tags
            number_of_hashtags = random.randint(0, 10)
            hashtags_post_pk_list = []  # [pk_1, pk_2 , ...]
            # create hashtags
            if number_of_hashtags > 0:
                hashtags_post_pk_list = create_hashtags_dic(number_of_hashtags, hashtags, hashtags_used, data)
            # create locations
            if if_locations > 0:
                locations_pk = create_location_dic(locations, location_used, data)

            data.append(
                create_post(pk_post, 'me {}'.format(username), user_data[0]['pk'], user_data[1]['pk'], order[post],
                            hashtags_post_pk_list, locations_pk)
            )

            if number_of_people_tag > 0:
                create_post_profile_tag_dic(number_of_people_tag, username, usernames, pk_post, pk_post_profile_tag,
                                            data)
                pk_post_profile_tag += 1

            pk_post += 1
        data += user_data
        pk_user += 1

    save_in_json(data, base_dir, 'data.json')
    save_username_and_passwd(usernames, base_dir, 'user_info.csv')
