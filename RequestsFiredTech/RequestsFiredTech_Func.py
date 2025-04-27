import requests
import json
import sys
sys.path.append("C:\\ManageEngine\\ServiceDesk\\integration\\custom_scripts")

import urllib3
import logging
import time

from config_secrets import ApiKey
from config_variables import SdpUri 

urllib3.disable_warnings()
##  проверить ключ и URL куда стучусь перед запуском
headers ={"authtoken":ApiKey}

def req_massive(start_index):
    if start_index == 1 :
        requests_array = []
    """ 
    Criteria:
    status.name not in [Closed,Resolved] 
    and ( technician.name contains "sql_id:" or start with "х ")  
    """
    input_data_dict = {
            "list_info": {
                "row_count": 100,
                "start_index": start_index,
                "sort_field": "subject",
                "sort_order": "asc",
                "get_total_count": True,
                "search_criteria": {
                    "field": "status.name",
                    "condition": "is not",
                    "values": [
                        "Closed",
                        "Resolved"
                    ],
                    "children": [
                        {
                            "field": "technician.name",
                            "condition": "contains",
                            "values": [
                                "sql_id:"
                            ],
                            "logical_operator": "AND"
                        },
                        {
                            "field": "technician.name",
                            "condition": "starts with",
                            "values": [
                                "х "
                            ],
                            "logical_operator": "OR"
                        }
                    ]
                }
            },
            "fields_required": [
                "id",
                "technician",
                "template"
            ]
        }

    url = f"{SdpUri}/api/v3/requests/"
    input_data = json.dumps(input_data_dict)
    params = {'input_data': input_data}

    """ response = requests.get(url,headers=headers,params=params,verify=False)
    json_answer = json.loads(response.content)
    print(json_answer["list_info"]["total_count"]) """
    try:
        response = requests.get(url,headers=headers,params=params,verify=False)
        json_answer = json.loads(response.content)
        request_count = json_answer["list_info"]["total_count"] 
        if json_answer["list_info"]["total_count"] > 200:
            logging.info(f"Too many requests found {request_count}")
            raise Exception
        if response.status_code not in [200,2000]:
            raise Exception
        #return json_answer
    except:
        logging.error(f"Can't fetch Requests.\r\n Response: {response.content}.\r\n Url: {url}\r\n Json: {input_data}")
        sys.exit()

    for object in json_answer["requests"]:
        request_info = {   'ReqID':object["id"],
                            'ReqTemplate':object["template"]["name"], 
                            'TechID':object["technician"]["id"],
                            'TechName': object["technician"]["name"] 
                    } 
        requests_array.append(request_info)

    if json_answer["list_info"]["has_more_rows"]:      
        time.sleep(1)
        req_massive(start_index+100)

    logging.info(f"Found {len(requests_array)} Requests")
    return requests_array

def Proposal_to_Incident (ReqID):
    url = f"{SdpUri}/api/v3/requests/{ReqID}" 
    input_data_dict = {
        "request": {
            "template": { "name": "Default Request" },
            "request_type": {"name": "Request"},
            "technician": None
            }
        }
    input_data = json.dumps(input_data_dict)
    params = {'input_data': input_data}
    try:
        response = requests.put(url,headers=headers,params=params,verify=False)
        if response.status_code not in [200,2000]:
            raise Exception
        logging.info(f"{ReqID} Move to Incident Success")
    except:
        logging.error(f"{ReqID} Don't moved to Incident.\r\n Response: {response}.\r\n Url: {url}\r\n Json: {input_data}")
        sys.exit()

def MassFiredTech (ReqID):
    url = f"{SdpUri}/api/v3/requests/{ReqID}"
    input_data_dict = {
        "request": {
            "technician": {"name":"Name, Name"}
            }
        }
    input_data = json.dumps(input_data_dict)
    params = {'input_data': input_data}
    try:
        response = requests.put(url,headers=headers,params=params,verify=False)
        if response.status_code not in [200,2000]:
            raise Exception
        logging.info(f"Mass {ReqID} reassigned")
    except:
        logging.error(f"Mass {ReqID} can't edited.\r\n Response: {response}.\r\n Url: {url}\r\n Json: {input_data}")
        sys.exit()

def ReqToProcessing (ReqID):
    url = f"{SdpUri}/api/v3/requests/{ReqID}"
    input_data_dict = {
    "request": {
        "status": { "name": "Processing" },
        "technician": None
        }
    }
    input_data = json.dumps(input_data_dict)	
    params = {'input_data': input_data}
    try:
        response = requests.put(url,headers=headers,params=params,verify=False)
        if response.status_code not in [200,2000]:
            raise Exception
        logging.info(f"{ReqID} Move to Processing Success")
    except:
        logging.error(f"{ReqID} Can't go to Processing.\r\n Response: {response}.\r\n Url: {url}\r\n Json: {input_data}")
        sys.exit()

def Add_Note (ReqID,Message):
    url = f"{SdpUri}/api/v3/requests/{ReqID}/notes"
    input_data_dict = {
    "note": {
        "description": f"{Message}"
        }
    }
    input_data = json.dumps(input_data_dict)	
    params = {'input_data': input_data}
    try:
        response = requests.post(url,headers=headers,params=params,verify=False)
        if response.status_code not in [200,201,2000]:
            raise Exception
        logging.info(f"{ReqID} Note added")
    except:
        logging.error(f"{ReqID} Can't add Note. {response.status_code}\r\n Response: {response.content}.\r\n Url: {url}\r\n Json: {input_data}")
        sys.exit()

def TechToUser(TechID, TechName):
    try:  
        url = f"{SdpUri}/api/v3/technicians/change_as_user?ids={TechID}"
        response = requests.put(url,headers=headers,verify=False)
        if response.status_code not in [200,2000]:
            raise Exception
        logging.info(f"Succesful clear Licence for: {TechName}")
    except:
        logging.error(f"License not Clear for: {TechName}")
        sys.exit()
