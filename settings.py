CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# For production, consider using Redis or Memcached:
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.redis.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379/1',
#     }
# } 

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# For development only
if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')