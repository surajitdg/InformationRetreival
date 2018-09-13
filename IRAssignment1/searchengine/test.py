from configparser import ConfigParser

cfg = ConfigParser()

cfg.read('static/config.ini')

ignore = cfg.get('others', 'ignoresections')
print(ignore)