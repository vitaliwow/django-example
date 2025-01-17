"""Settings to connect with AI server. """

from core.conf.environ import env

AI_SEARCH_HOST = env.str("AI_SEARCH_HOST", "")
AI_SEARCH_PORT = env.int("AI_SEARCH_PORT", 3239)
AI_SEARCH_TOKEN = env.str("AI_SERVER_TOKEN", "")
