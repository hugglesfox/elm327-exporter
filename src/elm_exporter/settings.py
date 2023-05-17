from starlette.config import Config

config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=False)
LOG_LEVEL = config("LOG_LEVEL", cast=str, default="INFO")
ELM_PORT = config("ELM_PORT", cast=str, default=None)
ELM_MAX_RETRIES = config("ELM_MAX_RETRIES", cast=int, default=1)
ELM_AUTO_LP = config("ELM_AUTO_LP", cast=bool, default=True)
