from flask import Flask, request, jsonify
import swisseph as swe
import datetime
import os

app = Flask(__name__)
swe.set_ephe_path('')  # Nutzt Standardpfad für Ephemeriden

@app.route('/astro', methods=['POST'])
def calculate():
    data = request.get_json()

    year = int(data['year'])
    month = int(data['month'])
    day = int(data['day'])
    hour = int(data['hour'])
    minute = int(data['minute'])
    latitude = float(data['latitude'])
    longitude = float(data['longitude'])

    jd_ut = swe.utc_to_jd(year, month, day, hour, minute, 0.0)[0]
    sun = swe.calc_ut(jd_ut, swe.SUN)
    moon = swe.calc_ut(jd_ut, swe.MOON)

    return jsonify({
        'julian_day': jd_ut,
        'sun_longitude': sun[0][0],
        'moon_longitude': moon[0][0]
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
