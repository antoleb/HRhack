import pandas as pd
import numpy as np
import DataHandler
import NaiveBias

class Tester:
    def __init__(self, dataHandler):
        self.dataHandler = dataHandler

    def get_relevant(self, all_ids, position, dataHandler):
        relevant = np.ones_like(all_ids)
        for c, id in enumerate(all_ids):
            positions = dataHandler.positions_by_id(id)
            if position in positions:
                relevant[c] = 0
        return relevant

    def test_without_id(self, id, modelConstructor):
        testDataHandler = self.dataHandler.remove_id(id)
        positions = self.dataHandler.positions_by_id(id)
        position = positions[0]
        skills = testDataHandler.skills_by_position(position)
        id_skills = self.dataHandler.skills_by_id(id)
        model = modelConstructor(skills)
        all_ids, skill_list = self.dataHandler.all_skills()
        relevant = self.get_relevant(all_ids, skill_list, testDataHandler)
        sorted_list = model.get_sorted(all_ids[relevant], skill_list[relevant])

        return sorted_list
