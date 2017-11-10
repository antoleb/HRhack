import pandas as pd
import numpy as np


class NaiveBias:
    def __init__(self, skills, eps=1e-5):
        self.eps = eps
        self.word_dict = dict()

        for id, performance, skill_list in skills:
            for skill in skill_list:
                for word in skill.split():
                    if word in self.word_dict:
                        continue
                    self.word_dict[word] = len(self.word_dict)
        self.freq_list = np.zeros(len(self.word_dict))

        for id, performance, skill in skills:
            self.freq_list += self._build_one_hot_vector_by_list_(skill)

        self.freq_list /= len(skills)
        self.freq_list[self.freq_list == 0] = eps
        self.freq_list[self.freq_list == 1.] = 1-eps

    def _build_one_hot_vector_by_string_(self, string):
        description = np.zeros(len(self.word_dict))
        for word in string.split():
            description[self.word_dict[word]] = 1
        return description

    def _build_one_hot_vector_by_list_(self, skill_list):
        description = np.zeros(len(self.word_dict))
        for skill in skill_list:
            description = (description & self._build_one_hot_vector_by_string_(skill))
        return description

    def log_likehood(self, skill):
        description = self._build_one_hot_vector_(skill)
        return np.sum(np.log(self.freq_list) * description + np.log(1 - self.freq_list) * (1 - description))

    def get_sorted(self, ids, skill_list):
        scores = []
        for skill in skill_list:
            scores.append(self.log_likehood(skill))
        scores = np.array(scores)
        return ids[np.argsort(-scores)]
