import json
from types import SimpleNamespace

import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


config_path = os.path.join(project_root, 'configs', 'config.json')
with open(config_path, 'r', encoding="utf-8") as config_file:
    data = config_file.read()
config = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))


config_path = os.path.join(project_root, 'configs', 'text_configs', 'main', 'main_answer_text_config.json')
with open(config_path, 'r', encoding="utf-8") as config_file:
    data = config_file.read()
main_answer_text_config = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))


config_path = os.path.join(project_root, 'configs', 'text_configs', 'main', 'main_send_text_config.json')
with open(config_path, 'r', encoding="utf-8") as config_file:
    data = config_file.read()
main_send_text_config = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))


config_path = os.path.join(project_root, 'configs', 'text_configs','register', 'register_answer_text_config.json')
with open(config_path, 'r', encoding="utf-8") as config_file:
    data = config_file.read()
register_answer_text_config = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))


config_path = os.path.join(project_root, 'configs', 'text_configs', 'register', 'register_send_text_config.json')
with open(config_path, 'r', encoding="utf-8") as config_file:
    data = config_file.read()
register_send_text_config = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))


def db_path():
    return os.path.join(project_root, config.db_path)






# config_path = os.path.join(project_root, 'configs', 'text_configs', 'send_text_config.json')
# with open(config_path, 'r', encoding="utf-8") as config_file:
#     data = config_file.read()
# send_text_config = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
#
#
# config_path = os.path.join(project_root, 'configs', 'text_configs', 'answer_text_config.json')
# with open(config_path, 'r', encoding="utf-8") as config_file:
#     data = config_file.read()
# answer_text_config = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))