import logging

import azure.functions as func

import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = str(req.params.get('project'))
    tools = dict()
    tools.update({'project': name,
                   'tools':
                  {'sonarqube': 
                    {
                      'id': '1',
                      'toolname': 'sonarqube',
                      'status': 'warning',
                      'state' : True,
                      'instances':{
                        'sonarVuln':{
                           "state":True,
                           "status":"Success"
                        },
                        'sonarCode':{
                           "state":True,
                           "status":"Success"
                        },
                        'sonarCov':{
                           "state":True,
                           "status":"Warning"
                        }
                      }
                    },
                    'application-insights':{
                      'id': '2',
                      'toolname': 'application insights',
                      'status': 'warning',
                      'state' : True,
                      'instances':{
                        'SonarVuln':{
                           "state":True,
                           "status":"Success"
                        },
                        'SonarCode':{
                           "state":True,
                           "status":"Success"
                        },
                        'SonarCov':{
                           "state":True,
                           "status":"Warning"
                        }
                      }
                    }
                  }
                }
     )
    Result = json.dumps(tools)
    
        
    return func.HttpResponse(Result)
