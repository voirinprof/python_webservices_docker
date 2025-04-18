from flask import Flask, request, jsonify

app = Flask(__name__)

# Random data
POINTS = [
    {"name": "Point_A", "value": 50, "coordinates": [-73.935, 40.730]},
    {"name": "Point_B", "value": 75, "coordinates": [2.352, 48.856]},
    {"name": "Point_C", "value": 20, "coordinates": [-0.127, 51.507]},
    {"name": "Point_D", "value": 90, "coordinates": [139.691, 35.689]},
    {"name": "Point_E", "value": 30, "coordinates": [151.209, -33.868]}
]

def to_geojson_feature(point):
    """Convert in a GeoJSON Feature."""
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": point["coordinates"]
        },
        "properties": {
            "name": point["name"],
            "value": point["value"]
        }
    }

@app.route("/points", methods=["GET"])
def get_points():
    """Return all points (GeoJSON FeatureCollection)."""
    try:
        feature_collection = {
            "type": "FeatureCollection",
            "features": [to_geojson_feature(point) for point in POINTS]
        }
        return jsonify(feature_collection)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/points/filter", methods=["POST"])
def filter_points():
    """Filter all points according the criteria."""
    try:
        # Check if body is in JSON
        if not request.is_json:
            return jsonify({"error": "Request body must be JSON"}), 400

        # Get the criteria
        filters = request.get_json()
        min_value = filters.get("min_value")
        name_contains = filters.get("name_contains")

        # Filter all points
        filtered_points = POINTS
        if min_value is not None:
            try:
                min_value = int(min_value)
                filtered_points = [p for p in filtered_points if p["value"] >= min_value]
            except (ValueError, TypeError):
                return jsonify({"error": "min_value must be an integer"}), 400

        if name_contains:
            name_contains = str(name_contains).lower()
            filtered_points = [p for p in filtered_points if name_contains in p["name"].lower()]

        # Convert in GeoJSON
        feature_collection = {
            "type": "FeatureCollection",
            "features": [to_geojson_feature(point) for point in filtered_points]
        }
        return jsonify(feature_collection)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)