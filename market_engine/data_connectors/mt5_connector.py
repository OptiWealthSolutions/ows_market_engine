# data_connectors/mt5_connector.py (concept)
import MetaTrader5 as mt5
import redis
from config.settings import settings # Charger la config

class MT5Connector:
    def __init__(self):
        # Connexion à Redis (le bus de message) [cite: 152]
        self.redis = redis.Redis(host=settings.redis_host) 
        
    def connect_mt5(self):
        # Logique de connexion à MT5 avec les identifiants de settings
        if not mt5.initialize(account=settings.mt5_account):
            print("MT5 connection failed")
            return False
        return True

    def stream_ticks(self):
        # S'abonne aux symboles définis dans TOUTES les stratégies activées
        all_assets = set()
        for s_config in settings.strategies:
            if s_config.enabled:
                all_assets.update(s_config.assets)
        
        for asset in all_assets:
            mt5.symbol_select(asset, True)
            
        print(f"Streaming ticks for: {all_assets}")
        
        while True:
            # Boucle pour récupérer les ticks de MT5
            for asset in all_assets:
                tick = mt5.symbol_info_tick(asset)
                if tick:
                    # 1. Normaliser les données [cite: 134]
                    message = {
                        "type": "tick",
                        "symbol": asset,
                        "ts": tick.time_msc, # Assurer format ISO
                        "bid": tick.bid,
                        "ask": tick.ask
                    } # Conforme au contrat 
                    
                    # 2. Publier sur le bus (Redis Stream) [cite: 158]
                    self.redis.xadd("ticks_stream", message)