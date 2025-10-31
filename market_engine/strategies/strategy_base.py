# strategies/strategy_base.py

# Ceci est l'interface que toutes vos stratégies doivent implémenter
# [cite: 183-187]
class StrategyBase:
    def __init__(self, strategy_id: str, assets: List[str], params: Dict):
        # Chaque stratégie connaît son identité et sa config
        self.strategy_id = strategy_id
        self.assets = assets
        self.params = params

    def on_start(self, env):
        # 'env' peut être un objet pour accéder aux données historiques, etc.
        pass

    def on_tick(self, tick_data):
        # tick_data sera un dict (voir contrat JSON )
        # C'est ici que la stratégie génère un signal ou non
        # IMPORTANT: La stratégie ne fait que RENVOYER un signal
        # Elle ne l'exécute pas, n'appelle pas d'API [cite: 188]
        
        # Exemple de logique :
        # if tick_data['symbol'] not in self.assets:
        #    return None
        #
        # ... calculs ...
        #
        # if condition_achat:
        #    return {
        #        "type": "signal",
        #        "strategy": self.strategy_id, # <- L'identité !
        #        "symbol": tick_data['symbol'],
        #        "side": "BUY",
        #        "score": 0.85 
        #    } # Correspond au contrat JSON [cite: 167]
        pass

    def on_bar(self, bar_data):
        pass

    def on_signal_ack(self, ack_data):
        # Confirmation que le signal a été reçu (ou rejeté)
        pass