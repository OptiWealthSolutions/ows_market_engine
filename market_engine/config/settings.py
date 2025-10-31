from pydantic import BaseModel
from typing import List, Dict

# --- Modèles de Configuration ---

class RiskProfile(BaseModel):
    """Profil de risque spécifique à la stratégie."""
    max_pos_size: int = 10000        # Taille max de position (pour le sizing)
    max_drawdown_pct: float = 0.05   # Max drawdown autorisé
    exposure_limit: int = 50000      # Limite d'exposition totale
    
# [cite: 7] Paramètres stratégiques (stratégies, hyperparamètres)
class StrategyConfig(BaseModel):
    """Configuration et identité pour une stratégie unique."""
    id: str                         # Identité unique (ex: "rsi_mean_revert")
    enabled: bool = True            # Activation/Désactivation rapide
    assets: List[str]               # Actifs que cette stratégie a le droit de trader
    params: Dict                    # Hyperparamètres spécifiques
    risk_profile: RiskProfile       # Votre idée d'aversion au risque différente

# [cite: 8] Connexions brokers / comptes
class Settings(BaseModel):
    """Configuration Globale de l'Engine."""
    # Messaging (Bus de signaux)
    redis_host: str = "redis"
    redis_port: int = 6379
    
    # Database
    timescale_db_url: str = "postgresql://user:pass@timescale:5432/trading"
    
    # Strategy configuration
    strategies: List[StrategyConfig] = [
        StrategyConfig(
            id="rsi_mean_revert",
            enabled=True,
            assets=["EURUSD", "GBPUSD"],
            params={"rsi_period": 14, "buy_threshold": 30, "sell_threshold": 70},
            risk_profile=RiskProfile(max_pos_size=5000, max_drawdown_pct=0.03)
        ),
        StrategyConfig(
            id="ma_crossover",
            enabled=False, # Désactivée par défaut
            assets=["AUDUSD"],
            params={"short_window": 10, "long_window": 50},
            risk_profile=RiskProfile(max_pos_size=20000, max_drawdown_pct=0.08)
        ),
    ]

# Instance unique chargée au démarrage de chaque module
SETTINGS = Settings()