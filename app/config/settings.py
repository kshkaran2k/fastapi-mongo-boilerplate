import os
from app.config.default import DefaultConfig

class Config:
    MONGO_URI = os.getenv('MONGO_URI', DefaultConfig.MONGO_URI)
    ENV = os.getenv('ENV', DefaultConfig.ENV)
    MODE = os.getenv('MODE', DefaultConfig.MODE)

