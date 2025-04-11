# api_b.py
from flask import Flask, jsonify

app = Flask(__name__)

# Simulando um banco de dados de temperaturas
weather_data = {
    "SãoPaulo": 25,
    "RioDeJaneiro": 33,
    "Curitiba": 13,
    "Salvador": 29,
    "PortoAlegre": 18
}

@app.route('/weather/<city>', methods=['GET'])
def get_weather(city):
    city_key = city.replace(" ", "")
    temp = weather_data.get(city_key, None)

    if temp is None:
        return jsonify({"error": "Cidade não encontrada"}), 404

    return jsonify({
        "city": city.replace(" ", " "),
        "temp": temp,
        "unit": "Celsius"
    })

if __name__ == '__main__':
    app.run(port=5001)
