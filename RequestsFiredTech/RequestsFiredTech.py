
import os
import sys
sys.path.append("C:\\ManageEngine\\ServiceDesk\\integration\\custom_scripts")

from RequestsFiredTech_Func import * 
from config_variables import logs_dir 

logging.basicConfig(level=logging.INFO, 
                    filename=f"{logs_dir}/{os.path.basename(__file__).split('.')[0]}.log",filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")

###################### Find Requests ##############################

""" 
Find_Req() has builtin criteria:
status.name not in [Closed,Resolved] 
and ( technician.name contains "sql_id:" or start with "х ")  

Then in each loop request dict add to requests_array list
"""
requests_array = req_massive(start_index=1)


###################### Action for each Req ##############################

for request in requests_array:

    Message = f"Внимание!<br>\
        Данная заявка была снята с уволившегося исполнителя {request['TechName']}.<br>\
        Необходимо уточнить руководителя уволившегося исполнителя и переназначить на него заявку.<br>\
        Нового исполнителя необходимо уведомить в корпоративном мессенджере."
    
    if request['ReqTemplate'] in ["Change Proposal"]:
        Proposal_to_Incident(request['ReqID'])
        ReqToProcessing(request['ReqID'])
        Add_Note(request['ReqID'],Message)
    if request['ReqTemplate'] in ["Default Request"]:
        ReqToProcessing(request['ReqID'])
        Add_Note(request['ReqID'],Message)
    if request['ReqTemplate'] in ["Mass Incident"]:
        MassFiredTech(request['ReqID']) 
        Add_Note(request['ReqID'],Message) 

###################### Tech to User ##############################

ClearLicTechs = []
RemoveTechs = []

for request in requests_array:
    if request['TechID'] not in ClearLicTechs:
        Tech = {    
            'TechID':request['TechID'],
            'TechName': request['TechName']
            }
        ClearLicTechs.append(request['TechID'])
        RemoveTechs.append(Tech)
    else:
        pass

for Tech in RemoveTechs:
    TechToUser(Tech['TechID'], Tech['TechName'])
    
