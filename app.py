
from flask import Flask, redirect, url_for, request, session, render_template
import requests
import urllib.parse


app = Flask(__name__)

app.secret_key = '3lvKQGLL84O2599qeO21KFqbqYtSQfKb'

CLIENT_ID = 'c9f3386b76074211a1a2e478661ea36c'
CLIENT_SECRET = 'd11a3cf5187c41188ab53ebce5ffc8d3'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'

#constantes para las rutas
AUTHN_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.sportify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'
SCOPE = 'user-library-read'

@app.route('/')
def index():
    return render_template ("login.html")

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

if __name__ == '_main_':
    app.run(debug=True)