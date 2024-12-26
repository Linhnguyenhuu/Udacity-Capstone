from settings import DATABASE_URL

# Enable debug mode.
DEBUG = True

# Change tracker
SQLALCHEMY_TRACK_MODIFICATIONS = False

# To generate sql queries in the terminal
SQLALCHEMY_ECHO = True

# DATABASE URL
SQLALCHEMY_DATABASE_URI = DATABASE_URL