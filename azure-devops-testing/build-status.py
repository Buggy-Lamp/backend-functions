import requests

CRED_USERNAME = 'PAT_FROM_WEBSITE'
CRED_PASSWORD = 'ptqqy6k2tjxa6ldjh5262g66sny4o3kkpjepmgc35c6v4l6ow5ma'

API_PARAM_DEFINITION = '1'
API_PARAM_ORG = 'hu-todss-2020'
API_PARAM_PROJECT = 'template-SmartHotel360'
API_BUILD_LATEST = f'https://dev.azure.com/{API_PARAM_ORG}/{API_PARAM_PROJECT}/_apis/build/latest/{API_PARAM_DEFINITION}'


def main():
    print('Starting...')

    # Setup basic auth
    session = requests.Session()
    session.auth = (CRED_USERNAME, CRED_PASSWORD)

    # Get latest build information
    print(f'[*] Hitting: {API_BUILD_LATEST}')
    latest_info = session.get(API_BUILD_LATEST)
    latest_info = latest_info.json()

    # Get timeline url from the build data
    timeline = latest_info['_links']['timeline']['href']
    print(f'[^] Found timeline: {timeline}')

    # Get build timeline information to calculate succeeded score
    print(f'[*] Hitting: {timeline}')
    timeline_info = session.get(timeline)
    timeline_info = timeline_info.json()

    print(f'[^] More than 0 records? {len(timeline_info["records"]) > 0}')

    if len(timeline_info["records"]) <= 0:
        print('[!] Not enough records to calculate score; returning')
        return

    score, target_score = calc_score(timeline_info['records'])
    print(f'[^] Score {score / target_score * 100}% succeeded')


def calc_score(records):
    target_succeeded = len(records)
    succeeded = 0

    if target_succeeded > 0:
        succeeded_records = list(filter(lambda x: x['result'] == 'succeeded', records))
        succeeded = len(succeeded_records)

    return succeeded, target_succeeded


if __name__ == '__main__':
    main()
