import sys

from os.path import dirname, join, abspath

from flask import Flask, render_template, request, flash, jsonify

from commands.set_up_db import SetupDB

sys.path.insert(0, abspath(join(dirname(__file__), '.')))

from managers.database_manager import DatabaseManager

app = Flask(__name__)
app.secret_key = "SECRET_KEY"


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET', 'POST'])
def index():
    template_data = dict()
    database_manager = DatabaseManager()
    connection = database_manager.get_connecion()
    connection.row_factory = dict_factory
    if request.method == 'POST':
        tour_search = request.form['tour']
        print(tour_search)
        template_data['tours'] = connection.execute(
            f"""SELECT * from TOURS WHERE name LIKE '%{tour_search}%';"""
        ).fetchall()

    template_data['cities'] = connection.execute(""" SELECT * from Cities;""").fetchall()
    template_data['users'] = connection.execute(""" SELECT * from Users;""").fetchall()
    template_data['success'] = 'True'

    return render_template('index.html', **template_data)


@app.route('/tours', methods=['POST', ])
def create_tour():
    template_data = dict()
    database_manager = DatabaseManager()
    connection = database_manager.get_connecion()
    connection.row_factory = dict_factory
    values = list()

    for el, v in request.form.items():
        if el == 'frequency':
            continue
        else:
            values.append(v)

    days = ','.join(request.form.getlist('frequency'))

    values.append(days)
    connection.execute(
        f"""INSERT INTO Tours (name, CityID, UserID, description, days) VALUES {tuple(values)};"""
    )
    template_data['cities'] = connection.execute(""" SELECT * from Cities;""").fetchall()
    template_data['users'] = connection.execute(""" SELECT * from Users;""").fetchall()
    flash('Tour created', 'success')

    return render_template('index.html', **template_data)


@app.route('/setup', methods=['GET', ])
def setup_db():
    print('ok')
    SetupDB().run_script()
    return jsonify({'status': 'OK'})


if __name__ == "__main__":
    app.run(debug=True)
