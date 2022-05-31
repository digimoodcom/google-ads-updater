# Google Ads Updater
[![Python package](https://github.com/digimoodcom/google-ads-updater/actions/workflows/main.yml/badge.svg)](https://github.com/digimoodcom/google-ads-updater/actions/workflows/main.yml)

## Requirements
- Python > 3.7 https://www.python.org/downloads/
- PIP https://pip.pypa.io/en/stable/installation/

## How to use it

### Install dependencies
```commandline
pip install -r requirements.txt
```

### Edit google-ads.yaml
```commandline
# See https://developers.google.com/google-ads/api/docs/first-call/dev-token
developer_token: YOUR_DEVELOPER_TOKEN

# See https://developers.google.com/google-ads/api/docs/oauth/overview  
client_id: YOUR_CLIENT_ID
client_secret: YOUR_CLIENT_SECRET
refresh_token: YOUR_REFRESH_TOKEN

# See https://developers.google.com/google-ads/api/docs/concepts/call-structure?hl=en#cid
login_customer_id: YOUR_LOGIN_CUSTOMER_ID
```

### Export all campaigns
```commandline
python export.py -c YOUR_CUSTOMER_ID --monitor_urls
```
An `output.csv` was created.

### Open output.csv
Open `output.csv` and replace your urls in the `replace_url_by` column.

| customer_id | campaign_id | campaign_status        | campaign_name            | ad_group_ad_id | ad_group_ad_name | url                 | replace_url_by       |
|-------------|-------------|------------------------|--------------------------|----------------|------------------|---------------------|----------------------|
| 9570124171  | 17325082039 | CampaignStatus.PAUSED  | Website traffic-Search-3 | 599902919184   | ad_group_ad_1    | http://digimood.com | https://digimood.com |
| 9570124171  | 17325082039 | CampaignStatus.PAUSED  | Website traffic-Search-3 | 599904259677   | ad_group_ad_2    | http://digimood.com | https://digimood.com |
| 9570124171  | 17325082039 | CampaignStatus.PAUSED  | Website traffic-Search-3 | 599904259677   | ad_group_ad_2    | http://digimood.com | https://digimood.com |
| 9570124171  | 17325082040 | CampaignStatus.ENABLED | Website traffic-Search-6 | 599904259678   | ad_group_ad_3    | http://digimood.com | https://digimood.com |

### Apply your changes to Google Ads
```commandline
python import.py
```