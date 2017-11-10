import pandas as pd
import numpy as np


class DataHandler:
    def __init__(self, skills, courses, communication, movement, performance):
        self.skills = skills
        self.courses = courses
        self.communication = communication
        self.movement = movement
        self.performance = performance

        self.movement['full_position'] = self.movement[['position', 'Department']].apply(
            lambda x: "{}/{}".format(x[0], x[1]),
            axis=1)

    def skills_by_id(self, id):
        """
        returns: list of srtings from self.skills
        """
        return self.skills[self.skills.ID == id].TAGNAME.values

    def positions_by_id(self, id):
        """
        returns: string list from self.movement
        """
        return self.movement[self.movement.id == id]['full_position'].values

    def ids_by_position(self, full_position):
        """
        returns: ids
        """
        return list( movement.loc[lambda df: df['full_position']==full_position, :]['id'] )

    def skills_by_position(self, position):
        """
        returns: [id, performance, skills]
        """
        pass
