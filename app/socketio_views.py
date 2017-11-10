from flask_socketio import emit

import pandas as pd

from .hr import DataHandler, Finder
from .main import socketio
from .settings.paths import KROK_FILE


def init_datahandler(krok_file=KROK_FILE):
    xls = pd.ExcelFile(krok_file)
    skills = xls.parse('Навыки')
    courses = xls.parse('Обучение')
    communication = xls.parse('Коммуникации')
    movement = xls.parse('Движения')
    performance = xls.parse('performance management')

    return DataHandler(skills, courses, communication, movement, performance)


data_handler = init_datahandler()
finder = Finder(data_handler)


def make_response(success, message):
    return {
        'status': 'success' if success else 'error',
        'message': message,
    }


@socketio.on('find_canditates')
def find_canditates(json):
    try:
        sorted_candidates = finder.find_sorted_candidates(json['department'], json['position'])
    except:
        emit('candidates', make_response(False, 'Bad args'))

    emit('candidates', make_response(True, 'fuck_you'))
