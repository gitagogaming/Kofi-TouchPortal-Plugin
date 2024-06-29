PLUGIN_ID = "gitago.kofi"
PLUGIN_NAME = "Kofi"
PLUGIN_ICON = "Kofi_Logo_26px.png"
PLUGIN_FOLDER = "Kofi"
__version__ = 100



TP_PLUGIN_INFO = {
    "sdk": 6,
    'version': __version__,
    "name": "Kofi",
    "id": PLUGIN_ID,
    "plugin_start_cmd_windows": "%TP_PLUGIN_FOLDER%Kofi\\Kofi_Plugin.exe",
    "configuration": {
        "colorDark": "#222423",
        "colorLight": "#43a047"
    },
    "plugin_start_cmd": "%TP_PLUGIN_FOLDER%Kofi\\Kofi_Plugin.exe"
}

TP_PLUGIN_SETTINGS = {
    'Ngrok Server Address': {
        'name': "Ngrok Server Address",
        'type': "text",
        'default': "",
        'readOnly': False,
        'value': None,
        "isPassword": False
    },
    'Ngrok Port': {
        'name': "Ngrok Port",
        'type': "text",
        'default': "5000",
        'readOnly': False,
        'value': None  
    },
    "Ngrok Auth Token": {
        'name': "Ngrok Auth Token",
        'type': "text",
        'default': "",
        'readOnly': False,
        'value': None,
        "isPassword": True
    },
    "Kofi Verification Token": {
        'name': "Kofi Verification Token",
        'type': "text",
        'default': "",
        'readOnly': False,
        'value': None,
        "isPassword": True
    }
 }

TP_PLUGIN_CATEGORIES = {
    "main": {
        "id": PLUGIN_ID + ".main",
        "name": "Kofi Main Category",
        "imagepath": "%TP_PLUGIN_FOLDER%Kofi\\Kofi_Logo_26px.png"
    },
    "donation": {
        "id": PLUGIN_ID + ".donation",
        "name": "Kofi - New Donations",
        "imagepath": "%TP_PLUGIN_FOLDER%Kofi\\Kofi_Logo_26px.png"
    },
    "subscription": {
        "id": PLUGIN_ID + ".subscription",
        "name": "Kofi - New Subscriptions",
        "imagepath": "%TP_PLUGIN_FOLDER%Kofi\\Kofi_Logo_26px.png"
    },
    "shop": {
        "id": PLUGIN_ID + ".shop",
        "name": "Kofi - New Shop Orders",
        "imagepath": "%TP_PLUGIN_FOLDER%Kofi\\Kofi_Logo_26px.png"
    }
}


TP_PLUGIN_ACTIONS = {
  
}

TP_PLUGIN_STATES = { }


SHOP_STATES = {
    "shop_timestamp": {
        "id": PLUGIN_ID + ".shop.timestamp",
        "type": "text",
        "desc": "Timestamp of the Shop Order",
        "default": "",
        "category": "shop"
    },
    "shop_is_public": {
        "id": PLUGIN_ID + ".shop.is_public",
        "type": "text",
        "desc": "Is the Shop Order Public",
        "default": "",
        "category": "shop"
    },
    "city": {
        "id": PLUGIN_ID + ".shop.city",
        "type": "text",
        "desc": "City of the Shop Order",
        "default": "",
        "category": "shop"
    },
    "state": {
        "id": PLUGIN_ID + ".shop.state",
        "type": "text",
        "desc": "State of the Shop Order",
        "default": "",
        "category": "shop"
    },
    "country": {
        "id": PLUGIN_ID + ".shop.country",
        "type": "text",
        "desc": "Country of the Shop Order",
        "default": "",
        "category": "shop"
    },
    "country_code": {
        "id": PLUGIN_ID + ".shop.country_code",
        "type": "text",
        "desc": "Country Code of the Shop Order",
        "default": "",
        "category": "shop"
    },
    "shop_item_1": {
        "id": PLUGIN_ID + ".shop.shop_item_1",
        "type": "text",
        "desc": "Shop Item 1 Details",
        "default": "",
        "category": "shop"
    },
    "shop_item_2": {
        "id": PLUGIN_ID + ".shop.shop_item_2",
        "type": "text",
        "desc": "Shop Item 2 Details",
        "default": "",
        "category": "shop"
    },
    "shop_item_3": {
        "id": PLUGIN_ID + ".shop.shop_item_3",
        "type": "text",
        "desc": "Shop Item 3 Details",
        "default": "",
        "category": "shop"
    },
    "shop_item_4": {
        "id": PLUGIN_ID + ".shop.shop_item_4",
        "type": "text",
        "desc": "Shop Item 4 Details",
        "default": "",
        "category": "shop"
    },
    "shop_item_5": {
        "id": PLUGIN_ID + ".shop.shop_item_5",
        "type": "text",
        "desc": "Shop Item 5 Details",
        "default": "",
        "category": "shop"
    },
    "shop_item_6": {
        "id": PLUGIN_ID + ".shop.shop_item_6",
        "type": "text",
        "desc": "Shop Item 6 Details",
        "default": "",
        "category": "shop"
    },
    "total_items": {
        "id": PLUGIN_ID + ".shop.total_items",
        "type": "text",
        "desc": "Total Items Ordered",
        "default": "",
        "category": "shop"
    },
    "shop_total_amount": {
        "id": PLUGIN_ID + ".shop.amount",
        "type": "text",
        "desc": "Total Amount of the Shop Order",
        "default": "",
        "category": "shop"
    },
    "newShopOrder": {
        "id": PLUGIN_ID + ".state.newShopOrder",
        "type": "text",
        "desc": "New Shop Order Event",
        "default": "",
        "category": "shop"
    }
}


DONATION_STATES = {
    "donation_name": {
        "id": PLUGIN_ID + ".donation.name",
        "type": "text",
        "desc": "Name of the Donor",
        "default": "",
        "category": "donation"
    },
    "donation_message": {
        "id": PLUGIN_ID + ".donation.message",
        "type": "text",
        "desc": "Message from the Donor",
        "default": "",
        "category": "donation"
    },
    "donation_amount": {
        "id": PLUGIN_ID + ".donation.amount",
        "type": "text",
        "desc": "Amount Donated",
        "default": "",
        "category": "donation"
    },
    "donation_timestamp": {
        "id": PLUGIN_ID + ".donation.timestamp",
        "type": "text",
        "desc": "Timestamp of the Donation",
        "default": "",
        "category": "donation"
    },
    "donation_is_public": {
        "id": PLUGIN_ID + ".donation.is_public",
        "type": "text",
        "desc": "Is the Donation Public",
        "default": "",
        "category": "donation"
    },
    "donation_currency_type": {
        "id": PLUGIN_ID + ".donation.currency",
        "type": "text",
        "desc": "Currency Type of the Donation",
        "default": "",
        "category": "donation"
    },
    "newDonation": {
        "id": PLUGIN_ID + ".state.newDonation",
        "type": "text",
        "desc": "New Donation Event",
        "default": "",
        "category": "donation"
    }

}



SUBSCRIPTION_STATES = {
    "is_first_subscription_payment": {
        "id": PLUGIN_ID + ".subscription.is_first_subscription_payment",
        "type": "text",
        "desc": "Is this the first subscription payment",
        "default": "",
        "category": "subscription"
    },
    "subscription_timestamp": {
        "id": PLUGIN_ID + ".subscription.timestamp",
        "type": "text",
        "desc": "Timestamp of the Subscription Payment",
        "default": "",
        "category": "subscription"
    },
    "subscription_is_public": {
        "id": PLUGIN_ID + ".subscription.is_public",
        "type": "text",
        "desc": "Is the Subscription Payment Public",
        "default": "",
        "category": "subscription"
    },
    "subscription_from_name": {
        "id": PLUGIN_ID + ".subscription.from_name",
        "type": "text",
        "desc": "Name of the Subscriber",
        "default": "",
        "category": "subscription"
    },
    "subscription_message": {
        "id": PLUGIN_ID + ".subscription.message",
        "type": "text",
        "desc": "Message from the Subscriber",
        "default": "",
        "category": "subscription"
    },
    "subscription_amount": {
        "id": PLUGIN_ID + ".subscription.amount",
        "type": "text",
        "desc": "Amount of the Subscription Payment",
        "default": "",
        "category": "subscription"
    },
    "subscription_currency_type": {
        "id": PLUGIN_ID + ".subscription.currency_type",
        "type": "text",
        "desc": "Currency Type of the Subscription Payment",
        "default": "",
        "category": "subscription"
    },
    "subscription_tier_name": {
        "id": PLUGIN_ID + ".subscription.tier_name",
        "type": "text",
        "desc": "Name of the Subscription Tier",
        "default": "",
        "category": "subscription"
    },
    "newSubscription": {
        "id": PLUGIN_ID + ".state.newSubscription",
        "type": "text",
        "desc": "New Subscription Event",
        "default": "",
        "category": "subscription"
    },
    "recurringSubscription": {
        "id": PLUGIN_ID + ".state.recurringSubscription",
        "type": "text",
        "desc": "Recurring Subscription Event",
        "default": "",
        "category": "subscription"
    }
}



TP_PLUGIN_STATES.update(SUBSCRIPTION_STATES)
TP_PLUGIN_STATES.update(DONATION_STATES)
TP_PLUGIN_STATES.update(SHOP_STATES)



TP_PLUGIN_CONNECTORS = {}
TP_PLUGIN_EVENTS = {
    "0": {
        'id': PLUGIN_ID + ".event.newDonation",
        'name':"Kofi | New Donation",
        'category': "main",
        "format":"When receiving a new donation $val",
        "type":"communicate",
        "valueType":"choice",
        "valueChoices": [
        "True"
        ],
    "valueStateId": PLUGIN_ID + ".state.newDonation",
    },
    "1": {
        'id': PLUGIN_ID + ".event.newSubscription",
        'name':"Kofi | New Subscription",
        'category': "main",
        "format":"When receiving a new subscription $val",
        "type":"communicate",
        "valueType":"choice",
        "valueChoices": [
        "True"
        ],
    "valueStateId": PLUGIN_ID + ".state.newSubscription",
    },
    "2": {
        'id': PLUGIN_ID + ".event.newShopOrder",
        'name':"Kofi | New Shop Order",
        'category': "main",
        "format":"When receiving a new shop order $val",
        "type":"communicate",
        "valueType":"choice",
        "valueChoices": [
        "True"
        ],
    "valueStateId": PLUGIN_ID + ".state.newShopOrder",
    },
    "3": {
        'id': PLUGIN_ID + ".event.recurringSubscription",
        'name':"Kofi | Recurring Subscription",
        'category': "main",
        "format":"When receiving a recurring subscription $val",
        "type":"communicate",
        "valueType":"choice",
        "valueChoices": [
        "True"
        ],
    "valueStateId": PLUGIN_ID + ".state.recurringSubscription",
    }


}


