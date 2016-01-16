from system.core.model import Model
from flask import Flask, session
from flask.ext.bcrypt import Bcrypt
app = Flask(__name__)
flask_bcrypt = Bcrypt(app)
import re

class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def new_user(self, user_info):
        password = user_info['password']

        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []

        if len(user_info['first_name']) < 1:
            errors.append('First name cannot be blank')
        if len(user_info['last_name']) < 1:
            errors.append('Last name cannot be blank')
        if len(user_info['email']) < 1:
            errors.append('email cannot be blank')
        if not EMAIL_REGEX.match(user_info['email']):
            errors.append('Must enter a valid email')
        if len(user_info['password']) < 8:
            errors.append('Password must be at least 8 characters')
        if user_info['password'] != user_info['pw_confirm']:
            errors.append('Passwords must match')

        if errors:
            return {
            "status" : False,
            "errors" : errors
            }
            print errors['errors']

        else:
            pw_hash = self.bcrypt.generate_password_hash(password)
            registration_query = "INSERT INTO users (first_name, last_name, email, pw_hash, created_at, updated_at) VALUES ('{}', '{}', '{}', '{}', NOW(), NOW())".format(user_info['first_name'], user_info['last_name'], user_info['email'], pw_hash)
            self.db.query_db(registration_query)

            select_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            user = self.db.query_db(select_user_query)
            session['id'] = user[0]['id']

            session['first_name'] = user_info['first_name']
            return{"status" : True}

    def signin(self, login_info):
        password = login_info['password']
        signin_query = "SELECT * FROM users WHERE email='{}' LIMIT 1".format(login_info['email'])

        user = self.db.query_db(signin_query)

        if user != []:
            print self.bcrypt.check_password_hash(user[0]['pw_hash'], password)
            if self.bcrypt.check_password_hash(user[0]['pw_hash'], password):
                session['first_name'] = user[0]['first_name']
                session['id'] = user[0]['id']
                return {"status" : True}
            else:
                return{"status" : False}

        else:
            return{"status" : False}

    def get_songs(self):
        get_songs_query = "SELECT artists.name, songs.title, songs.id FROM songs LEFT JOIN artists ON artists.id = songs.artist_id"
        return self.db.query_db(get_songs_query)

    def get_song_count(self, id):
        print "************"
        print id
        count_query = "SELECT count(song_id) FROM song_playlist WHERE song_id = '{}'".format(id)
        return self.db.query_db(count_query)

    def insert_song(self, new_song_info):
        artist_query = "SELECT * FROM artists WHERE name='{}' LIMIT 1".format(new_song_info['artist'])
        artist = self.db.query_db(artist_query)

        if not artist:
            insert_artist_query = "INSERT INTO artists (name, created_at, updated_at) VALUES ('{}', NOW(), NOW())".format(new_song_info['artist'])
            self.db.query_db(insert_artist_query)

            get_artist_query = "SELECT * FROM artists WHERE name='{}' LIMIT 1".format(new_song_info['artist'])
            artist = self.db.query_db(get_artist_query)

        insert_song_query = "INSERT INTO songs (title, created_at, updated_at, artist_id) VALUES ('{}', NOW(), NOW(), '{}')".format(new_song_info['title'], artist[0]['id'])
        self.db.query_db(insert_song_query)

    def display_song(self, id):
        get_song_query = "SELECT users.id as user_id, users.first_name, users.last_name, songs.id as song_id, songs.title, playlists.id as playlist_id FROM users LEFT JOIN playlists ON users.id = playlists.user_id LEFT JOIN song_playlist ON playlists.id = song_playlist.playlist_id LEFT JOIN songs ON songs.id = song_playlist.song_id WHERE songs.id = '{}' GROUP BY playlist_id".format(id)
        return self.db.query_db(get_song_query)

    def get_playlist(self, id):
        get_playlist_query = "SELECT * FROM song_playlist WHERE song_id = '{}' LIMIT 1".format(id)
        return self.db.query_db(get_playlist_query)

    def get_user_add_count(self, id, playlist_ident):
        get_add_count_query = "SELECT count(song_id) FROM song_playlist WHERE song_id='{}' AND playlist_id='{}'".format(id, playlist_ident)
        return self.db.query_db(get_add_count_query)

    def display_user_playlist(self, user_id):
        get_playlist_query = "SELECT users.first_name, users.last_name, artists.name, songs.title FROM users LEFT JOIN playlists ON users.id = playlists.user_id LEFT JOIN song_playlist ON playlists.id = song_playlist.playlist_id LEFT JOIN songs ON songs.id = song_playlist.song_id LEFT JOIN artists ON artists.id = songs.artist_id WHERE users.id = '{}' GROUP BY songs.title".format(user_id)
        return self.db.query_db(get_playlist_query)

    def playlist_add_count(self, user_id):
        playlist_count_query = "SELECT count(users.id) FROM song_playlist LEFT JOIN users ON users.id = playlists.user_id WHERE users.id = '{}'".format(user_id)
        return self.db.query_db(playlist_count_query)

    def insert_playlist_song(self, id):
        select_song_query = "SELECT * FROM songs WHERE id = '{}'".format(id)
        song = self.db.query_db(select_song_query)

        select_user_query = "SELECT users.id as user_id, playlists.id as playlist_id FROM users LEFT JOIN playlists ON users.id = playlists.user_id WHERE first_name = '{}'".format(session['first_name'])
        user = self.db.query_db(select_user_query)

        insert_playlist_song_query = "INSERT INTO song_playlist (song_id, playlist_id) VALUES ('{}', '{}')".format(song[0]['id'], user[0]['playlist_id'])
        self.db.query_db(insert_playlist_song_query)
