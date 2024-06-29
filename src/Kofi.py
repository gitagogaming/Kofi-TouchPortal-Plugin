from flask import Flask, request
from datetime import datetime
from argparse import ArgumentParser
import subprocess
import sys
import json       
import time
import webbrowser
import logging    
import TouchPortalAPI as TP
from TouchPortalAPI.logger import Logger
from TPPEntry import TP_PLUGIN_SETTINGS, PLUGIN_ID, TP_PLUGIN_INFO, __version__
from createDefaultConfig import create_default_yaml_file
from updateConfig import update_config_file
import os
import signal


## figure out how to set a static location for pyngrok to download the ngrok.exe file rather than it doing it every time?
## need to find a way to kill the ngrok process when the plugin is closed rather than the os.kill.. it should be related to the pyinstaller process but 
## seems as if its not since its downloaded after the fact..

app = Flask(__name__)
ngrok_running = False

g_log = Logger(name = PLUGIN_ID)
## setting logging for flask to only log errors
logging.getLogger('werkzeug').setLevel(logging.ERROR)   
logging.getLogger("pyngrok.process.ngrok").setLevel(logging.ERROR)   

try:
    TPClient = TP.Client(
        pluginId = PLUGIN_ID,             # required ID of this plugin
        sleepPeriod = 0.05,               # allow more time than default for other processes
        autoClose = True,                 # automatically disconnect when TP sends "closePlugin" message
        checkPluginId = True,             # validate destination of messages sent to this plugin
        maxWorkers = 4,                   # run up to 4 event handler threads
        updateStatesOnBroadcast = False,  # do not spam TP with state updates on every page change
    )
except Exception as e:
    sys.exit(f"Could not create TP Client, exiting. Error was:\n{repr(e)}")



@app.route('/', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = json.loads(request.form['data'])
        if data['verification_token']  != TP_PLUGIN_SETTINGS['Kofi Verification Token']:
            return '', 403
        
        process_webhook_data(data)
        return '', 200


def process_webhook_data(data):
    payment_type = data.get('type')
    if payment_type == 'Donation':
        process_donation(data)
    elif payment_type in ['Subscription', 'Commission', 'Shop Order']:
        process_payment(data)
    

def process_donation(data):
    g_log.debug(f"Processing Donation: {data}")

    currency_symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥",
        "AUD": "A$",
        "CAD": "C$"
    }
    statelist = []

    symbol = currency_symbols.get(data['currency'], "")  # Returns
    if symbol:
        statelist.append({"id": PLUGIN_ID + ".donation.currency", "value": symbol})

    readable_timestamp = formatTimestamp(data['timestamp'])

    statelist.extend([
        {"id": PLUGIN_ID + ".donation.timestamp", "value": readable_timestamp},
        {"id": PLUGIN_ID + ".donation.name", "value": data['from_name']},
        {"id": PLUGIN_ID + ".donation.message", "value": data['message'] if data.get('message') is not None else ""},
        {"id": PLUGIN_ID + ".donation.amount", "value": f"{symbol}{data['amount']}"}
    ])

    TPClient.stateUpdateMany(statelist)
    trigger_event("newDonation")


def process_payment(data):
    g_log.debug(f"Processing {data['type']}: {data}")

    if data.get('is_subscription_payment'):
        handleSubscription(data)

    if data.get('shop_items') is not None:
        handleShopOrder(data)


def handleSubscription(data):
    statelist = []
    readable_timestamp = formatTimestamp(data['timestamp'])

    statelist.extend([
        {"id":PLUGIN_ID + ".subscription.timestamp", "value":readable_timestamp},
        {"id":PLUGIN_ID + ".subscription.from_name", "value":data['from_name']},
        {"id":PLUGIN_ID + ".subscription.message", "value":data['message'] if data.get('message') is not None else ""},
        {"id":PLUGIN_ID + ".subscription.amount", "value":data['amount'] if data.get('amount') is not None else ""}
    ])

    # first time subscription
    if data.get('is_first_subscription_payment'):
        g_log.info("First subscription payment for the user.")
        statelist.append({"id": PLUGIN_ID + ".subscription.is_first_subscription_payment", "value": str(data['is_subscription_payment']) if data.get('is_subscription_payment') is not None else ""})

    # Checking for Tier
    if data.get('tier_name') is not None:
        statelist.append({"id": PLUGIN_ID + ".subscription.tier_name", "value": data['tier_name']} if data.get('tier_name') is not None else "")

    # Respect the is_public field
    if data.get('is_public'): 
        statelist.append({"id": PLUGIN_ID + ".subscription.is_public", "value": str(data['is_public'])})
    
    TPClient.stateUpdateMany(statelist)

    # Determine trigger event
    if data.get('is_first_subscription_payment') == True:
        trigger_event("newSubscription")
    if data.get('is_first_subscription_payment') == False:
        trigger_event("recurringSubscription")


def handleShopOrder(data):
    g_log.debug(f"Processing Shop Order: {data}")
    total_Items = sum([order['quantity'] for order in data['shop_items']])
    stateList = []
    readable_timestamp = formatTimestamp(data['timestamp'])

    currency_symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥",
        "AUD": "A$",
        "CAD": "C$"
    }
    symbol = currency_symbols.get(data['currency'], "")  # Returns empty string if currency is not found

    stateList.extend([
        {'id':PLUGIN_ID + ".shop.timestamp", 'value':readable_timestamp},
        {'id':PLUGIN_ID + ".shop.from_name", 'value':data['from_name']},
        {'id':PLUGIN_ID + ".shop.message", 'value':data['message'] if data.get('message') is not None else ""},
        {'id':PLUGIN_ID + ".shop.amount", 'value': symbol + data['amount']},
        {'id':PLUGIN_ID + ".shop.city", 'value':data['shipping']['city'] if data.get('shipping') is not None else ""},
        {'id':PLUGIN_ID + ".shop.country", 'value':data['shipping']['country']  if data.get('shipping') is not None else ""},
        {'id':PLUGIN_ID + ".shop.country_code", 'value':data['shipping']['country_code'] if data.get('shipping') is not None else ""},
        {'id':PLUGIN_ID + ".shop.state", 'value':data['shipping']['state_or_province'] if data.get('shipping') is not None else ""},
        {"id": PLUGIN_ID + ".shop.total_items", "value": str(total_Items)}
        ])

    clearStatelist = []
    ## Clearing out all previous shop items in case the next event has fewer
    for state in TPClient.currentStates:
        if state.startswith(PLUGIN_ID + ".shop.shop_item_"):
            clearStatelist.append({"id": state, "value": ""})   
    TPClient.stateUpdateMany(clearStatelist)

    # Loop through the shop items and update the states
    for index, item in enumerate(data['shop_items']): 
        g_log.debug(f"Order {index + 1}: {item['variation_name']} x{item['quantity']}")
        stateList.append({"id": PLUGIN_ID + f".shop.shop_item_{index + 1}", "value": f"{item['variation_name']} x{item['quantity']}"})
    TPClient.stateUpdateMany(stateList)

    trigger_event("newShopOrder")
    

def formatTimestamp(timestamp):
    return datetime.fromisoformat(timestamp.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')   

def trigger_event(event_id):
    """ Triggers event inside of TouchPortal """
    g_log.debug(f"Triggering Event: {event_id}")
    TPClient.stateUpdate(PLUGIN_ID + f".state.{event_id}", "True")
    TPClient.stateUpdate(PLUGIN_ID + f".state.{event_id}", "False")

def handleSettings(settings, on_connect=False):
    settings = { list(settings[i])[0] : list(settings[i].values())[0] for i in range(len(settings)) }
    g_log.debug(f"Settings: {settings}")

    if (value := settings.get("Ngrok Server Address")) is not None:
        TP_PLUGIN_SETTINGS['Ngrok Server Address']['value'] = value

    if (value := settings.get("Ngrok Port")) is not None:
        TP_PLUGIN_SETTINGS['Ngrok Port']['value'] = value

    if (value := settings.get("Ngrok Auth Token")) is not None:
        TP_PLUGIN_SETTINGS['Ngrok Auth Token'] = value

    if (value := settings.get("Kofi Verification Token")) is not None:
        TP_PLUGIN_SETTINGS['Kofi Verification Token'] = value


@TPClient.on(TP.TYPES.onNotificationOptionClicked)
def onNoticationClicked(data):
    if data['optionId'] == f"{PLUGIN_ID}.settings.error.options":
        url = "https://dashboard.ngrok.com/signup"
        webbrowser.open(url, new=0, autoraise=True)


#--- On Startup ---#
@TPClient.on(TP.TYPES.onConnect)
def onConnect(data):
    g_log.info(f"Connected to TP v{data.get('tpVersionString', '?')}, plugin v{data.get('pluginVersion', '?')}.")
    g_log.debug(f"Connection: {data}")
    if settings := data.get('settings'):
        handleSettings(settings, True)

    create_default_yaml_file('ngrok.yaml')
    time.sleep(1)
    config_updated = update_config_file()
    if config_updated:
        g_log.info("Updated ngrok configuration file.")

    start_ngrok()


#--- Settings handler ---#
@TPClient.on(TP.TYPES.onSettingUpdate)
def onSettingUpdate(data):
    g_log.info(f"Settings: {data}")
    handleSettings(data['values'])

    if ngrok_running:
        shutdownNgrok()
        time.sleep(4)
        update_config_file()
        start_ngrok()


#--- Action handler ---#
@TPClient.on(TP.TYPES.onAction)
def onAction(data: dict):
    g_log.debug(f"Action: {data}")

def start_flask():
    app.run(debug=False)
    
from pyngrok import ngrok, conf
from pyngrok.conf import PyngrokConfig
http_tunnel = None
def start_ngrok():
    global ngrok_running, http_tunnel
    ## Starting up Ngrok server
    if TP_PLUGIN_SETTINGS['Ngrok Server Address']['value'] != "" and TP_PLUGIN_SETTINGS['Ngrok Port']['value'] != "":
        try:
            # ngrok_command = "ngrok start --config=ngrok.yaml --all"
            # subprocess.Popen(ngrok_command, shell=True)
            ngrok_config = PyngrokConfig()
            ngrok_config.config_path = "ngrok.yaml" 
            http_tunnel = ngrok.connect(name='TP_NGROK', pyngrok_config=ngrok_config)
            
            ngrok_running = True
        except Exception as e:
            g_log.error(f"Error starting ngrok server: {e}")
    else:
        TPClient.showNotification(
            notificationId= f"{PLUGIN_ID}.settings.error",
            title=f"Kofi Plugin",
            msg="\n ! Settings Error ! \n\nNgrok settings not set\nPlease set the Server Address and Port in the settings\n\n",
            options= [{
            "id":f"{PLUGIN_ID}.settings.error.options",
            "title":"Sign up for Ngrok Server"
        }])
        g_log.info("Ngrok settings not set. Please set the Ngrok Server Address and Port in the settings ")

    ## Starting the Flask server
    try:
        app.run(debug=False)
    except Exception as e:
        g_log.error(f"Error starting Flask server: {e}")



def shutdownNgrok():
    global ngrok_running
    try:
        g_log.info("Shutting down ngrok...")
        ngrok.disconnect(http_tunnel.public_url)
        
        ## ngrok is spawning outside of our pyinstaller sometimes and we need to assure its dead for next reload
        subprocess.run(["taskkill", "/F", "/IM", "ngrok.exe"], check=True)
        g_log.info("ngrok terminated.")
        ngrok_running = False
    except Exception as e:
        g_log.error(f"Error shutting down ngrok: {e}")
        return False

 

# Shutdown handler
@TPClient.on(TP.TYPES.onShutdown)
def onShutdown(data:dict):
    g_log.info('Received shutdown event from TP Client.')
    shutdownNgrok()
    
    ## Requesting a shutdown for the Flask server
    os.kill(os.getpid(), signal.SIGTERM) 
    


## main
def main():
    global TPClient, g_log
    ret = 0  # sys.exit() value

    logFile = f"./{PLUGIN_ID}.log"
    logStream = sys.stdout
    
    parser = ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument("-d", action='store_true',
                        help="Use debug logging.")
    parser.add_argument("-w", action='store_true',
                        help="Only log warnings and errors.")
    parser.add_argument("-q", action='store_true',
                        help="Disable all logging (quiet).")
    parser.add_argument("-l", metavar="<logfile>",
                        help=f"Log file name (default is '{logFile}'). Use 'none' to disable file logging.")
    parser.add_argument("-s", metavar="<stream>",
                        help="Log to output stream: 'stdout' (default), 'stderr', or 'none'.")

    # his processes the actual command line and populates the `opts` dict.
    opts = parser.parse_args()
    del parser

    # trim option string (they may contain spaces if read from config file)
    opts.l = opts.l.strip() if opts.l else 'none'
    opts.s = opts.s.strip().lower() if opts.s else 'stdout'

    # Set minimum logging level based on passed arguments
    logLevel = "INFO"
    if opts.q: logLevel = None
    elif opts.d: logLevel = "DEBUG"
    elif opts.w: logLevel = "WARNING"

    # set log file if -l argument was passed
    if opts.l:
        logFile = None if opts.l.lower() == "none" else opts.l
    # set console logging if -s argument was passed
    if opts.s:
        if opts.s == "stderr": logStream = sys.stderr
        elif opts.s == "stdout": logStream = sys.stdout
        else: logStream = None
        
    TPClient.setLogFile(logFile)
    TPClient.setLogStream(logStream)
    TPClient.setLogLevel(logLevel)

    # ready to go
    g_log.info(f"Starting {TP_PLUGIN_INFO['name']} v{__version__} on {sys.platform}.")


    try:
        TPClient.connect()
        g_log.info('TP Client closed.')
    except KeyboardInterrupt:
        g_log.warning("Caught keyboard interrupt, exiting.")
    except Exception:
        from traceback import format_exc
        g_log.error(f"Exception in TP Client:\n{format_exc()}")
        ret = -1
    finally:
        TPClient.disconnect()

    del TPClient

    g_log.info(f"{TP_PLUGIN_INFO['name']} stopped.")
    return ret



if __name__ == "__main__":
    sys.exit(main())
    
    
    
