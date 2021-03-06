import uuid

from azure.cosmos import CosmosClient

from .constants import DB_KEY, DB_ENDPOINT, DB_DATABASE_ID


def generateid(req_body):
    req_body['id'] = str(uuid.uuid4())
    return req_body


def get_container(container_name):
    client = CosmosClient(DB_ENDPOINT, DB_KEY)
    database = client.get_database_client(DB_DATABASE_ID)
    container = database.get_container_client(container_name)
    return container


def update(container, requestinfo):
    project = requestinfo['project']
    sql = "select * from c where c.project = '" + project + "'"
    # print(sql)
    currentitem = list(container.query_items(query=sql, enable_cross_partition_query=True))
    if len(currentitem) == 0:
        requestinfo = generateid(requestinfo)
        return container.create_item(body=requestinfo)
    else:
        # print(requestinfo);
        newtoollist = requestinfo['tools'][0]
        newtoolname = newtoollist['tool_name']
        newinstance = newtoollist['instances'][0]
        instance_name = newinstance['instance_name']

        instancecheck = 'SELECT d FROM projects f JOIN c IN f.tools join d IN c.instances WHERE f.project = \'' + project + '\' and d.instance_name  = \'' + instance_name + '\''
        instancecheck = len(list(container.query_items(query=instancecheck, enable_cross_partition_query=True)))

        toolcheck = 'SELECT c FROM projects f JOIN c IN f.tools WHERE f.project = \'' + project + '\' and c.tool_name = \'' + newtoolname + '\''
        toolcheck = len(list(container.query_items(query=toolcheck, enable_cross_partition_query=True)))

        if toolcheck == 0:
            toolcheck = True
        else:
            toolcheck = False

        if instancecheck == 0:
            instancecheck = True
        else:
            instancecheck = False
        currentitem = currentitem[0]
        if toolcheck:
            currentitem['tools'].append(newtoollist)
            return currentitem
        elif instancecheck:
            toolindex = findindex(newtoolname, currentitem['tools'], 'tool_name')
            currentitem['tools'][toolindex]['instances'].append(newinstance)
        else:
            toolindex = findindex(newtoolname, currentitem['tools'], 'tool_name')
            instanceindex = findindex(instance_name, currentitem['tools'][toolindex]['instances'], 'instance_name')
            currentitem['tools'][toolindex]['instances'][instanceindex] = newinstance;

        return container.upsert_item(body=currentitem)


def findindex(needle, itemslist, searchindex):
    for index, value in enumerate(itemslist, start=0):
        if needle == value[searchindex]:
            return index

    return type(itemslist)
