from slack import WebClient
import concurrent.futures


def send_to_slack(photo):
    slack_token = os.environ['JIMAPI'] # Your API HERE
    client = slack.WebClient(slack_token)

    # upload file
    response = client.files_upload(
        file=photo,
        initial_comment='Better to Check the Rooms!!',
        channels='#general')

    # assert response['ok']
    # slack_file = response['file']


def send_it(list_of_photos):
    with concurrent.futures.ThreadPoolExecutor() as exe:
        exe.map(send_to_slack, list_of_photos)
