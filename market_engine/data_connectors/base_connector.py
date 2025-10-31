import time
import redis
import yfinance as yf
from datetime import datetime
from config.settings import SETTINGS

REDIS_CLIENT = redis.Redis(host=SETTINGS.redis_host, port=SETTINGS.redis_port)
STREAM_KEY = "ticks_stream" # Nom du canal de communication 

def get_active_assets():
    """Récupère tous les actifs uniques à trader parmi les stratégies activées."""
    assets = set()
    for s_config in SETTINGS.strategies:
        if s_config.enabled:
            assets.update(s_config.assets)
    return list(assets)

def start_streamer():
    print("--- Démarrage du Data Connector (yfinance) ---")
    active_assets = get_active_assets()
    if not active_assets:
        print("Aucun actif à trader. Arrêt du connecteur.")
        return

    print(f"Streaming les données pour : {active_assets}")

    while True:
        for asset in active_assets:
            try:
                # Utilisation de yfinance pour simuler une donnée en temps réel
                ticker = yf.Ticker(asset)
                # Nous récupérons le dernier prix (pour simuler un tick)
                data = ticker.info 
                
                # Simuler le format de tick [cite: 51-52]
                price = data.get('currentPrice') or data.get('previousClose')
                
                if price is not None:
                    # Envoi au stream Redis
                    message = {
                        "type": "tick",
                        "symbol": asset,
                        "ts": datetime.utcnow().isoformat() + "Z", # Timestamp ISO 8601
                        "bid": price,
                        "ask": price * 1.0001 # Simuler un spread
                    }
                    
                    # Publier sur le stream (xadd)
                    REDIS_CLIENT.xadd(STREAM_KEY, {"data": json.dumps(message)})
                    print(f"Pushed Tick: {asset} @ {price}")

            except Exception as e:
                print(f"Erreur lors de la récupération de {asset}: {e}")

        # Pause pour simuler un intervalle entre les ticks (1 seconde)
        time.sleep(1) 

if __name__ == "__main__":
    import json
    start_streamer()