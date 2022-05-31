import argparse

import pandas as pd
import progressbar

from settings import client
from src.url import Page


def main(customer_id, output_file, monitor_urls):
    googleads_service = client.get_service("GoogleAdsService")

    data = []
    query = """
        SELECT
            ad_group.id,
            campaign.id,
            campaign.name,
            campaign.status,
            ad_group_ad.ad.id,
            ad_group_ad.ad.name,
            ad_group_ad.ad.final_urls,
            ad_group_ad.ad.final_mobile_urls,
            ad_group_ad.ad.final_app_urls
        FROM ad_group_ad
        WHERE campaign.status != 'REMOVED'
    """
    results = googleads_service.search(
        customer_id=str(customer_id), query=query
    )

    bar = progressbar.ProgressBar(max_value=len(list(results)))
    i = 1
    for row in results:
        urls = [] + \
               list(row.ad_group_ad.ad.final_urls) + \
               list(row.ad_group_ad.ad.final_mobile_urls) + \
               list(row.ad_group_ad.ad.final_app_urls)

        for url in urls:
            d = {
                'customer_id': customer_id,
                'campaign_id': row.campaign.id,
                'campaign_status': str(row.campaign.status),
                'campaign_name': row.campaign.name,
                'ad_group_ad_id': row.ad_group_ad.ad.id,
                'ad_group_ad_name': row.ad_group_ad.ad.name,
                'url': url,
            }

            if monitor_urls:
                page = Page.from_url(url)
                d['nb_redirect'] = page.nb_redirect
                d['destination_url'] = page.destination_url
                d['status_code'] = page.status_code
            d['replace_url_by'] = url

            data.append(d)
        bar.update(i)
        i += 1

    if len(data) > 0:
        df = pd.DataFrame(data)
        df.to_csv(output_file)
    else:
        print('No data.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="List ad groups for specified customer."
    )
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        default=client.login_customer_id,
        help="The Google Ads customer ID.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default='output.csv',
        help="Output CSV file",
    )
    parser.add_argument(
        "-mu",
        "--monitor_urls",
        action='store_true',
        help="Enable URLs monitoring",
    )
    args = parser.parse_args()
    main(args.customer_id, args.output, args.monitor_urls)
