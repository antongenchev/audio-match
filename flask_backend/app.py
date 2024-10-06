from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'message': 'api is working'}), 200