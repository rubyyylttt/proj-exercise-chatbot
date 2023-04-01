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
                'Incline bench dumbbell curls 5*8 reps \n Tricep dips 5*8 reps \n Concentration curls with dumbbell 5*8 reps \n Overhead dumbbell tricep extensions 5*8 reps',\
                    'Close-grip chin-ups 6*6 reps \n Close-grip push-ups 6*6 \n Alternating dumbbell curls with heavy weights 6*6 reps \n Tricep kickbacks with dumbbells 6*6 reps'],
    
    'back':['Lat pulldowns 2*15 reps \n Seated cable rows 2*15 reps \n Dumbbell rows 2*15 reps \n Back extensions 2*15 reps',\
        'T-bar rows 3*12 reps \n Single-arm dumbbell rows 3*12 reps \n Wide-grip lat pulldowns 3*12 reps \n Seated cable rows with V-bar attachment 3*12 reps',\
            'Barbell bent-over rows 4*10 reps \n Close-grip lat pulldowns 4*10 reps \n Cable face pulls 4*10 reps \n Hyperextensions 4*10 reps',\
                'Deadlifts 5*8 reps \n Weighted chin-ups 5*8 reps \n Cable rows with rope attachment 5*8 reps \n Wide-grip pull-ups 5*8 reps',\
                    'Rack pulls 6*6 reps \n Barbell rows with supinated grip 6*6 reps \n One-arm dumbbell rows with heavy weights 6*6 reps \n Weighted hyperextensions - 6*6 reps'],
    
    'hip':['Glute bridges 2*15 reps \n Clamshells 2*15 reps \n Standing leg lifts 2*15 reps \n Fire hydrants 2*15 reps',\
        'Cable kickbacks 3*12 reps \n Hip thrusts with barbell 3*12 reps \n Side-lying leg lifts with ankle weights 3*12 reps \n Kettlebell swings 3*12 reps',\
            'Bulgarian split squats with dumbbells 4*10 reps \n Barbell hip thrusts with resistance band 4*10 reps \n Cable pull-throughs 4*10 reps \n Curtsy lunges with dumbbells 4*10 reps',\
                'Romanian deadlifts with barbell 5*8 reps \n Hip abductions with resistance band  5*8 reps \n Single-leg glute bridges with barbell 5*8 reps \n Reverse lunges with dumbbells 5*8 reps',\
                    'Sumo deadlifts with barbell 6*6 reps \n Barbell hip thrusts with heavy weights 6*6 reps \n Single-leg Romanian deadlifts with dumbbells 6*6 reps \n Pistol squats with bodyweight 6*6 reps'],
    
    'core':['Warm up with 5-10 minutes of jogging in place \n Perform 3*15 reps of crunches. \n Perform 3*15 reps of leg raises. \n Perform 3*60 seconds of plank.',\
        'Warm up with 5-10 minutes of jumping jacks \n Perform 3*15 reps of bicycle crunches. \n Perform 3*15 reps of Russian twists \n Perform 3*60 seconds of side plank',
        'Warm up with 5-10 minutes of jump rope \n Perform 3*15 reps of hanging leg raises \n Perform 3*15 reps of weighted decline sit-ups \n Perform 3*60 seconds of weighted plank.',\
            'Warm up with 5-10 minutes of burpees \n Perform 3*15 reps of dragon flags \n Perform 3*15 reps of cable crunches \n Perform 3860 seconds of single-arm plank on each side.',\
                'Warm up with 5-10 min of mountain climbers \n Perform 3*15 reps of hanging windshield wipers \n Perform 3*15 reps of ab wheel rollouts \n Perform 3*60 seconds of Swiss ball pike.']
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

class DecideTrainingType(Action):

    def name(self) -> Text:
        return "action_training_type"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        training_type = next(tracker.get_latest_entity_values("training_type"),None)
        workout = workout_db.get(training_type, None)

        if not workout:
            workout = f"I cannot recognise {training_type}. is it spelled correctly?"
            dispatcher.utter_message(text=workout)
            return[]
        dispatcher.utter_message(text='you can do..')
        dispatcher.utter_message(text=workout)


        return[]


class GiveDietSuggestion(Action):

    def name(self) -> Text:
        return "action_diet_suggestion"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        food_eaten = next(tracker.get_latest_entity_values("food_eaten")) #intent and entity not yet added       
        calories = food_db.get(food_eaten, None)

        if not calories:
            workout = f"I cannot recognise {food_eaten}. is it spelled correctly?"
            dispatcher.utter_message(text=calories)
            return[]
        if calories < 200:
            dispatcher.utter_message(text="your calories in this meal is {calories}, great job, keep it up!")
        elif calories < 400:
            dispatcher.utter_message(text="{calories}Kcal is fine for you in this meal, enjoy!")
        else:
            dispatcher.utter_message(text="what a fulfilling meal with {calories} Kcal, try to eat light in your next meal")



        return[]
