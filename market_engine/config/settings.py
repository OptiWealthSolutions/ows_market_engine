# config/settings.py
from pydantic import BaseModel
from typing import List, Dict

# Configuration pour UNE stratégie
class StrategyConfig(BaseModel):
    id: str             # Identité (ex: "rsi_mean_revert")
    enabled: bool = True  # Pour "activer ou non"
    assets: List[str]   # Les actifs à trader (ex: ["EURUSD", "GBPUSD"])
    params: Dict         # Hyperparamètres (ex: {"rsi_period": 14})
    risk_profile: Dict   # ex: {"max_pos_size": 10000, "max_drawdown_pct": 0.05}

# Configuration globale
class Settings(BaseModel):
    redis_host: str = "redis"
    timescale_db_url: str = "postgresql://user:pass@timescale:5432/trading"
    mt5_account: int = 12345
    mt5_password: str = "SECRET"
    
    # Liste de toutes les stratégies gérées par le moteur
    strategies: List[StrategyConfig] = [
        StrategyConfig(
            id="rsi_mean_revert",
            enabled=True,
            assets=["EURUSD"],
            params={"rsi_period": 14, "buy_threshold": 30},
            risk_profile={"max_pos_size": 5000}
        ),
        StrategyConfig(
            id="ma_crossover",
            enabled=False,
            assets=["EURUSD", "AUDUSD"],
            params={"short_window": 10, "long_window": 50},
            risk_profile={"max_pos_size": 10000, "exposure_limit": 50000}
        ),
    ]

# Instance unique chargée au démarrage
settings = Settings()

