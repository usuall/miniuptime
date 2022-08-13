import configparser
import os


def get_Config():
    # 설정파일 읽기
    properties = configparser.ConfigParser()
    config_file = os.path.abspath(os.getcwd()) + '\\config.ini'
    properties.read(config_file, encoding='utf-8')

    return properties