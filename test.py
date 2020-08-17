import json

from azure_func.Model import *

props = [Property(name='exceptions'), Property(name='exceptions2', color='green', color_weight=2)]
instances = [Instance(name='webwinkel', properties=props)]
tools = [Tool(name='application_insights', instances=instances)]

project = Project(name='template-SmartHotel360', tools=tools)

project.process_project_color()
print(json.dumps(project.serialize()))
