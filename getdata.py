import os
import json
import pandas as pd
import pprint
from collections import namedtuple

run_folder = "./data"
Card = namedtuple("Card", ["name", "act_number", "floor_number", "ascension", "victory"])

if __name__ == "__main__":
    all_data = {}

    #load all run files from the data folder
    for filename in os.listdir(run_folder):
        if filename.endswith(".run"):
            with open(os.path.join(run_folder, filename), "r") as f:
                data = json.load(f)
                if data["was_abandoned"] == False:
                    all_data[filename] = data

    #condense all run data into a single JSON file
    df = pd.DataFrame(all_data)
    df.to_json("all_data.json", orient="columns", indent=4)

    #create a summary of the run data and extract card information
    summary_data = {}
    summary_data = {
        "num_entries": len(all_data),
        "num_victories": 0,
    }
    card_data = []

    for run in all_data:   
        if all_data[run]["win"] == True:
            summary_data["num_victories"] += 1

        floor_number = 0
        act_number = 0

        for act in all_data[run]["map_point_history"]:
            act_number += 1
            for floor in act:
                floor_number += 1

                #get victory data for each card gained and which floor it was gained on
                if "cards_gained" in floor["player_stats"][0]:
                    for card in floor["player_stats"][0]["cards_gained"]:
                        card_data.append(
                            {
                                "name": card["id"],
                                "act_number": act_number,
                                "floor_number": floor_number,
                                "ascension": all_data[run]["ascension"],
                                "victory": all_data[run]["win"]
                            }
                        )
    print(f"{summary_data['num_entries']} runs recorded with {summary_data['num_victories']} victories.")
    print(f"{len(card_data)} card entries recorded.")
    df2 = pd.DataFrame(card_data)
    df2.to_json("card_data.json", orient="records", indent=4)
    print("Done!")


        
                
            

    