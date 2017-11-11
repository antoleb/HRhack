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

        self.movement['full_position'] = self.movement[['position', 'Department']].apply(lambda x: "{}/{}".format(x[0], x[1]),
    axis=1)

        if remove:
            good_positions = self.movement.full_position.value_counts()[self.movement.full_position.value_counts() > k].index
            self.movement = self.movement[self.movement.full_position.isin(good_positions)]

    def unique_full_positions(self):
        all = self.movement.full_position.unique()
        dic = dict()
        for i in all:
            p, d = i.split('/')
            if d not in dic:
                dic[d] = []
            dic[d].append(p)
        return dic

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
        return self.movement.loc[lambda df: df['full_position'] == full_position, :]['id'].values

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

    def first_start_time(self, id, position):
        """
        :param id:
        :param position:
        :return: first start time of id on position
        """
        return self.movement[(self.movement.full_position == position) & (self.movement.id == id)].START_DATE.min()

    def last_start_time(self, id, position):
        """
        :param id:
        :param position:
        :return: last start time of id on position
        """
        return self.movement[(self.movement.full_position == position) & (self.movement.id == id)].START_DATE.max()

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

    def career_by_id(self, id):
        """
        returns: [id, position, full name, start date, end date]
        """
        ar = self.movement.loc[lambda df: df['id'] == id, :][['id', 'position', 'FULL_NAME', 'START_DATE', 'END_DATE']].values
        ar = ar[np.argsort(ar[:,3], axis=0)]
        for i in range(ar.shape[0]-1):
            ar[i,4] = min(ar[i,4], ar[i+1,3])
        if (self.current_position_by_id(id)[2] > 0): # if currently working set end date as today's date
            ar[-1,4] = None
        return ar

    def suggested_courses_by_id_and_position(self, id, position):
        """
        :param id:
        :param position:
        :return:  sorted list of suggested courses
        """
        ids = self.movement[self.movement.full_position == position].id.unique()
        all_courses = self.courses[self.courses.id.isin(ids)]
        user_courses = self.courses[self.courses.id == id]
        mask = np.zeros(all_courses.shape[0])
        for id_ in ids:
            id_start_time = self.first_start_time(id_, position)
            mask[all_courses.id == id_] = all_courses[all_courses.id == id_]['Дата окончания'] < id_start_time
        all_courses = all_courses[mask.astype(bool)]
        need_courses = all_courses[~all_courses['Название обучения'].isin(user_courses)]
        sorted_courses = need_courses['Название обучения'].value_counts().index.values
        return sorted_courses

    def suggested_positions_by_id(self, id):
        """
        returns: [position, department, count]
        """
        pos = self.current_position_by_id(id)
        if (pos[2] == 0):
            return np.empty()
        idx = self.movement.loc[lambda df: df['position'] == pos[1],:].loc[lambda df: df['Department'] == pos[0],:].index
        next_move = []
        for i in idx:
            if (i >= self.movement.last_valid_index() or (not (i in self.movement.index)) or (not (i+1 in self.movement.index))):
                continue
            if (self.movement.loc[i+1]['id'] == self.movement.loc[i]['id'] and (self.movement.loc[i+1]['position'] != pos[1] or self.movement.loc[i+1]['Department'] != pos[0] )):
                next_move.append([self.movement.loc[i+1]['position'], self.movement.loc[i+1]['Department']])
        unique_moves, counts = np.unique(next_move, return_counts=True, axis=0)
        srt = counts.argsort()[::-1]
        return np.concatenate([unique_moves[srt], counts[srt].reshape(-1,1)], axis=1)

    def get_mean_work_time_and_contacts(self, current_pos, desiered_pos):
        """
        :param current_pos:
        :param desiered_pos:
        :return:  [indxes, mean_time]
        """

        current_pos_ids = self.movement[self.movement.full_position == current_pos].id.unique()
        desiered_pos_ids = self.movement[self.movement.full_position == desiered_pos].id.unique()
        both_ids = np.intersect1d(current_pos_ids, desiered_pos_ids)
        time_list = []
        for id_ in both_ids:
            end = self.last_start_time(id_, desiered_pos)
            start = self.last_start_time(id_, current_pos)
            time_list.append(end - start)

        return both_ids, np.mean(time_list)

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
