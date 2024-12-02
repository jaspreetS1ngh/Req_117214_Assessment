import json
import paho.mqtt.client as mqtt
import logging
from config import Config

# Configuring logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MQTT Broker Details from Config.py
MQTT_BROKER = Config.MQTT_BROKER
MQTT_PORT = Config.MQTT_PORT
input_topic = Config.MQTT_TOPIC_INPUT
output_topic = Config.MQTT_TOPIC_OUTPUT

def calculate_supplement(input_data):
    """
    Calculates the winter supplement based on input data.
    """
    try:
        # Eligibility check: Ensuring family unit is eligible for December
        is_eligible = input_data.get('familyUnitInPayForDecember', False)

        # Base amount depending on family composition
        base_amount = 0.0
        children_amount = 0.0

        # Logic for base amount based on family composition
        family_composition = input_data.get('familyComposition')
        number_of_children = input_data.get('numberOfChildren', 0)
        
        if (is_eligible==False):
            base_amount=0.0
            children_amount = 0.0
        elif family_composition == "single" and number_of_children == 0:
            base_amount = 60.0  # Single person with no children
        elif family_composition == "couple" and number_of_children == 0:
            base_amount = 120.0  # Childless couple
        elif (family_composition == "single"  and number_of_children) > 0:
            base_amount = 60  # Single with children
            children_amount = number_of_children * 20.0  # $20 per child
        elif (family_composition == "couple" and number_of_children > 0):
            base_amount = 120.0  # couple with children
            children_amount = number_of_children * 20.0 
        else:
            base_amount = 0.0  # no supplement

        # Supplement calculation, based on eligibility
        supplement_amount = (base_amount if is_eligible else 0.0) + (children_amount if is_eligible else 0.0)

        # Return the calculated result
        return {
            "id": input_data.get('id', ''),
            "isEligible": is_eligible,
            "baseAmount": base_amount,
            "childrenAmount": children_amount if is_eligible else 0.0,
            "supplementAmount": supplement_amount
        }

    except Exception as e:
        print(f"Error in supplement calculation: {e}")
        return {}


def on_message(client, userdata, msg):
    """
    Callback function to process incoming messages from the input topic.
    """
    try:
        # parse the incoming message payload
        input_data = json.loads(msg.payload.decode())
        logger.info(f"Received message: {input_data}")
        
        # Process the input data and calculate the supplement
        result = calculate_supplement(input_data)
        
        if result:
            # Publish the result to the output topic
            client.publish(output_topic, json.dumps(result))
            logger.info(f"Published result: {result}")
        else:
            logger.error("Error processing input data, no result published.")
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding message: {e}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")

def on_connect(client, userdata, flags, rc):
    """
    Callback function when connected to the broker.
    """
    if rc == 0:
        logger.info("Successfully connected to MQTT broker.")
        # Subscribe to the input topic after successful connection
        client.subscribe(input_topic, qos=0)
        logger.info(f"Subscribed to topic: {input_topic}")
    else:
        logger.error(f"Failed to connect with return code {rc}")

def on_subscribe(client, userdata, mid, granted_qos):
    """
    Callback function for subscription confirmation.
    """
    logger.info(f"Subscribed to topic {input_topic} with QoS {granted_qos}")

def start_mqtt_client():
    """
    Initializes the MQTT client and starts listening for incoming messages.
    """
    # Create an MQTT client instance
    client = mqtt.Client("winter_supplement_engine", protocol=mqtt.MQTTv311)
    
    # Setting the connection and message callbacks
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe 
    
    # Connecting to the MQTT broker
    logger.info("Connecting to the MQTT broker...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    # Starting the MQTT client loop to listen for incoming messages
    client.loop_forever()
