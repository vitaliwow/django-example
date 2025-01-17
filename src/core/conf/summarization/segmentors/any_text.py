from core.conf.environ import env

THRESHOLD = env("THRESHOLD", cast=float, default=0.3)
THRESHOLD_RATIO = env("THRESHOLD_RATIO", cast=float, default=0.7)
MIN_PARAGRAPH_LEN = env("MIN_PARAGRAPH_LEN", cast=int, default=150)
MIN_PARAGRAPH_COUNT = env("MIN_PARAGRAPH_COUNT", cast=int, default=3)
MAX_PARAGRAPH_COUNT = env("MAX_PARAGRAPH_COUNT", cast=int, default=30)
MIN_PARAGRAPH_RATIO = env("MIN_PARAGRAPH_RATIO", cast=float, default=None)
MAX_PARAGRAPH_RATIO = env("MAX_PARAGRAPH_RATIO", cast=float, default=None)
MIN_PARAGRAPHS_PER_MINUTE = env("MIN_PARAGRAPHS_PER_MINUTE", cast=float, default=0.5)
MAX_PARAGRAPHS_PER_MINUTE = env("MAX_PARAGRAPHS_PER_MINUTE", cast=float, default=None)
