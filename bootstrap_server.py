from flask import Flask, request, jsonify
import threading
import time

app = Flask(__name__)

# Store peer and resource information
peers = {}
resources = {}

# Announce the current peers in the network for new nodes attempting to connect
@app.route("/announce", methods=["POST"])
def announce():
    """
    A peer calls /announce with:
    {
        "ip": "127.0.0.1",
        "port": 6001,
        "resources": ["file1.txt", "img.jpg"]
    }
    """
    data = request.json
    node_id = f"{data['ip']}:{data['port']}"

    # Save or update the peer
    peers[node_id] = {
        "resources": data.get("resources", [])
    }

    print(f"[BOOTSTRAP] New peer announced: {node_id}")

    # Build resource index: { "filename": ["ip:port", ...] }
    resource_index = {}
    for peer, info in peers.items():
        for res in info["resources"]:
            resource_index.setdefault(res, []).append(peer)

    # Send back peers + resource index
    return jsonify({
        "status": "ok",
        "peers": list(peers.keys()),
        "resources": resource_index
    })