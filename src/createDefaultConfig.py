import os
import yaml


def create_default_yaml_file(file_path):
    default_content = {
        'authtoken': '',
        'tunnels': {
            'TP_NGROK': {
                'addr': '127.0.0.1:5000',
                'hostname': '',
                'proto': 'http'
            }
        },
        'version': 2,
        'web_addr': False
    }
    # Check if the file already exists
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            yaml.dump(default_content, file, default_flow_style=False)
        print(f"Created default YAML file at {file_path}")
    else:
        print(f"YAML file already exists at {file_path}")
