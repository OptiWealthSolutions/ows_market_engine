# core_engine/strategy_runner.py (concept)
import redis
from config.settings import settings
from strategies.strategy_base import StrategyBase
# Importer dynamiquement les classes de stratégies
from strategies.rsi_revert import RSIRevertStrategy 
from strategies.ma_crossover import MACrossoverStrategy

class StrategyRunner:
    def __init__(self):
        self.redis = redis.Redis(...)
        self.strategies = []
        self._load_strategies()

    def _load_strategies(self):
        # Charge les stratégies ACTIVÉES depuis la config
        strategy_map = {
            "rsi_mean_revert": RSIRevertStrategy,
            "ma_crossover": MACrossoverStrategy,
        }
        
        for s_config in settings.strategies:
            if s_config.enabled:
                if s_config.id in strategy_map:
                    strategy_class = strategy_map[s_config.id]
                    # Instancie la stratégie avec sa config
                    instance = strategy_class(
                        strategy_id=s_config.id,
                        assets=s_config.assets,
                        params=s_config.params
                    )
                    self.strategies.append(instance)
                    print(f"Loaded strategy: {s_config.id}")

    def run(self):
        # S'abonne au stream de ticks [cite: 159]
        stream_key = "ticks_stream"
        last_id = '$' # Écoute seulement les nouveaux messages
        
        while True:
            messages = self.redis.xread({stream_key: last_id}, block=5000)
            if messages:
                for _, msg_list in messages:
                    for msg_id, tick_data in msg_list:
                        # Dispatcher le tick à toutes les stratégies chargées
                        for strategy in self.strategies:
                            # La stratégie filtre elle-même les assets
                            signal = strategy.on_tick(tick_data)
                            
                            if signal:
                                # 3. Publier le signal sur le bus [cite: 159]
                                self.redis.xadd("signals_stream", signal)
                        
                        last_id = msg_id