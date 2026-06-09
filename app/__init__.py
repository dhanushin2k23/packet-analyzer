from flask import Flask, request, jsonify
from app.services.pcap_parser import analyze_pcap
import os

def create_app():

    app = Flask(__name__)

    @app.route("/upload", methods=["POST"])
    def upload():

        file = request.files.get("file")

        if file is None or file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        filepath = os.path.join("uploads", file.filename)

        file.save(filepath)

        result = analyze_pcap(filepath)

        return jsonify(result)

    return app