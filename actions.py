# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from geopy import geocoders # pip install geopy
import tzwhere


g = geocoders.GoogleV3()

class ActionShowTimeZone(Action):

    def name(self) -> Text:
        return "action_show_time_zone"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        # timedict ={
        #     "Lonodn": "UTC+1.00",
        #     "Colombo": "UTC+5.30",
        #     "Sofia": "UTC+3.00",
        #     "Lisbon": "UTC+1.00"
        # }
        city = tracker.get_slot("city").capitalize()
        # timezone = timedict.get(city)

        
        place, (lat, lng) = g.geocode(city)
        # -> (u'Singapore', (1.352083, 103.819836))
        w = tzwhere()
        timezone = w.tzNameAt(1.352083, 103.819836)


        if timezone is None:
            output = "Could not find time zone of {}".format(city)
        else: 
            output = "Timezone of {} is {}".format(city, timezone)

        dispatcher.utter_message(text=output)

        return []