import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class TfIdfBias:
    def __init__(self, skills, dataHandler, pos, eps=1e-5):
        self.eps = eps
        self.dataHandler = dataHandler
        self.pos = pos

        collection = []
        indx = np.where(dataHandler.movement.full_position.unique() == pos)[0][0]
        for pos in dataHandler.movement.full_position.unique():
            collection.append(self.get_string(pos))

        tfIdf = TfidfVectorizer()
        self.idfcoef = tfIdf.fit_transform(collection).toarray()[indx]
        self.word_dict = tfIdf.vocabulary_

        self.freq_list = np.zeros(len(self.word_dict))

        for id, performance, skill in skills:
            self.freq_list += self._build_one_hot_vector_by_list_(skill)

        self.freq_list /= len(skills)
        self.freq_list[self.freq_list == 0] = eps
        self.freq_list[self.freq_list == 1.] = 1-eps

    def get_string(self, pos):
        texts = []
        for _, _, t in self.dataHandler.skills_by_position(pos):
            texts.append(t)
        res = ''
        for i in texts:
            s = set()
            for i in i:
                for word in i.split():
                    s.add(word)
            res += ' '.join(sorted(list(s)))
        return res

    def _build_one_hot_vector_by_string_(self, string):
        description = np.zeros(len(self.word_dict))
        for word in string.split():
            if word in self.word_dict:
                description[self.word_dict[word]] = 1
        return description

    def _build_one_hot_vector_by_list_(self, skill_list):
        description = np.zeros(len(self.word_dict))
        for skill in skill_list:
            description += self._build_one_hot_vector_by_string_(skill)
        description[description != 0] = 1
        return description

    def log_likehood(self, skill):
        description = self._build_one_hot_vector_by_list_(skill)
        return np.sum(np.log(1 - self.freq_list) * (1 - description) * self.idfcoef)

    def get_sorted(self, ids, skill_list):
        scores = []

        for skill in skill_list:
            scores.append(self.log_likehood(skill))
        scores = np.array(scores)
        return ids[np.argsort(-scores)]
