from fastapi import FastAPI
from fastapi import FastAPI, Request, Header, Response, Form, Depends
from fastapi.staticfiles import StaticFiles
from typing import Optional, List
import json

import os.path

SERVER_DOMAIN = os.environ['VIRTUAL_HOST']
SERVER_URL = "https://" + SERVER_DOMAIN

DIR = os.path.dirname(__file__)

app = FastAPI()
app.mount("/static", StaticFiles(directory=os.path.join(DIR, "static")), name="static")

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Instances this instance is aware of
@app.get("/api/v1/instance/peers")
async def subscribe(request: Request):
    return [SERVER_URL]

def get_context():
    return ["https://www.w3.org/ns/activitystreams",
    SERVER_URL + "/schemas/litepub-0.1.jsonld",
    {
        "@language":"und"
    }]

# Example response: curl https://hayu.sh/users/guysoft  -H "Accept: application/json"
@app.get("/group/{id}")
async def group_page(request: Request, id: str):
    return_value = {
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    SERVER_DOMAIN + "/schemas/litepub-0.1.jsonld",
    {
      "@language": "und"
    }
  ],
  "id": SERVER_URL + "/group/aaa",
  "type": "Person",
  "following": SERVER_URL + "/group/aaa/following",
  "followers": SERVER_URL + "/group/aaa/followers",
  "inbox": SERVER_URL + "/group/aaa/inbox",
  "outbox": "AA",
  "featured": SERVER_URL + "/group/aaa/featured",
  "preferredUsername": "aaa",
  "name": "aaa",
  "summary": "aaa",
  "url": SERVER_URL + "/group/aaa",
  "publicKey": {
    "id": SERVER_URL + "/group/aaa#main-key",
    "owner": SERVER_URL + "/aaa",
    "publicKeyPem": "-----BEGIN RSA PUBLIC KEY-----\nMIIBCgKCAQEAyyR4y6GYCJ3DBxguFaX/zhGEc8KE4uKd/zbWpOlbz7TfTbQZaaNg\n9AYP04uFQ3W+nn18B7Y7RmNeRbKvHhyy1/nmMD3AFG11sNFLOfgRC7QtwskIbYfB\nd7gO9K5GnzSaF/iciyLZuyacGgSXBSUQ4GJ3K/sEUgHVZTnOMRDA+U8jK6nSXGnb\nYMLKhtMz3XRLN8Nq1vEIqQL9knRDAOZB7zteadPgHwByO7wcCpVgNtbFGWEJnUb5\nrAWcIaOA8NopFVR8h97Ova6zurpKPM1yetdmGFbmDynMtMZUAa4Nu149azJy07N2\nD7xaLejJaJVUGxkN6QI8axvdODqwk8ewbwIDAQAB\n-----END RSA PUBLIC KEY-----\n"
  },
  "tag": [],
  "attachment": [],
  "endpoints": {
    "oauthAuthorizationEndpoint": SERVER_URL + "/oauth/authorize",
    "oauthRegistrationEndpoint": SERVER_URL + "/api/v1/apps",
    "oauthTokenEndpoint": SERVER_URL + "/oauth/token",
    "sharedInbox": SERVER_URL + "/inbox",
    "uploadMedia": SERVER_URL + "/api/ap/upload_media"
  },
  "icon": {
    "type": "Image",
    "url": SERVER_URL + "/static/default_group_icon.png"
  },
  "image": {
    "type": "Image",
    "url": SERVER_URL + "/static/default_group_icon.png"
  },
  "manuallyApprovesFollowers": False,
  "discoverable": False
}
    
    response = Response(content=json.dumps(return_value), media_type="application/activity+json")
    return response

# Pleroma and Mastodon return this and search it, so I copied
@app.get("/.well-known/host-meta")
async def well_known(request: Request):
    data = """<?xml version="1.0" encoding="UTF-8"?>
<XRD xmlns="http://docs.oasis-open.org/ns/xri/xrd-1.0">
  <Link rel="lrdd" template=""" + SERVER_URL + """/.well-known/webfinger?resource={uri}"/>
</XRD>
    """
    response = Response(content=str(data), media_type="application/xrd+xml")
    return response

# Pleroma and Mastodon return this and search it, so I copied
@app.get("/group/{id}/featured")
async def group_featured(request: Request, id: str):
    orderedItems = []
    data = {
        "@context": get_context(),
        "id": SERVER_URL + "/group/" + id,
        "orderedItems": orderedItems,
        "totalItems": len(orderedItems),
        "type": "OrderedCollection"
    }

    response = Response(content=str(data), media_type="application/jrd+json")
    return response

# Example response: curl https://hayu.sh/.well-known/webfinger?resource=acct:guysoft@hayu.sh
# Doc https://docs.joinmastodon.org/spec/webfinger/
@app.head("/.well-known/webfinger")
@app.get("/.well-known/webfinger")
async def webfinger(request: Request, resource: str):
    return_value = {
  "aliases": [
    SERVER_URL + "/group/aaa"
  ],
  "links": [
    {
      "href": SERVER_URL + "/group/aaa",
      "rel": "self",
      "type": "application/activity+json"
    },
    {
      "href": SERVER_URL + "/group/aaa",
      "rel": "http://webfinger.net/rel/profile-page",
      "type": "text/html"
    },
    {
      "rel": "http://ostatus.org/schema/1.0/subscribe",
      "template": SERVER_URL + '/ostatus_subscribe?acct={uri}'
    }
  ],
  "subject": "acct:aaa@" + SERVER_DOMAIN
  }
    response = Response(content=str(json.dumps(return_value)), media_type="application/jrd+json; charset=utf-8")
    return response
