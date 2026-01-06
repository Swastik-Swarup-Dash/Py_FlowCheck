@dataclass
class Config:


    env: Environment = "dev"
    sample_size: float = 0.1
    mode:  Mode = "raise"


    def __post_init__(self):
        """Validating config values"""
        if not 0.0 <= self.sample_size<= 1.0:
            raise ValueError("Sample must be between 0.0 and 1.0")
        if self.env not in ["dev","staging","prod"]:
            raise ValueError("Environment must be 'dev', 'staging', or 'prod'")
        if self.mode not in ["raise","log","silent"]:
            raise ValueError("Mode must be 'raise', 'log', or 'silent'")
        
        