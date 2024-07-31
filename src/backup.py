import os
import json
import google.auth
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']

#People API Page size
PEOPLE_API_PAGE_SIZE = 100

# Function to authenticate and get the service
def get_service():
    creds = None
    # Load the credentials file
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no valid credentials available, request new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('people', 'v1', credentials=creds)

# Function to fetch contacts with pagination
def fetch_contacts(service):
    contacts = []
    page_token = None
    while True:
        results = service.people().connections().list(
            resourceName='people/me',
            personFields='names,emailAddresses,phoneNumbers,biographies,birthdays,addresses,urls,organizations,relations,events',
            pageToken=page_token,
            pageSize=PEOPLE_API_PAGE_SIZE
        ).execute()
        connections = results.get('connections', [])
        contacts.extend(connections)
        page_token = results.get('nextPageToken')
        if not page_token:
            break
    return contacts

# Add names
def add_names(contact, vcf_content):
    name = contact['names'][0]
    family = name.get('familyName', '')
    given = name.get('givenName', '')
    additional = name.get('middleName', '')
    prefix = name.get('honorificPrefix', '')
    suffix = name.get('honorificSuffix', '')
    display_name = name.get('displayName', '')
    vcf_content.append(f"N:{family};{given};{additional};{prefix};{suffix}")
    vcf_content.append(f"FN:{display_name}")

# Add email addresses
def add_emailAddresses(contact, vcf_content):
    for email in contact['emailAddresses']:
        email_value = email.get('value', '')
        email_type = email.get('type', 'INTERNET').upper()
        vcf_content.append(f"EMAIL;TYPE={email_type}:{email_value}")

# Add phone numbers
def add_phoneNumbers(contact, vcf_content):
    for phone in contact['phoneNumbers']:
        phone_value = phone.get('value', '')
        phone_type = phone.get('type', 'Other').upper()
        vcf_content.append(f"TEL;TYPE={phone_type}:{phone_value}")

# Add birthdays
def add_birthdays(contact, vcf_content):
    for birthday in contact['birthdays']:
        if 'date' in birthday:
            date = birthday['date']
            year = date.get('year', '')
            month = f"{date.get('month', 1):02}"
            day = f"{date.get('day', 1):02}"
            vcf_content.append(f"BDAY:{year}-{month}-{day}")

# Add addresses
def add_addresses(contact, vcf_content):
    for address in contact['addresses']:
        street = address.get('streetAddress', '')
        city = address.get('city', '')
        region = address.get('region', '')
        code = address.get('postalCode', '')
        country = address.get('country', '')
        address_type = address.get('type', 'HOME').upper()
        vcf_content.append(f"ADR;TYPE={address_type}:;;{street};{city};{region};{code};{country}")

# Add URLs
def add_urls(contact, vcf_content):
    for url in contact['urls']:
        url_value = url.get('value', '')
        url_type = url.get('type', 'Home Page').upper()
        vcf_content.append(f"URL;TYPE={url_type}:{url_value}")

# Add organizations
def add_organizations(contact, vcf_content):
    for org in contact['organizations']:
        org_name = org.get('name', '')
        org_title = org.get('title', '')
        vcf_content.append(f"ORG:{org_name}")
        if org_title:
            vcf_content.append(f"TITLE:{org_title}")

# Add relations
def add_x_attribute_relations(contact, vcf_content, start_idx):
    for idx, relation in enumerate(contact['relations'], start=start_idx):
        related_name = relation.get('person', '')
        related_label = f"_$!<{relation.get('type', 'Other').capitalize()}>!$_"
        vcf_content.append(f"item{idx}.X-ABRELATEDNAMES:{related_name}")
        vcf_content.append(f"item{idx}.X-ABLabel:{related_label}")
        start_idx += 1
    return start_idx

# Add significant dates
def add_x_attribute_significant_dates(contact, vcf_content, start_idx):
    for idx, event in enumerate(contact['events'], start=start_idx):
        if 'date' in event:
            date = event['date']
            year = date.get('year', '')
            month = f"{date.get('month', 1):02}"
            day = f"{date.get('day', 1):02}"
            event_date = f"{year}{month}{day}"
            label = event.get('type', 'Other').replace('_', ' ').title()
            vcf_content.append(f"item{idx}.X-ABDATE:{event_date}")
            vcf_content.append(f"item{idx}.X-ABLabel:{label}")
            start_idx += 1
    return start_idx

# Add biographies
def add_biographies(contact, vcf_content):
    for bio in contact['biographies']:
        note_value = bio.get('value', '').replace('\n', '\\n')
        vcf_content.append(f"NOTE:{note_value}")

# Function to generate VCF content
def generate_vcf(contacts):
    start_idx = 1
    vcf_content = []
    for contact in contacts:
        vcf_content.append("BEGIN:VCARD")
        vcf_content.append("VERSION:3.0")
        
        # Add names
        if 'names' in contact:
            add_names(contact, vcf_content)
        
        # Add emails
        if 'emailAddresses' in contact:
            add_emailAddresses(contact, vcf_content)
        
        # Add phone numbers
        if 'phoneNumbers' in contact:
            add_phoneNumbers(contact, vcf_content)
        
        # Add notes
        if 'biographies' in contact:
            add_biographies(contact, vcf_content)
        
        # Add birthdays
        if 'birthdays' in contact:
            add_birthdays(contact, vcf_content)
        
        # Add addresses
        if 'addresses' in contact:
            add_addresses(contact, vcf_content)
        
        # Add websites
        if 'urls' in contact:
            add_urls(contact, vcf_content)
        
        # Add organizations
        if 'organizations' in contact:
            add_organizations(contact, vcf_content)
        
        # Add related persons
        if 'relations' in contact:
            start_idx = add_x_attribute_relations(contact, vcf_content, start_idx)
                
        # Add significant dates
        if 'events' in contact:
            start_idx = add_x_attribute_significant_dates(contact, vcf_content, start_idx)
        
        vcf_content.append("END:VCARD")
    
    return "\n".join(vcf_content)

# Function to save VCF content to a file
def save_to_vcf(contacts, filename):
    vcf_content = generate_vcf(contacts)
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        f.write(vcf_content)

# Main function
def main():
    service = get_service()
    contacts = fetch_contacts(service)
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M')
    filename = f'contacts_{timestamp}.vcf'
    save_to_vcf(contacts, filename)

if __name__ == '__main__':
    main()
