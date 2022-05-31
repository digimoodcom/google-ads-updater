import argparse

import pandas
import progressbar
from google.api_core import protobuf_helpers

from settings import client


def main(input_file):
    ad_service = client.get_service("AdService")

    df = pandas.read_csv(input_file)
    bar = progressbar.ProgressBar(max_value=df.shape[0])
    i = 1
    for idx, row in df.iterrows():
        request = client.get_type("GetAdRequest")
        request.resource_name = ad_service.ad_path(
            row['customer_id'], row['ad_group_ad_id']
        )

        response = ad_service.get_ad(request=request)
        final_urls = list(map(lambda x: x.replace(row['url'], row['replace_url_by']), response.final_urls))
        final_mobile_urls = list(map(lambda x: x.replace(row['url'], row['replace_url_by']), response.final_mobile_urls))
        final_app_urls = list(map(lambda x: x.replace(row['url'], row['replace_url_by']), response.final_app_urls))

        ad_operation = client.get_type("AdOperation")
        ad = ad_operation.update
        ad.resource_name = request.resource_name

        ad.final_urls = final_urls
        ad.final_mobile_urls = final_mobile_urls
        ad.final_app_urls = final_app_urls

        client.copy_from(
            ad_operation.update_mask,
            protobuf_helpers.field_mask(None, ad._pb),
        )

        ad_service.mutate_ads(
            customer_id=str(row['customer_id']), operations=[ad_operation]
        )
        bar.update(i)
        i += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="List ad groups for specified customer."
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        default='output.csv',
        help="Input CSV file",
    )
    args = parser.parse_args()
    main(args.input)
