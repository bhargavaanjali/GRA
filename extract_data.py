from pyzotero import zotero
from copy import deepcopy
from typing import Any, List

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

USER_ID = 12354040
USER_TYPE = 'user'
ACCESS_TOKEN = '9sPrZSh9r4VKeF7zO8Aau8qI'

z = ZoteroWrapper(
    USER_ID,
    USER_TYPE,
    ACCESS_TOKEN
)

items = z.query()
# items = z.duplicate_data(items, 1e4)

# we've retrieved the latest five top-level items in our library
# we can print each item's item type and ID
for item in items:
    tag_names = [tag['tag'] for tag in item['data']['tags']]
    print('Title: %s | URL: %s| Tags: %s' % (item['data']['title'], item['data']['url'], ', '.join(tag_names)))