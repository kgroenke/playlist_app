from system.core.controller import *
from flask import Flask, session
from flask.ext.bcrypt import Bcrypt
app = Flask(__name__)
flask_bcrypt = Bcrypt(app)
import re

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('User')

    def index(self):
        return self.load_view('index.html')

    def create_user(self):
        user_info = {
            "first_name" : request.form.get('first_name'),
            "last_name" : request.form.get('last_name'),
            "email" : request.form.get('email'),
            "password" : request.form.get('password'),
            "pw_confirm" : request.form.get('pw_confirm')
        }
        create_status = self.models['User'].new_user(user_info)
        if create_status['status'] == True:
            return redirect('/songs')
        else:
            for message in create_status['errors']:
                flash(message)
                # flash(create_status['errors'])
            return redirect('/')

    def display_songs(self):
        songs_info = self.models['User'].get_songs()
        count_arr = {}
        for song in songs_info:
            id = song['id']
            songs_count = self.models['User'].get_song_count(id)
            count_arr.update({song['id'] : songs_count[0]['count(song_id)']})
        return self.load_view('display_songs.html', songs_info=songs_info, count_arr=count_arr)

    def login(self):
        login_info = {
            "email" : request.form.get('email'),
            "password" : request.form.get('password')
        }
        login_status = self.models['User'].signin(login_info)
        print login_status

        if login_status['status'] == True:
            return redirect('/songs')
        else:
            invalid = "Error: invalid username or password"
            flash(invalid)
            return redirect('/')

    def logout(self):
        session.clear()
        return redirect('/')

    def add_playlist_song(self, id):
        self.models['User'].insert_playlist_song(id)
        return redirect('/songs')

    def add_song(self):
        new_song_info = {
            "artist" : request.form.get('artist'),
            "title" : request.form.get('title')
        }
        self.models['User'].insert_song(new_song_info)
        return redirect('/songs')

    def display_song_info(self, id):
        count_arr = {}
        song_info = self.models['User'].display_song(id)
        print song_info
        ind_count_arr = {}
        playlists = self.models['User'].get_playlist(id)


        for playlist in playlists:
            playlist_ident = playlists[0]['playlist_id']
            results = self.models['User'].get_user_add_count(id, playlist_ident)
            count_arr.update({playlist_ident : results[0]['count(song_id)']})

        return self.load_view('display_song_info.html', song_info=song_info, count_arr=count_arr)

    def display_user(self, user_id):
        playlist_info = self.models['User'].display_user_playlist(user_id)
        count = self.models['User'].playlist_add_count(user_id)
        print "######"
        print count
        return self.load_view('display_user.html', playlist_info=playlist_info)
