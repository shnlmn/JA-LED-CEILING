#!/usr/bin/env python3
import os
from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='web_interface')

@app.route('/')
def index():
    # Serve the main page
    return send_from_directory('web_interface', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    # Serve any other static files (JS, CSS)
    return send_from_directory('web_interface', filename)

if __name__ == '__main__':
    # Launch the Flask development server on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)

