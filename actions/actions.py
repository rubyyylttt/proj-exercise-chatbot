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
from typing import Any, Text, Dict, List

from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

food_db = {
    'Pineapple Bun':350,
    'Chicken Breast':155,
    'Brown Rice':100,
    'Bread':90,
    'Ramen':500
}

workout_db = {
    'leg':['Leg press 2*15 reps \n Leg extension 2*15 reps \n Seated leg curl 2*15 reps \n Standing calf raises 2*15 reps',\
        'Barbell squats 3*10 reps \n Romanian deadlifts 3*10 reps \n Leg press - 2*15 reps \n Seated calf raises 2*15 reps',\
            'Bulgarian split squats 3*10 reps \n Barbell hip thrusts 3*10 reps \n Leg press - 3*15 reps \n Seated calf raises 2*15 reps',\
                'Barbell front squats - 4*8 reps \n Barbell lunges 4*8 reps \n Leg press - 3*15 reps \n Standing calf raises 3*15 reps',\
                    'Barbell back squats 5*5 reps \n Deadlifts 5*5 reps \n Leg press 4*15 reps \n Donkey calf raises 3*20 reps'],
    'arm':['Bicep curls with dumbbells 2*15 reps \n Tricep extensions with dumbbells - 2*15 reps \n Standing dumbbell curls 2*15 reps \n Overhead tricep extensions with dumbbells 2*15 reps',\
        'Hammer curls with dumbbells 3*12 reps \n Close-grip bench press with barbell 3*12 reps \n Cable bicep curls 3*12 reps \n Tricep pushdowns with cable machine 3*12 reps',\
            'Barbell curls 4*10 reps \n Skull crushers with EZ bar 4*10 reps \n Preacher curls with dumbbells 4*10 reps \n Cable tricep extensions with rope attachment 4*10 reps',\
                '',''],
    'back':['','','','',''],
    'hip':['','','','',''],
    'core':['','','','',''],
    'cardio':['','','','','']
}

class IntensityCalculation(Action):

    def name(self) -> Text:
        return "action_calculate_intensity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        height = tracker.get_slot("height")
        height = int(height)
        height = height/100

        weight = tracker.get_slot("weight")
        weight = int(weight)

        exerciseFreq = tracker.get_slot("exercise_freq")
        exercise_freq = int(exercise_freq)

        BMI = weight/(height*height)
        if not (height and weight and exerciseFreq):
            dispatcher.utter_message(text="There is not enough info to calculate yet...")
        else:
            height = tracker.get_slot("height")
            height = int(height)
            height = height/100
  
            weight = tracker.get_slot("weight")
            weight = int(weight)

            BMI = weight/(height*height)
            if (exercise_freq <= 1):
                intensity = 2
            elif exercise_freq <3:
                intensity = 3
            else:
                intensity = 4
            if BMI < 18.5 or BMI > 25:
                intensity -= 1
                dispatcher.utter_message(text="i would suggest a mild workout intensity level {intensity}, is there any body parts you want to train on?")
            else:
                intensity += 1
                dispatcher.utter_message(text="I would suggest a workout plan of intensity {intensity}, tell me a part you want to train.")
        return[]                


