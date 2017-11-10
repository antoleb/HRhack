import pandas as pd
import numpy as np
import time
import datetime


class DataHandler:
    def __init__(self, skills, courses, communication, movement, performance, k=3, remove=True):
        self.skills = skills
        self.courses = courses
        self.communication = communication
        self.movement = movement
        self.performance = performance

    def __init__(self, skills, courses, communication, movement, performance, k=3, remove=True):
        self.skills = skills
        self.courses = courses
        self.communication = communication
        self.movement = movement
        self.performance = performance

        self.movement['full_position'] = self.movement[['position', 'Department']].apply(lambda x:'{}/{}'.format(x[0], x[1]),
    axis=1)

        if remove:
            good_positions = self.movement.full_position.value_counts()[self.movement.full_position.value_counts() > k].index
            self.movement = self.movement[self.movement.full_position.isin(good_positions)]

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

    def all_skills(self):
        result = []
        all_ids = self.skills.ID.unique()
        for id in all_ids:
            result.append(self.skills_by_id(id))
        return all_ids, np.array(result)

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

        pe = self.performance.loc[lambda df: df['ID'].isin(ids), :].set_index('ID')
        sk = self.skills.loc[lambda df: df['ID'].isin(ids), :].groupby('ID').agg(lambda x: x.tolist())
        df = pd.concat([pe, sk], axis=1)

        perf_col = ['2017 I Полугодие', '2016 II Полугодие', '2016 I Полугодие',
       '2015 II Полугодие', '2015 I Полугодие', '2014 II Полугодие',
       '2014 I Полугодие']

        df['performance'] = df[perf_col].values.tolist()
        df['TAGNAME'] = [row[1] if type(row[1]) == list else list() for row in df['TAGNAME'].iteritems()]
        df['performance'] = [row[1] if type(row[1]) == list else list() for row in df['performance'].iteritems()]

        need_col =['performance', 'TAGNAME']
        return df[need_col].reset_index().values

    def courses_by_id(self, id):
        """
        returns: list of srtings from self.courses
        """
        return self.courses[self.courses.id == id]['Название обучения'].values
    
    def courses_by_position(self, position):
        """
        returns: [id, skills]
        """
        ids = self.ids_by_position(position)
        df = self.courses.loc[lambda df: df['id'].isin(ids), :].groupby('id').agg(lambda x: x.tolist())
        df['Название обучения'] = [row[1] if type(row[1]) == list else list() for row in df['Название обучения'].iteritems()]
        return df['Название обучения'].reset_index().values

    def current_position_by_id(self, id):
        """
        returns: [department, position, work_time]
        """
        if self.performance.loc[lambda df: df['ID'] == id, :]['Статус'].values[0] == 'Бывший сотрудник':
            return ['', '', 0]
        info = self.movement.loc[self.movement.loc[lambda df: df['id'] == id, :]['START_DATE'].idxmax(), :].values
        today = pd.Timestamp(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        delta = today - info[3]
        return [info[6], info[1], delta.round(freq='1440min').days]

    def remove_id(self, id):
        """
        :param id:
        :return: new  DataHandler without any positions with such id
        """
        return DataHandler(
            skills=self.skills,
            courses=self.courses,
            communication=self.communication,
            movement=self.movement[self.movement.id != id],
            performance=self.performance,
            remove=False
        )
