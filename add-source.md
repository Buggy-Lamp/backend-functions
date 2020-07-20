
# Databron toevoegen

## Back-end
Voor de back-end/ server wordt er gebruik gemaakt van Python.

Bij het calculeren van de kleur voor de lamp zal de back-end over alle ingestelde instanties itereren. Over deze iteraties zal de back-end het kleuren gewicht vergelijken. De meest zwaar wegende kleur zal als overzicht kleur worden gekozen; dit is gelijk aan de kleur van de lamp. 

Voorbeeldje:
- Property A heeft een kleurgewicht van 1
- Property B heeft een kleurgewicht van 0

Dan geld: `A > B` en zal de kleur van property A worden overgenomen.

#### File structuur
Voordat we een bron toevoegen is het handig om te weten hoe de file structuur eruit ziet.
```
. 
+-- HttpCalcState
|	+-- __init__.py  					-> Deze class wordt uitgevoerd vanuit Azure
+-- Http<functienaam>  					-> Deze mappen zijn voor dit niet relevant
+-- ToolServices
|	+-- Application insights
|	|	+-- __init__.py  				-> Dit is de entry-point voor de bron properties van Application Insights
|	|	+-- handler_<propertynaam>.py
|	+-- Sonarqube
|	|	+-- __init__.py  				-> Dit is de entry-point voor de bron properties van Sonarqube
|	|	+-- handler_<propertynaam>.py
|	+-- __init__.py  					-> Dit is de entry-point class voor het calculeren van de kleur
|	+-- application_insights.py  		-> Hier wordt Application Insights gecalculeerd
|	+-- sonarqube.py  					-> Hier wordt Sonarqube gecalculeerd
|	+-- util.py  						-> Dit is een helper class voor het bepalen van de kleur
```

### Nieuw bron (Sonarqube)
Als we dan een nieuwe bron willen toevoegen en de huidige structuur willen behouden moeten we ieder geval twee dingen doen. 
- Map aanmaken in `ToolServices` met de naam `<Tool Name>`
	-> Bijvoorbeeld `Sonarqube`

- Python bestand aan maken in `ToolServices` met de naam `<Tool Name>.py`
	-> Bijvoorbeeld `sonarqube.py`

#### Boilerplate code
In het Python bestand `<Tool Name>.py` (bijvoorbeeld `sonarqube.py`) kan dan de volgende boilerplate code worden geplaatst.
```python
from .util import find_color, parse_error, find_threshold


def single_instance(instance_setting) -> dict or None:  
	instance_data = {  
		'color': 'gray',  
		'color_weight': -1,  
		'properties': {}  
	}

	# Start here with calling property handlers

	# End here with calling property handlers

	if len(instance_data['properties']) == 0:  
		del instance_data['properties']  

	if 'properties' in instance_data:  
		color, color_weight = find_color(instance_data['properties'])  
		instance_data['color'] = color  
		instance_data['color_weight'] = color_weight  

	return instance_data

def process_tool(settings) -> dict or None:  
	if len(settings) == 0:  
		return None  

	settings = settings[0]  

	return_data = {}  
	for instance in settings['instances']:  
		return_data[instance['instance_name']] = single_instance(instance)  

	color, color_weight = find_color(return_data)  
	return_data['color'] = color  
	return_data['color_weight'] = color_weight  

	return return_data
```

Bovenstaande code is vooral een boilerplate om over alle instellingen te itereren en voor elke iteratie de kleur te bepalen. Functie `process_tool()` is dan de eerste functie die afgevuurd zal worden. 

#### Data ophalen voor een enkele instantie
Verder staat in functie `single_instance()` een code blok hoe propertie handlers moeten worden verwerkt. Om de instellingen op te halen voor een property kan de volgende code blok worden toegevoegd.
```python
<PROPERTY_NAME>_settings = list(filter(lambda x: x['property_name'] == <PROPERTY_NAME>, instance_setting['properties']))
if len(<PROPERTY_NAME>_settings) > 0:  
    <PROPERTY_NAME>_settings = <PROPERTY_NAME>_settings[0]  
else:  
    <PROPERTY_NAME>_settings = None

if <PROPERTY_NAME>_settings:
	data = <PROPERTY_FUNCTIE>()
	
	threshold_target = find_threshold(<PROPERTY_NAME>_settings['thresholds'], data ['current_tresholds_state'], multiplier=2)
	instance_data['properties'][<PROPERTY_NAME>] = threshold_target
```

In bovenstaande code wordt de juiste instellingen opgehaald voor een bepaalde property.
Bovenstaande code bevat verder de volgende placeholders:
| Placeholder | Voorbeeld | Betekenis |
| -- | -- | ----- |
| <PROPERTY_NAME> | quality_gate | De naam van de property. |
| <PROPERTY_NAME>_settings | quality_gate_settings | Deze variabele heeft alle instellingen van de property quality_gate |
| <PROPERTY_FUNCTIE> | get_quality_gate_data() | Deze functie haalt de data op dat bij deze property hoort. Denk aan een REST-API call naar een service. |

De functie die de property data ophaalt zal dan door een zoekfunctie gaan genaamd `find_threshold()`. De find_threshold functie zal dan de bijbehorende threshold teruggeven. Verder heeft de find_thresholds functie de volgende parameters:
| Parameter | Uitleg | Verplicht |
| - | --- | - |
| thresholds | Deze parameter heeft alle threshold mogelijkheden. Bijvoorbeeld bij 0 excepties groen, 1 oranje etc. | Ja |
| target | De target integer die word gematched aan de threshold. Bijvoorbeeld als er 1 exceptie is zal de target parameter 1 doorgeven | Ja |
| multiplier | Hiermee kan het gewicht van de kleur mee worden vermenigvuldigd. In een situatie waar maar twee thresholds zijn is een multiplier van 2 nodig. Bij een normale situatie waar drie thresholds zijn is een multiplier van 1 nodig. | Nee |

Het is belangrijk om de `find_thresholds()` functie de juiste parameters mee te geven; zeker als er wordt afgeweken van de normale situatie waar drie thresholds zijn.



#### Resultaat
Als we alles combineren krijgen we dan een Python bestand dat er als volgt uitziet.
```python
from .util import find_color, parse_error, find_threshold


def single_instance(instance_setting) -> dict or None:  
	instance_data = {  
		'color': 'gray',  
		'color_weight': -1,  
		'properties': {}  
	}

	# Start here with calling property handlers
	
	<PROPERTY_NAME>_settings = list(filter(lambda x: x['property_name'] == <PROPERTY_NAME>, instance_setting['properties']))
	if len(<PROPERTY_NAME>_settings) > 0:  
	    <PROPERTY_NAME>_settings = <PROPERTY_NAME>_settings[0]  
	else:  
	    <PROPERTY_NAME>_settings = None

	if <PROPERTY_NAME>_settings:
		data = <PROPERTY_FUNCTIE>
		
		threshold_target = find_threshold(<PROPERTY_NAME>_settings['thresholds'], data ['current_tresholds_state'], multiplier=2)
		instance_data['properties'][<PROPERTY_NAME>] = threshold_target
	
	# End here with calling property handlers

	if len(instance_data['properties']) == 0:  
		del instance_data['properties']  

	if 'properties' in instance_data:  
		color, color_weight = find_color(instance_data['properties'])  
		instance_data['color'] = color  
		instance_data['color_weight'] = color_weight  

	return instance_data

def process_tool(settings) -> dict or None:  
	if len(settings) == 0:  
		return None  

	settings = settings[0]  

	return_data = {}  
	for instance in settings['instances']:  
		return_data[instance['instance_name']] = single_instance(instance)  

	color, color_weight = find_color(return_data)  
	return_data['color'] = color  
	return_data['color_weight'] = color_weight  

	return return_data
```
