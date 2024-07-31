# GoogleContactsBackup

Python3 utility to backup Google Contacts

This utility backups Google Contacts as a vcf file.

Prerequisites

# 1.Enable Google People API:

Go to the Google Cloud Console. Create a new project (or select an existing one) https://console.cloud.google.com/projectcreate Enable the "People API" for your project https://console.cloud.google.com/apis/api/people.googleapis.com/metrics?project=

See https://cloud.google.com/endpoints/docs/openapi/enable-api if you have a problem to enable API

Navigate to the API & Services Dashboard. Configure Consent Screen https://console.cloud.google.com/apis/credentials/consent?project= Define PeopleAPI scope as Contacts READ ONLY (second step of consent screen)

# 2.Set Up OAuth 2.0 Credentials:

In the API & Services Dashboard, go to "Credentials" https://console.cloud.google.com/apis/credentials?project= Create OAuth 2.0 Client ID credentials.

Download the JSON file with your credentials and save it under the name client_secret.json

# 3.Install Required Libraries:

pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client vobject

Note: this program does bot support custom attributes except -Related Person -Significant Date
