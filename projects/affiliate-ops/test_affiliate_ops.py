import os, tempfile, unittest
from pathlib import Path
import affiliate_ops as a
import creators_api
class Tests(unittest.TestCase):
 def test_creators_api_is_explicitly_disabled_without_credentials(self):
  old={k:os.environ.pop(k,None) for k in ('AMAZON_CREATORS_CREDENTIAL_ID','AMAZON_CREATORS_CREDENTIAL_SECRET','AMAZON_PARTNER_TAG')}
  try:
   client=creators_api.CreatorsAPI()
   self.assertFalse(client.ready())
   with self.assertRaisesRegex(creators_api.NotConfigured,'AMAZON_API_NOT_CONFIGURED'): client.token()
  finally:
   for k,v in old.items():
    if v is not None: os.environ[k]=v

 def test_builds_tagged_url_and_removes_fragment(self):
  self.assertEqual(a.safe_affiliate_url('https://www.amazon.com/dp/0140280197?ref_=x#reviews','example-20'),'https://www.amazon.com/dp/0140280197?ref_=x&tag=example-20')
 def test_rejects_non_amazon_destination(self):
  with self.assertRaises(ValueError): a.safe_affiliate_url('https://evil.example/item','example-20')
 def test_schema_keeps_only_tax_status_and_secure_reference(self):
  old=a.DB
  try:
   with tempfile.TemporaryDirectory() as d:
    a.DB=Path(d)/'t.db'; db=a.connect(); cols={r[1] for r in db.execute('pragma table_info(tax_profiles)')}
    self.assertNotIn('ssn',cols); self.assertNotIn('tin',cols); self.assertIn('secure_document_ref',cols)
  finally: a.DB=old
if __name__=='__main__': unittest.main()
