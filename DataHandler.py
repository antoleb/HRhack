import pandas as pd
import numpy as np


class DataHandler():
    def __init__(self, skills, courses, communication, movement, performance):
        self.skills = skills
        self.courses = courses
        self.communication = communication
        self.movement = movement
        self.performance = performance

        self.movement['full_position'] = self.movement[['position', 'Department']].apply(lambda x: "{}/{}".format(x[0], x[1]),
    axis=1)

    def skills_by_id(self, id):
        """
        returns: list of srtings from self.skills
        """
        return self.skills[skills.ID == id].TAGNAME.values

    def positions_by_id(self, id):
        """
        returns: string list from self.movement
        """
        return self.movement[self.movement.id == id]['full_position'].values

    def ids_by_position(self, full_position):
        """
        returns: ids
        """
        return self.movement.loc[lambda df: df['full_position']==full_position, :]['id'].values

    def skills_by_position(self, position):
        """
        returns: [id, performance, skills]
        """
        ids = self.ids_by_position(position)
        
        pe = performance.loc[lambda df: df['ID'].isin(ids), :].set_index('ID')
        sk = skills.loc[lambda df: df['ID'].isin(ids), :].groupby('ID').agg(lambda x: x.tolist())
        df = pd.concat([pe,sk], axis=1)
        
        perf_col =['2017 I Полугодие', '2016 II Полугодие', '2016 I Полугодие',
       '2015 II Полугодие', '2015 I Полугодие', '2014 II Полугодие',
       '2014 I Полугодие']
        df['performance'] = df[perf_col].values.tolist()
        
        need_col =['performance', 'TAGNAME']
        return df1[need_col].reset_index().values
