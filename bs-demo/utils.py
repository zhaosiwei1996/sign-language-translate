import os
import sys
import orjson
import time
import requests
import platform
import subprocess
import logging
import socket


class BaseUtils:
    @staticmethod
    def get_timestamp():
        return int(time.time())

    @staticmethod
    def json_to_string(data):
        return orjson.dumps(data).decode('utf-8')

    @staticmethod
    def string_to_json(data):
        return orjson.loads(data)

    @staticmethod
    def send_default_info(data):
        info = {"timestamp": int(time.time()), "response": data}
        return orjson.dumps(info)

    @staticmethod
    def read_file(file_path):
        with open(file_path, 'r') as file:
            return file.read()

    @staticmethod
    def write_file(file_path, content):
        with open(file_path, 'w') as file:
            file.write(content)

    @staticmethod
    def append_to_file(file_path, content):
        with open(file_path, 'a') as file:
            file.write(content)

    @staticmethod
    def setup_logging(log_file):
        logging.basicConfig(level=logging.INFO,
                            format='[%(levelname)s] %(asctime)s [%(funcName)s] %(message)s')

    @staticmethod
    def log(message):
        logging.info(message)

    @staticmethod
    def get_system_type():
        return platform.system()

    @staticmethod
    def send_post_request(url, data):
        response = requests.post(url, json=data)
        return response.json()

    @staticmethod
    def send_get_request(url, params=None):
        response = requests.get(url, params=params)
        return response.json()

    @staticmethod
    def send_delete_request(url):
        response = requests.delete(url)
        return response.json()

    @staticmethod
    def send_put_request(url, data):
        response = requests.put(url, json=data)
        return response.json()

    @staticmethod
    def get_client_ip():
        return socket.gethostbyname(socket.gethostname())

    @staticmethod
    def execute_command(command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        return {
            'output': output.decode('utf-8'),
            'error': error.decode('utf-8'),
            'returncode': process.returncode
        }
