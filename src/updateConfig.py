from TPPEntry import TP_PLUGIN_SETTINGS, PLUGIN_ID, TP_PLUGIN_INFO, __version__
import yaml

def update_config_file():
    # Load the current ngrok configuration
    with open('ngrok.yaml', 'r') as file:
        ngrok_config = yaml.safe_load(file)

    tunnel_name = 'TP_NGROK' 
    config_changed = False

    # Update the authtoken if it has changed
    if ngrok_config.get('authtoken') != TP_PLUGIN_SETTINGS['Ngrok Auth Token']:
        ngrok_config['authtoken'] = TP_PLUGIN_SETTINGS['Ngrok Auth Token']
        config_changed = True

    if tunnel_name in ngrok_config['tunnels']:
        current_hostname = ngrok_config['tunnels'][tunnel_name].get('hostname')
        new_hostname = TP_PLUGIN_SETTINGS['Ngrok Server Address']['value']
        current_addr = ngrok_config['tunnels'][tunnel_name].get('addr')
        new_addr = "127.0.0.1:" + TP_PLUGIN_SETTINGS['Ngrok Port']['value']

        # Check if the hostname or addr has changed
        if current_hostname != new_hostname or current_addr != new_addr:
            ngrok_config['tunnels'][tunnel_name]['hostname'] = new_hostname
            ngrok_config['tunnels'][tunnel_name]['addr'] = new_addr
            config_changed = True

    # Only rewrite the ngrok.yaml file if the configuration has changed
    if config_changed:
        with open('ngrok.yaml', 'w') as file:
            yaml.dump(ngrok_config, file, default_flow_style=False)
        return True
