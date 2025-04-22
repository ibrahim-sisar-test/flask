import requests
from flask import Flask, jsonify, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/ip')
def get_ip_info():
    ip = request.remote_addr
    try:
        res = requests.get(f"https://ipinfo.io/{ip}/json")
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": "Could not fetch IP info", "details": str(e)})

if __name__ == '__main__':
     port = int(os.environ.get("PORT", 5000))  # Railway سيحدد البورت المناسب تلقائيًا
     app.run(host='0.0.0.0', port=port, debug=True)
