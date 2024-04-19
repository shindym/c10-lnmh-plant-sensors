"""This file is responsible for alerting users/botanists via email about a plant having an issue."""
from boto3 import client


class Alerter():
    """"This class is responsible for the functionality required to alert a botanists via email. """

    def __init__(self, config) -> None:
        self.ses_client = self.connect_to_ses_client(config)

    def connect_to_ses_client(self, config):
        """ Returns sesv2 client object."""

        return client('sesv2', aws_access_key_id=config['ACCESS_KEY_ID'],
                      aws_secret_access_key=config['SECRET_ACCESS_KEY'])

    def get_email_addresses_from_names(self, names: list[str]) -> list[str]:
        """Returns a list of valid emails addresses from a list of names."""
        email_list = []
        response = self.ses_client.list_email_identities(
            PageSize=123
        )
        emails = response['EmailIdentities']
        for user in names:
            for email in emails:
                if user in email['IdentityName']:
                    email_list.append(email['IdentityName'])
        return email_list

    def send_plain_email(self, emails: list[str], plant_num: int, body: str, source_email: str = 'trainee.setinder.manic@sigmalabs.co.uk'):
        """Sends an email out to a number of email addresses."""
        self.ses_client.send_email(
            FromEmailAddress=source_email,
            Destination={
                'ToAddresses': emails
            },
            Content={
                'Simple': {
                    'Subject': {
                        'Data': f'Plant {plant_num} Alert',
                        'Charset': "UTF-8"
                    },
                    'Body': {
                        'Text': {
                            'Data': 'string',
                            'Charset': "UTF-8"
                        },
                        'Html': {
                            'Data': f'{body}',
                            'Charset': "UTF-8"
                        }
                    },
                    'Headers': [
                        {
                            'Name': 'string',
                            'Value': 'string'
                        },
                    ]
                }
            }
        )
