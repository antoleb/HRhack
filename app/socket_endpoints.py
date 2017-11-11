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


def make_candidate_dict(data_handler, id_, sought_department, sought_position):
    """
    Args:
        data_handler (DataHandler): fuck you
        id (int): fuck you

    Returns:
        dict: candidate
    """

    candidate_dict = {
        'id': int(id_),
    }

    department, position, work_time = data_handler.current_position_by_id(id_)
    candidate_dict['department'] = department
    candidate_dict['position'] = position

    candidate_dict['careers'] = [
        {
            'id': career[0],
            'position': career[1],
            'department': career[2],
            'start_timestamp': career[3].timestamp(),
            'end_timestamp': career[4] if career[4] is None else career[4].timestamp(),
        } for career in data_handler.career_by_id(id_)
    ]

    candidate_dict['finished_courses'] = list(data_handler.courses_by_id(id_))
    candidate_dict['suggested_courses'] = list(data_handler.suggested_courses_by_id_and_position(
        id_, finder.make_internal_position(sought_department, sought_position))
    )

    return candidate_dict


data_handler = init_datahandler()
finder = Finder(data_handler)


def make_response(success, message):
    return {
        'status': 'success' if success else 'error',
        'message': message,
    }


@socketio.on('find_candidates')
def find_canditates(json):
    # try:
    sought_department = json['department']
    sought_position = json['position']

    sorted_candidates = finder.find_sorted_candidates(json['department'], json['position'])
    candidates = [
        make_candidate_dict(data_handler, candidate_id, sought_department, sought_position)
        for candidate_id in sorted_candidates[:5]
    ]

    emit('candidates', make_response(True, candidates))
    # except:
    #     emit('candidates', make_response(False, 'Bad args'))


@socketio.on('get_all_positions')
def get_all_positions():
    emit('all_positions', make_response(True, data_handler.unique_full_positions()))


@socketio.on('get_all_ids')
def get_all_ids():
    emit('all_ids', make_response(True, 'Nothing'))


def candidate_position_and_time(id_):
    department, position, work_time = data_handler.current_position_by_id(id_)

    return {
        'department': department,
        'position': position,
        'work_time': work_time,
    }


@socketio.on('get_position_and_time')
def get_position_and_time(json):
    emit('postition_and_time', make_response(True, candidate_position_and_time(json['id'])))


@socketio.on('get_opportunities')
def get_opportunities(json):
    emit('opportunities', make_response(True, 'u tebya net vozmozhnostei, pidor'))
