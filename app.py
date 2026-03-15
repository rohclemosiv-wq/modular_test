# -*- coding: utf-8 -*-
"""
Flask async API entry point
"""

from flask import Flask, request, jsonify
import os
from utils import get_address_coordinates
from coverage_service import CoverageService
import logging
CSV_FILENAME = '2018-01-sites-mobiles-2g-3g-4g-france-metropolitaine-l93-ver2-1-.csv'
csv_path = os.path.join(os.path.dirname(__file__), CSV_FILENAME)
service = CoverageService(csv_path)
app = Flask(__name__)

@app.route("/coverage", methods=["POST"])
async def coverage():
    """
    Async endpoint handling address lookup and coverage
    """
    global service
    if not request.is_json:
        return jsonify({"error": "Invalid content type, expecting application/json"}), 400
    
    payload = request.get_json()
    if not isinstance(payload, dict):
        return jsonify({"error": "Payload must be a JSON object mapping ids to addresses"}), 400
    
    result = {}
    for identifier, address in payload.items():
        try:
            lon, lat = await get_address_coordinates(address)
            # print(f"coordinates : ({lon},{lat})")
            coverage = service.get_nearest_coverage(lon, lat)
            result[identifier] = coverage
        except Exception as e:
            result[identifier] = {"error": str(e)}
    
    return jsonify(result)

logging.basicConfig(level=logging.INFO)
logging.info("Flask async coverage service starting")
if __name__ == "__main__":
    # Development server – use a proper WSGI server in production.
    app.run(host="0.0.0.0", port=5000, debug=True)
