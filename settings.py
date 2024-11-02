from decouple import config

class Config:
    # Configuración de TheMovieDB
    THEMOVIEDB_API_KEY = config('THEMOVIEDB_API_KEY')
    ACCOUNT_ID = config('ACCOUNT_ID')
    ACCESS_TOKEN = config('THEMOVIEDB_ACCESS_TOKEN')
    CACHE_DURATION = config('CACHE_DURATION', default=30)

    @property
    def headers(self):
        return {
            "Authorization": f"Bearer {self.ACCESS_TOKEN}",
            "Content-Type": "application/json;charset=utf-8"
        }

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development': DevelopmentConfig
}
