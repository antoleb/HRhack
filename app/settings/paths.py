import os

SETTINGS_DIR = os.path.split(os.path.realpath(__file__))[0]

DATA_DIR = os.path.join(SETTINGS_DIR, 'data')
KROK_FILE = os.path.join(DATA_DIR, 'krok.xlsx')
