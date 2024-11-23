from flask import Flask, redirect, url_for, request, session, render_template, jsonify
import requests


app = Flask(__name__)

app.secret_key = '3lvKQGLL84O2599qeO21KFqbqYtSQfKb'  # Sin esto no funciona, por favor no tocar.

CLIENT_ID = 'c9f3386b76074211a1a2e478661ea36c'
CLIENT_SECRET = 'd11a3cf5187c41188ab53ebce5ffc8d3'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'

# Constantes para las rutas
AUTHN_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'
SCOPE = 'user-read-email, user-read-private, user-read-recently-played, user-library-read, user-top-read, user-modify-playback-state, app-remote-control, streaming, user-read-playback-state' #alcances. datos a los que la aplicacion tiene acceso

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
    response = requests.post(TOKEN_URL, data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    })
    data = response.json()
    session['access_token'] = data.get('access_token')
    
    return redirect(url_for('profile'))
    
@app.route('/profile')
def profile():
    #Acceder a los datos del perfil del usuario
    headers = {"Authorization": f"Bearer {session['access_token']}"}
    
    #solicitud http de tipo para acceder a los datos de perfil usuario 
    response = requests.get(f"{API_BASE_URL}me", headers=headers)
    
    #se crea una variable que almacenara la respuesta de la api (en formato json). al almacenarse se va a convertir en un diccionario
    user_info = response.json() #Ejemplo de la respuesta de la api: https://developer.spotify.com/documentation/web-api/reference/get-current-users-profile
    
    return render_template("perfilUsuario.html", user_info=user_info)

# Obtener canciones escuchadas recientemente
@app.route('/historial')
def historial():
    
    if 'access_token' not in session:
        return redirect(url_for('login'))
    
    #Acceder a los datos del perfil del usuario
    headers = {"Authorization": f"Bearer {session['access_token']}"}
    
    #Esta variable funciona para especificar cuantas canciones vamos a pedirle a la api, en este caso vamos a pedir la maxima cantidad (50).
    params = {"limit": 50}
    response = requests.get(f"{API_BASE_URL}me/player/recently-played", headers=headers, params=params)
    
    #Verifica que la respuesta de la api sea positiva
    if response.status_code == 200:
        #Convierte el json de la respuesta recibida en un diccionario
        data = response.json()
        
        #Creamos una lista de diccionarios para especificar la informacion que vamos a tomar (artista, cancion, fecha de reproduccion)
        tracks = [
            {
                "track_name": item['track']['name'], 
                "artist_name": ", ".join(artist['name'] for artist in item['track']['artists']), #', '.join usa como separador ", " y dentro de usa iterable usa un ciclo for para obtener los artistas dentro de esa canion
                "played_at": item['played_at']
            }
            for item in data.get('items', [])
            #itera sobre la lista de elementos devuelta json de la api, en caso de que no se hata obtenido nada devolvera una lista vacia

        ]
        #Amigo, track se vuelve una lista de diccionarios (DAMN!!!! he KNOWS PytHON)
        
        return render_template("historial.html", tracks=tracks)
    
    else:
        return f"Error: {response.status_code} - {response.text}"

@app.route('/gustados')
def liked_tracks():
    
    if 'access_token' not in session:
        return redirect(url_for('login'))
    
    # Obtener las últimas 50 canciones en likes
    headers = {"Authorization": f"Bearer {session['access_token']}"}
    params = {"limit": 50}
    response = requests.get(f"{API_BASE_URL}me/tracks", headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        tracks = [
            {
                "track_name": item['track']['name'],
                "artist_name": ", ".join(artist['name'] for artist in item['track']['artists']),
                "album_name": item['track']['album']['name'],
                "added_at": item['added_at']
            }
            for item in data.get('items', [])
        ]
        return render_template("canciones.html", tracks=tracks)
    
    else:
        return f"Error: {response.status_code} - {response.text}"

@app.route('/repifyWawa')
def repify():
    
    if 'access_token' not in session:
        return redirect(url_for('login'))
    
    # Obtener las canciones del historial
    headers = {"Authorization": f"Bearer {session['access_token']}"}
    historial_response = requests.get(f"{API_BASE_URL}me/player/recently-played", headers=headers, params={"limit": 50})
    
    #canciones guardadas
    liked_response = requests.get(f"{API_BASE_URL}me/tracks", headers=headers, params={"limit": 50})
    
    if historial_response.status_code == 200 and liked_response.status_code == 200:
        historial_data = historial_response.json()
        liked_data = liked_response.json()

        #canciones del historial
        historial_tracks = {
            item['track']['id']: {
                "track_name": item['track']['name'],
                "artist_name": ", ".join(artist['name'] for artist in item['track']['artists']),
                "album_name": item['track']['album']['name'],
                "played_at": item['played_at']
            }
            for item in historial_data.get('items', [])
        }

        #canciones guardadas
        liked_tracks = {
            item['track']['id']: {
                "track_name": item['track']['name'],
                "artist_name": ", ".join(artist['name'] for artist in item['track']['artists']),
                "album_name": item['track']['album']['name'],
                "added_at": item['added_at']
            }
            for item in liked_data.get('items', [])
        }
        
        #canciones en las dos listas
        
        #Creamos un cojunto de las claves de diccionarios no repetidas con el metodo set
        common_ids = set(historial_tracks.keys()) & set(liked_tracks.keys())
        
        #recuperamos los valores perdiod en common_ids (Por favor escuchar "I LAY DOWN MY LIFE FOR YOU" DE JPEGMAFIA)
        common_tracks = [historial_tracks[track_id] for track_id in common_ids]

        return render_template("repify.html", tracks=common_tracks)
    
    else:
        return f"Error: {historial_response.status_code} o {liked_response.status_code} - Revisa tus permisos o el token de acceso."

#oBTENER canciones mas escuchadas por el usuario
def get_user_top_tracks(access_token, time_range='medium_term', limit=10):
    url = "https://api.spotify.com/v1/me/top/tracks"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "time_range": time_range,
        "limit": limit
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()['items']
    else:
        return []

@app.route('/tops')
def top_tracks():
    if 'access_token' not in session:
        return redirect(url_for('login'))  # Redirige si no hay token en la sesión

    access_token = session['access_token']
    tracks = get_user_top_tracks(access_token)
    return render_template('top.html', tracks=tracks,  access_token=access_token)

#aqui termina la funcion


@app.route('/play', methods=['POST'])
def play():
    # Obtener los datos enviados desde el frontend (URI de la canción)
    data = request.get_json()
    track_uri = data.get('uri')
    
    access_token = session['access_token']
    
    # Aquí puedes integrar el código para usar el SDK de Spotify o la API para reproducir la canción
    if track_uri:
        # Esto puede ser un ejemplo de una solicitud para reproducir una canción con la API de Spotify
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        # Aquí puedes hacer la solicitud API a Spotify para controlar la reproducción (esto es solo un ejemplo)
        response = requests.put(f'https://api.spotify.com/v1/me/player/play', headers=headers, json={"uris": [track_uri]})
        
        if response.status_code == 204:
            return jsonify({"message": "Track is now playing!"}), 200
        else:
            return jsonify({"error": "Failed to play track."}), 500
    return jsonify({"error": "No track URI provided"}), 400

@app.route('/logout')
def logout():
    
    if 'access_token' not in session:
        return redirect(url_for('login'))
    
    code = request.args.get('code')
    
    # Solicitar el token de acceso
    response = requests.post(TOKEN_URL, data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    })
    
    data = response.json()
    session['access_token'] = data.get('access_token')
    
    session.clear(session['access_token'])
    
    return redirect(url_for("/"))

@app.route("/inicio")
def inicio():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
