import csv, hashlib, io, json, math, re
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from .validation import validate_input, http_url, unique

def now(): return datetime.now(timezone.utc).isoformat()
def validate(data,records): return initialize(validate_input(data,CONFIG['example']),records)

def initialize(row,records):
    if row['environment']!='dev': raise ValueError('Releases must start in dev')
    unique(records,row,['service','release_version'])
    return dict(row,history=['Created in dev'],approved=False)
def summary(rows): return {environment:sum(r['environment']==environment for r in rows) for environment in ['dev','staging','production']}
def transition(row,action):
    if action=='approve' and row['environment']=='staging' and not row.get('approved'): return dict(row,approved=True,history=row['history']+['Approved in staging'])
    if action!='promote' or row['environment']=='production': raise ValueError('Unsupported release transition')
    if row['environment']=='staging' and not row.get('approved'): raise ValueError('Approve before production promotion')
    environment='staging' if row['environment']=='dev' else 'production'
    return dict(row,environment=environment,history=row['history']+['Promoted to '+environment])
