from flask import Flask, request
from scapy.all import rdpcap
import os

def create_app():
    app = Flask(__name__)

    @app.route("/upload",methods=["POST"])
    def upload():
        file = request.files.get("file")

        if file is None:
            return "No file uploaded."
        
        filepath = os.path.join("uploads", file.filename)
        file.save(filepath)

        packets = rdpcap(filepath)
        for packets in packets:
            print(packets[0].summary())
        print(packets)

        return f"{file.filename} uploaded successfully."

    return app