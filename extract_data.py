from pyzotero import zotero
from copy import deepcopy
from typing import Any, List
import requests
import smtplib
from email.mime.text import MIMEText


class ZoteroWrapper:
    def __init__(self, user_account_id: int, user_type: str, access_token: str):
        self.user_account_id = user_account_id
        self.user_type = user_type
        self.access_token = access_token
        self.client = zotero.Zotero(
            self.user_account_id,
            self.user_type,
            self.access_token
        )
    
    def query(self) -> List[Any]:
        return self.client.top(limit=5)
    
    def duplicate_data(self, items: List[Any], multiplier: int) -> List[Any]:
        larger_items = [deepcopy(i) for _ in range(int(multiplier)) for i in items]
        return larger_items
    #check validity of link
    def is_url_valid(self, url: str) -> bool:
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
        try:
            response = requests.get(url, headers=headers, timeout=10)  # Increase timeout to 10 seconds
            # Checking if status_code is between 200 and 299 which are typically considered successful
            return 200 <= response.status_code < 300
        except requests.RequestException:
            return False
    def check_links_validity(self, items: List[Any]) -> List[bool]:
        """
        Returns a list of boolean values indicating whether each URL in the items is valid or not.
        """
        return [self.is_url_valid(item['data']['url']) for item in items]
    
USER_ID = 12354040
USER_TYPE = 'user'
ACCESS_TOKEN = '9sPrZSh9r4VKeF7zO8Aau8qI'

z = ZoteroWrapper(
    USER_ID,
    USER_TYPE,
    ACCESS_TOKEN
)

items = z.query()
dummy_item = {
    'data': {
        'title': 'Dummy Title',
        'url': 'http://www.invalidlink1234567890.com',
        'tags': [{'tag': 'Dummy Tag'}]
    }
}

items.append(dummy_item)
validities = z.check_links_validity(items)

# items = z.duplicate_data(items, 1e4)

# we've retrieved the latest five top-level items in our library
# we can print each item's item type and ID
for item, valid in zip(items, validities):
    tag_names = [tag['tag'] for tag in item['data']['tags']]
    status = "Valid" if valid else "Invalid"
    print('Title: %s | URL: %s| Status: %s| Tags: %s' % (item['data']['title'], item['data']['url'], status, ', '.join(tag_names)))