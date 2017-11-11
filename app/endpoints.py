from flask import request, jsonify, make_response, current_app
from datetime import timedelta
from functools import update_wrapper

import pandas as pd

from .hr import DataHandler, Finder
from .app import app
from .settings.paths import KROK_FILE


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


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
        } for career in reversed(data_handler.career_by_id(id_))
    ]

    candidate_dict['finished_courses'] = list(data_handler.courses_by_id(id_))
    candidate_dict['suggested_courses'] = list(data_handler.suggested_courses_by_id_and_position(
        id_, finder.make_internal_position(sought_department, sought_position))
    )

    return candidate_dict


data_handler = init_datahandler()
finder = Finder(data_handler)


def my_make_response(success, message):
    return jsonify({
        'status': 'success' if success else 'error',
        'message': message,
    })


@app.route('/find_candidates')
def find_canditates():
    sought_department = request.form['department']
    sought_position = request.form['position']

    sorted_candidates = finder.find_sorted_candidates(sought_department, sought_position)
    candidates = [
        make_candidate_dict(data_handler, candidate_id, sought_department, sought_position)
        for candidate_id in sorted_candidates[:5]
    ]

    return my_make_response(True, candidates)


@app.route('/get_all_positions')
@crossdomain(origin='*')
def get_all_positions():
    return my_make_response(True, data_handler.unique_full_positions())


@app.route('/get_all_ids')
def get_all_ids():
    return my_make_response(True, my_make_response(True, 'Nothing'))


def candidate_position_and_time(id_):
    department, position, work_time = data_handler.current_position_by_id(id_)

    return {
        'department': department,
        'position': position,
        'work_time': work_time,
    }

@app.route('/get_position_and_time')
def get_position_and_time():
    print(type(request.form['id']))
    return my_make_response(True, candidate_position_and_time(request.form['id']))


def suggested_positions_by_id(id_):
    real_candidate_info = candidate_position_and_time(id_)
    suggested_positions = []

    for suggested_position in data_handler.suggested_positions_by_id(id_):
        desired_position = suggested_position[0]
        desired_department = suggested_position[1]

        desired_internal_position = finder.make_internal_position(desired_department, desired_position)
        real_internal_position = finder.make_internal_position(
            real_candidate_info['department'], real_candidate_info['position']
        )

        indexes, mean_time = data_handler.get_mean_work_time_and_contacts(
            real_internal_position,
            desired_internal_position
        )

        position_dict = {
            'position': desired_position,
            'department': desired_department,
            'promotion_number': suggested_position[2],
            'mean_time': mean_time.days,
            'promoted_ids': list(map(int, indexes)),
        }

        suggested_positions.append(position_dict)

    return suggested_positions


@app.route('/get_suggested_positions')
def get_opportunities():
    return my_make_response(True, suggested_positions_by_id(request.form['id']))
