import logging

import azure.functions as func

import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = str(req.params.get('project'))
    tools = dict()
    tools.update({'hu-todss':
                  {'Sonarqube': 
                    {
                      'id': '1',
                      'Status': 'warning',
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
                    },
                    'Application insights':{
                      'id': '2',
                      'Status': 'warning',
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
