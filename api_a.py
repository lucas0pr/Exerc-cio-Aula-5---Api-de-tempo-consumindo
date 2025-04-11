# api_a.py
from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

API_B_URL = "http://localhost:5001/weather/{}"

# Cache simples (cidade -> (resposta, timestamp))
cache = {}

CACHE_TIMEOUT = 300  # 5 minutos

def get_cached_weather(city):
    """Verifica se a resposta está no cache e ainda é válida"""
    if city in cache:
        data, timestamp = cache[city]
        if time.time() - timestamp < CACHE_TIMEOUT:
            return data
    return None

@app.route('/recommendation/<city>', methods=['GET'])
def get_recommendation(city):
    # Verificando se temos um cache válido
    cached_data = get_cached_weather(city)
    if cached_data:
        weather = cached_data
        print(f"Usando dados do cache para {city}.")
    else:
        try:
            # Requisição à API B
            response = requests.get(API_B_URL.format(city))
            if response.status_code == 404:
                return jsonify({"error": f"Cidade '{city}' não encontrada na API B."}), 404
            elif response.status_code != 200:
                return jsonify({"error": "Erro ao acessar a API B."}), 500

            # Armazenando resposta no cache
            weather = response.json()
            cache[city] = (weather, time.time())
            print(f"Obtendo dados ao vivo para {city}.")

        except requests.RequestException as e:
            return jsonify({"error": f"Erro na requisição à API B: {str(e)}"}), 500

    # Processando a recomendação com base na temperatura
    temp = weather['temp']

    if temp > 30:
        recommendation = "Está bem quente! Hidrate-se e use protetor solar."
    elif 15 < temp <= 30:
        recommendation = "O clima está agradável. Aproveite o dia!"
    else:
        recommendation = "Está frio! Use um casaco."

    return jsonify({
        "city": weather["city"],
        "temperature": f"{temp}°C",
        "recommendation": recommendation
    })

if __name__ == '__main__':
    app.run(port=5000)
