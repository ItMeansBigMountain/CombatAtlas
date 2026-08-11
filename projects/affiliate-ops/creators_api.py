#!/usr/bin/env python3
"""Minimal server-side Amazon Creators API client; disabled until real credentials exist."""
from __future__ import annotations
import json, os, time, urllib.error, urllib.request

TOKEN_ENDPOINTS={'3.1':'https://api.amazon.com/auth/o2/token','3.2':'https://api.amazon.co.uk/auth/o2/token','3.3':'https://api.amazon.co.jp/auth/o2/token'}
BASE='https://creatorsapi.amazon/catalog/v1'
class NotConfigured(RuntimeError): pass
class CreatorsAPI:
 def __init__(self):
  self.client_id=os.getenv('AMAZON_CREATORS_CREDENTIAL_ID','').strip()
  self.secret=os.getenv('AMAZON_CREATORS_CREDENTIAL_SECRET','').strip()
  self.version=os.getenv('AMAZON_CREATORS_CREDENTIAL_VERSION','3.1').strip()
  self.marketplace=os.getenv('AMAZON_MARKETPLACE','www.amazon.com').strip()
  self.partner_tag=os.getenv('AMAZON_PARTNER_TAG','').strip()
  self._token=''; self._expires=0.0; self._last_call=0.0
 def ready(self): return bool(self.client_id and self.secret and self.partner_tag and self.version in TOKEN_ENDPOINTS)
 def token(self):
  if not self.ready(): raise NotConfigured('AMAZON_API_NOT_CONFIGURED')
  if time.time()<self._expires-60: return self._token
  body=json.dumps({'grant_type':'client_credentials','client_id':self.client_id,'client_secret':self.secret,'scope':'creatorsapi::default'}).encode()
  req=urllib.request.Request(TOKEN_ENDPOINTS[self.version],data=body,headers={'Content-Type':'application/json'},method='POST')
  with urllib.request.urlopen(req,timeout=30) as r: result=json.load(r)
  self._token=result['access_token']; self._expires=time.time()+int(result.get('expires_in',3600)); return self._token
 def call(self,operation,payload):
  now=time.monotonic(); delay=1-(now-self._last_call)
  if delay>0: time.sleep(delay)
  body={'marketplace':self.marketplace,'partnerTag':self.partner_tag,**payload}
  req=urllib.request.Request(f'{BASE}/{operation}',data=json.dumps(body).encode(),headers={'Authorization':'Bearer '+self.token(),'Content-Type':'application/json','x-marketplace':self.marketplace},method='POST')
  try:
   with urllib.request.urlopen(req,timeout=45) as r: result=json.load(r)
  finally: self._last_call=time.monotonic()
  return result
 def get_items(self,asins,resources=None):
  if not 1<=len(asins)<=10: raise ValueError('GetItems accepts 1..10 ASINs per request')
  return self.call('getItems',{'itemIds':asins,'itemIdType':'ASIN','resources':resources or ['images.primary.medium','itemInfo.title','offersV2']})
if __name__=='__main__':
 c=CreatorsAPI(); print(json.dumps({'configured':c.ready(),'marketplace':c.marketplace,'partner_tag_present':bool(c.partner_tag)}))
