import os


APP_NAME = os.environ.get('APP_NAME', 'tic-tac-toe')
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
