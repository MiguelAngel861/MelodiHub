from flask import Flask, redirect, url_for, request, session, render_template
import requests
import urllib.parse

app = Flask(__name__)

app.secret_key = '3lvKQGLL84O2599qeO21KFqbqYtSQfKb'  # Sin esto no funciona, por favor no tocar.

CLIENT_ID = 'c9f3386b76074211a1a2e478661ea36c'
CLIENT_SECRET = 'd11a3cf5187c41188ab53ebce5ffc8d3'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'

# Constantes para las rutas
AUTHN_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'
SCOPE = 'user-library-read, user-read-recently-played'

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/login')
def login():
    # Redireccionar al usuario a la página de autorización de Spotify
    auth_url = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    # Obtener el código de autorización de la URL
    code = request.args.get('code')
    # Solicitar el token de acceso
    token_url = "https://accounts.spotify.com/api/token"
    response = requests.post(token_url, data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    })
    data = response.json()
    session['access_token'] = data.get('access_token')
    # Redireccionar a una página después del login
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    # Acceder a los datos del perfil del usuario
    headers = {"Authorization": f"Bearer {session['access_token']}"}
    response = requests.get("https://api.spotify.com/v1/me", headers=headers)
    user_info = response.json()
    return f"Bienvenido, {user_info['display_name']}!"

@app.route('/historial')
def Historial():
    #canciones escuchadas la persiona
    headers = {"Authorization": f"Bearer {session['access_token']}"}
    params = {"limit": 50}
    response = requests.get("https://api.spotify.com/v1/me/player/recently-played", headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        tracks = [
            {
                "track_name": item['track']['name'],
                "artist_name": ", ".join(artist['name'] for artist in item['track']['artists']),
                "played_at": item['played_at']
            }
            for item in data.get('items', [])
        ]
        return render_template("historial.html", tracks=tracks)
    else:
        return f"Error: {response.status_code} - {response.text}"

if __name__ == '__main__':
    app.run(debug=True)
