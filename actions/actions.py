# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
    """A dictionary to map required slots to
        - an extracted entity
        - intent: value pairs
        - a whole message
        or a list of them, where a first match will be picked"""

    return {
        "age": [
            self.from_entity(entity="integer", role="age"),
            self.from_entity(entity="integer"),
        ],
        "weight": [
            self.from_entity(entity="integer", role="weight"),
            self.from_entity(entity="integer"),
        ],
        "height": [
            self.from_entity(entity="integer", role="height"),
            self.from_entity(entity="integer"),
        ],
    }
   
def validate_age(
    self,
    value: Text,
    dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any],
) -> Dict[Text, Any]:
    """Validate age value."""
    
    requested_slot = tracker.get_slot("requested_slot")
    age_slot = tracker.get_slot("age")

    if requested_slot == "age":
        return {"age": value}
    elif age_slot:
        return {"age": age_slot}
    else:
        return {"age": None}

def validate_weight(
    self,
    value: Text,
    dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any],
) -> Dict[Text, Any]:
    """Validate weight value."""
    
    requested_slot = tracker.get_slot("requested_slot")
    weight_slot = tracker.get_slot("weight")

    if requested_slot == "weight":
        return {"weight": value}
    elif weight_slot:
        return {"weight": weight_slot}
    else:
        return {"weight": None}

def validate_height(
    self,
    value: Text,
    dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any],
) -> Dict[Text, Any]:
    """Validate height value."""
    
    requested_slot = tracker.get_slot("requested_slot")
    height_slot = tracker.get_slot("height")

    if requested_slot == "height":
        return {"height": value}
    elif height_slot:
        return {"height": age_slot}
    else:
        return {"height": None}
