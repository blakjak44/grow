# -*- coding: utf-8 -*-
"""Application configuration."""
import os
from datetime import timedelta


class Config(object):
    """Base configuration."""

    SECRET_KEY = os.environ.get('CONDUIT_SECRET', 'secret-key')  # TODO: Change me
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    CORS_ORIGN_WHITELIST = [
        'http://0.0.0.0:8080',
        'http://localhost:8080',
    ]


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False
    MONGODB_DATABASE_URI = os.environ.get('DATABASE_URL', 'localhost:27017/grow')


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True


class TestConfig(Config):
    """Test configuration."""

    ENV = 'test'
    TESTING = True
    DEBUG = True
