
<img src="https://github.com/gitagogaming/Kofi-TouchPortal-Plugin/assets/76603653/4c3e4761-ad49-4863-841d-4103de39389a" width="1000" height="1000">

# Kofi
- [Kofi](#Kofi)
  - [Description](#description) 
  - [Settings Overview](#Settings-Overview)
  - [Features](#Features)
    - [States](#states)
        - [Kofi - New Donations](#gitago.kofi.donationstates)
        - [Kofi - New Subscriptions](#gitago.kofi.subscriptionstates)
        - [Kofi - New Shop Orders](#gitago.kofi.shopstates)
    - [Events](#events)
        - [Kofi Main Category](#gitago.kofi.mainevents)
  - [How To Install](#how-to-install)
  - [Bugs and Support](#bugs-and-suggestion)
  - [License](#license)
  
# Description

This documentation generated for Kofi V100 with [Python TouchPortal SDK](https://github.com/KillerBOSS2019/TouchPortal-API).

## Settings Overview
| Read-only | Type | Default Value |
| --- | --- | --- |
| False | text |  |

| Read-only | Type | Default Value |
| --- | --- | --- |
| False | text | 5000 |

| Read-only | Type | Default Value |
| --- | --- | --- |
| False | text |  |

| Read-only | Type | Default Value |
| --- | --- | --- |
| False | text |  |


# Features

## States
<details id='gitago.kofi.subscriptionstates'><summary><b>Category:</b> Kofi - New Subscriptions <small><ins>(Click to expand)</ins></small></summary>


| Id | Description | DefaultValue | parentGroup |
| --- | --- | --- | --- |
| .subscription.is_first_subscription_payment | Is this the first subscription payment |  |   |
| .subscription.timestamp | Timestamp of the Subscription Payment |  |   |
| .subscription.is_public | Is the Subscription Payment Public |  |   |
| .subscription.from_name | Name of the Subscriber |  |   |
| .subscription.message | Message from the Subscriber |  |   |
| .subscription.amount | Amount of the Subscription Payment |  |   |
| .subscription.currency_type | Currency Type of the Subscription Payment |  |   |
| .subscription.tier_name | Name of the Subscription Tier |  |   |
| .state.newSubscription | New Subscription Event |  |   |
| .state.recurringSubscription | Recurring Subscription Event |  |   |
</details>

<details id='gitago.kofi.donationstates'><summary><b>Category:</b> Kofi - New Donations <small><ins>(Click to expand)</ins></small></summary>


| Id | Description | DefaultValue | parentGroup |
| --- | --- | --- | --- |
| .donation.name | Name of the Donor |  |   |
| .donation.message | Message from the Donor |  |   |
| .donation.amount | Amount Donated |  |   |
| .donation.timestamp | Timestamp of the Donation |  |   |
| .donation.is_public | Is the Donation Public |  |   |
| .donation.currency | Currency Type of the Donation |  |   |
| .state.newDonation | New Donation Event |  |   |
</details>

<details id='gitago.kofi.shopstates'><summary><b>Category:</b> Kofi - New Shop Orders <small><ins>(Click to expand)</ins></small></summary>


| Id | Description | DefaultValue | parentGroup |
| --- | --- | --- | --- |
| .shop.timestamp | Timestamp of the Shop Order |  |   |
| .shop.is_public | Is the Shop Order Public |  |   |
| .shop.city | City of the Shop Order |  |   |
| .shop.state | State of the Shop Order |  |   |
| .shop.country | Country of the Shop Order |  |   |
| .shop.country_code | Country Code of the Shop Order |  |   |
| .shop.shop_item_1 | Shop Item 1 Details |  |   |
| .shop.shop_item_2 | Shop Item 2 Details |  |   |
| .shop.shop_item_3 | Shop Item 3 Details |  |   |
| .shop.shop_item_4 | Shop Item 4 Details |  |   |
| .shop.shop_item_5 | Shop Item 5 Details |  |   |
| .shop.shop_item_6 | Shop Item 6 Details |  |   |
| .shop.total_items | Total Items Ordered |  |   |
| .shop.amount | Total Amount of the Shop Order |  |   |
| .state.newShopOrder | New Shop Order Event |  |   |
</details>

<br>

## Events

<td></tr>
<td></tr>
<td></tr>
<td></tr>
<details open id='gitago.kofi.mainevents'><summary><b>Category: </b>Kofi Main Category <small><ins>(Click to expand)</ins></small></summary>

<table>
<tr valign='buttom'><th>Id</th><th>Name</th><th nowrap>Evaluated State Id</th><th>Format</th><th>Type</th><th>Choice(s)</th></tr>
<tr valign='top'><td>.event.newDonation</td><td>Kofi | New Donation</td><td>.state.newDonation</td><td>When receiving a new donation $val</td><td>choice</td><td><ul><li>True</li></ul></td><tr valign='top'><td>.event.newSubscription</td><td>Kofi | New Subscription</td><td>.state.newSubscription</td><td>When receiving a new subscription $val</td><td>choice</td><td><ul><li>True</li></ul></td><tr valign='top'><td>.event.newShopOrder</td><td>Kofi | New Shop Order</td><td>.state.newShopOrder</td><td>When receiving a new shop order $val</td><td>choice</td><td><ul><li>True</li></ul></td><tr valign='top'><td>.event.recurringSubscription</td><td>Kofi | Recurring Subscription</td><td>.state.recurringSubscription</td><td>When receiving a recurring subscription $val</td><td>choice</td><td><ul><li>True</li></ul></td></table></details>
<br>

# How To Install 
YouTube Tutorial<br>
<a href="https://www.youtube.com/watch?v=Hv2nZPQMh24">
  <img src="https://img.youtube.com/vi/Hv2nZPQMh24/0.jpg" alt="IMAGE ALT TEXT HERE">
</a>

# Bugs and Suggestion
Open an issue on github or join offical [TouchPortal Discord](https://discord.gg/MgxQb8r) for support.


# License
This plugin is licensed under the [GPL 3.0 License] - see the [LICENSE](LICENSE) file for more information.

