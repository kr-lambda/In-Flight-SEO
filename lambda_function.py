import re
from fetch_html import fetch_html
from transform_state import transform_state
from helpers import structure_headers
from _rules import rules
from _exclusions import exclusions
from _config import bucket_name, index_key

def lambda_handler(event, context):
    request = event["Records"][0]["cf"]["request"]
    
    for pattern in exclusions:
        if re.match(pattern, request["uri"]):
            return request
        
    for rule in rules: 
        if not re.match(rule["pattern"], request["uri"]):
            continue
        state = fetch_html(bucket_name, index_key)
        state['request'] = request
        state["response_headers"] = {"content-type": "text/html"}
        status = state["status"]
        if status>= 200 and status < 400:
            transform_state(state, rule)
        return {
            "status": state["status"],
            "body": state["html"],
            "headers": structure_headers(state["response_headers"])
        }
        
    return request
