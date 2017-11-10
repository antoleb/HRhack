import numpy as np
from .tfidf_bayes import TfIdfBayes

from app.hr.naive_bayes import NaiveBayes


class Finder:
    def __init__(self, data_handler):
        self._data_handler = data_handler

    def _get_relevant(self, all_ids, position, data_handler):
        relevant = np.ones_like(all_ids)
        for c, id in enumerate(all_ids):
            positions = data_handler.positions_by_id(id)
            if position in positions:
                relevant[c] = 0
        return relevant

    def make_internal_position(self, department, position):
        return position + '/' + department

    def find_sorted_candidates(self, department, position):
        internal_position = self.make_internal_position(department, position)
        skills = self._data_handler.skills_by_position(internal_position)
        model = TfIdfBayes(skills, self._data_handler, internal_position)

        all_ids, skill_list = self._data_handler.all_skills()
        relevant = self._get_relevant(all_ids, position, self._data_handler).astype(bool)
        sorted_candidates = model.get_sorted(all_ids[relevant], skill_list[relevant])

        return sorted_candidates

    def test_naive_bayes_without_id(self, id):
        test_data_handler = self._data_handler.remove_id(id)
        positions = self._data_handler.positions_by_id(id)
        position = positions[-1]
        skills = test_data_handler.skills_by_position(position)
        model = NaiveBayes(skills)
        all_ids, skill_list = self._data_handler.all_skills()
        relevant = self._get_relevant(all_ids, position, test_data_handler).astype(bool)
        sorted_list = model.get_sorted(all_ids[relevant], skill_list[relevant])
        return sorted_list

    def test_tf_idf_bayes_without_id(self, id):
        test_data_handler = self._data_handler.remove_id(id)
        positions = self._data_handler.positions_by_id(id)
        position = positions[-1]
        skills = test_data_handler.skills_by_position(position)
        model = TfIdfBayes(skills, test_data_handler, position)
        all_ids, skill_list = self._data_handler.all_skills()
        relevant = self._get_relevant(all_ids, position, test_data_handler).astype(bool)
        sorted_list = model.get_sorted(all_ids[relevant], skill_list[relevant])
        return sorted_list
