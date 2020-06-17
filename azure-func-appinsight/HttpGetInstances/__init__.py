import logging

import azure.functions as func

 # tools.update({'project': name,
      #                'tools':
      #               {'sonarqube': 
      #                 {
      #                   'id': '1',
      #                   'toolname': 'sonarqube',
      #                   'status': 'warning',
      #                   'state' : True,
      #                   'instances':{
      #                     'sonarVuln':{
      #                        "state":True,
      #                        "status":"Success"
      #                     },
      #                     'sonarCode':{
      #                        "state":True,
      #                        "status":"Success"
      #                     },
      #                     'sonarCov':{
      #                        "state":True,
      #                        "status":"Warning"
      #                     }
      #                   }
      #                 },
      #                 'application-insights':{
      #                   'id': '2',
      #                   'toolname': 'application insights',
      #                   'status': 'warning',
      #                   'state' : True,
      #                   'instances':{
      #                     'SonarVuln':{
      #                        "state":True,
      #                        "status":"Success"
      #                     },
      #                     'SonarCode':{
      #                        "state":True,
      #                        "status":"Success"
      #                     },
      #                     'SonarCov':{
      #                        "state":True,
      #                        "status":"Warning"
      #                     }
      #                   }
      #                 }
      #               }
      #             }
      #  )

from azure.cosmos import CosmosClient

from .. import family
from .. import constants

client = CosmosClient(constants.DB_ENDPOINT, constants.DB_KEY)

database = client.get_database_client(constants.DB_DATABASE_ID)
container = database.get_container_client(constants.DB_CONTAINER_ID)
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    project = str(req.params.get('project'))
    instance_name = str(req.params.get('instance_name'))
    print(instance_name)
    
    tools = '['

    #sql = 'SELECT  distinct VALUE {"project": c.project,"tools":{toolnaam:c.toolname,status:\'warning\',state:\'true\',instances:ARRAY(SELECT VALUE {instancename:t.propertyname,\'state\':\'true\',\'status\':\'Succes\'} FROM t in c.properties) }}  FROM c  JOIN n IN (SELECT value  ARRAY(SELECT t FROM t in c.properties)) where c.project = \''+name+'\';
    #sql = "SELECT distinct VALUE {'project': c.project,id:c.id,toolname:c.toolname,status:'Warning',state:'true',instances:ARRAY(SELECT VALUE {name:t.propertyname,'state':'true','status':'Warning'} FROM t in c.properties) }  FROM c JOIN n IN (SELECT value  ARRAY(SELECT t FROM t in c.properties)) where c.project = '"+project+"'"
    if  instance_name != 'None':
        sql = 'SELECT value d FROM Families f JOIN c IN f.tools join d IN c.instances WHERE f.project = \''+project+'\' and d.instance_name  = \''+instance_name +'\''
    else:
        sql = 'SELECT* FROM c where c.project = \'' + project + '\''
    print(sql)

    queryresult = container.query_items(query=sql, enable_cross_partition_query=True)
    print(queryresult)

    for item in queryresult:
      tools += json.dumps(item) + ','
    tools = tools[:-1];
    tools += ']';
    
    
     
    # print(tools)
    # Result = json.dumps(tools)
    
        
    return func.HttpResponse(tools)
