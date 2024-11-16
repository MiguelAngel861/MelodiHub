from flask import Flask, render_template
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

@app.route('/')
def Inicio():
    return render_template("Inicio.html")