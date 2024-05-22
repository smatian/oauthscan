import os

class Config:
    SECRET_KEY = os.getenv('INSTAGRAM_APP_SECRET')  
    INSTAGRAM_APP_ID = '295626456945238'
    INSTAGRAM_APP_SECRET = os.getenv('INSTAGRAM_APP_SECRET')
    REDIRECT_URI = 'https://70ac8810-32fb-46bb-9acf-734a23db8ee8-00-25khz7k18zzv.spock.replit.dev/callback'
