# GoogleContactsBackup

Python3 utility to backup Google Contacts

This utility backups Google Contacts as a vcf file.

Prerequisites

# 1.Enable Google People API:

Go to the Google Cloud Console. <br>
Create a new project (or select an existing one) https://console.cloud.google.com/projectcreate <br>
Enable the "People API" for your project https://console.cloud.google.com/apis/api/people.googleapis.com/metrics?project= <br>

See https://cloud.google.com/endpoints/docs/openapi/enable-api if you have a problem to enable API <br>

Navigate to the API & Services Dashboard.<br>
Configure Consent Screen https://console.cloud.google.com/apis/credentials/consent?project= <br>
Define PeopleAPI scope as Contacts READ ONLY (second step of consent screen) <br>

# 2.Set Up OAuth 2.0 Credentials:

In the API & Services Dashboard, go to "Credentials" https://console.cloud.google.com/apis/credentials?project= <br>
Create OAuth 2.0 Client ID credentials.<br>
Download the JSON file with your credentials and save it under the name client_secret.json v

# 3.Install Required Libraries:

pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client vobject <br>

Note: this program does bot support custom attributes except -Related Person -Significant Date v
