from flask import Flask, render_template, request, redirect, url_for, session
import requests
import base64
import json
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

app = Flask(__name__)
app.secret_key = 'dev_key_12345'  # Only for development!
app.config['SESSION_TYPE'] = 'filesystem'

# Mood to playlist mapping (you can customize these with your own playlists)
MOOD_PLAYLISTS = {
    'sadness': [
        {'name': 'Melancholy Melodies', 'id': '37i9dQZF1DX7qK8ma5wgG1'},
        {'name': 'Sad Songs', 'id': '37i9dQZF1DX7qK8ma5wgG1'}
    ],
    'joy': [
        {'name': 'Happy Hits', 'id': '37i9dQZF1DXdPec7aLTmlC'},
        {'name': 'Feel Good', 'id': '37i9dQZF1DX9XIFQuFvzM4'}
    ],
    'surprise': [
        {'name': 'Unexpected Finds', 'id': '37i9dQZF1DX4o1oenSJRJd'},
        {'name': 'Eclectic Mix', 'id': '37i9dQZF1EIh7H4YlZgU2P'}
    ],
    'anger': [
        {'name': 'Rock Workout', 'id': '37i9dQZF1DWXRqgorJj26U'},
        {'name': 'Hard & Heavy', 'id': '37i9dQZF1DX5n5gZBZb0AT'}
    ],
    'neutral': [
        {'name': 'Background Music', 'id': '37i9dQZF1DX4sWSpwq3LiO'},
        {'name': 'Chill Vibes', 'id': '37i9dQZF1DX4WYpdgoIcn6'}
    ],
    'fear': [
        {'name': 'Dark & Stormy', 'id': '37i9dQZF1DX5Ejj0EkURtP'},
        {'name': 'Atmospheric', 'id': '37i9dQZF1DX5trt9i14X7j'}
    ]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    scope = 'user-read-private user-read-email playlist-read-private'
    auth_url = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={scope}"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    
    # Request access token
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://127.0.0.1:5000/callback'
    }
    
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    if response.status_code != 200:
        return "Failed to authenticate with Spotify", 400
    
    session['access_token'] = response.json().get('access_token')
    session['refresh_token'] = response.json().get('refresh_token')
    
    return redirect(url_for('select_mood'))

@app.route('/select_mood', methods=['GET', 'POST'])
def select_mood():
    if 'access_token' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        mood = request.form.get('mood')
        session['selected_mood'] = mood
        return redirect(url_for('show_playlists'))
    
    return render_template('mood.html')

@app.route('/playlists')
def show_playlists():
    if 'access_token' not in session or 'selected_mood' not in session:
        return redirect(url_for('login'))
    
    mood = session['selected_mood']
    playlists = MOOD_PLAYLISTS.get(mood, [])
    
    return render_template('playlist.html', mood=mood, playlists=playlists)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)