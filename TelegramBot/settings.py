import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
MEDIA_ROOT = os.path.join(BASE_DIR, 'Media/')

if not os.path.exists(MEDIA_ROOT):
	os.makedirs(MEDIA_ROOT)