import json
import sys

import app
import pandas as pd
from . import stats_blueprint
from flask import current_app, render_template, request


# request callbacks
@stats_blueprint.before_request
def stats_before_request():
    current_app.logger.info('Calling before_request() for the stats blueprint...')


@stats_blueprint.after_request
def stats_after_request(response):
    current_app.logger.info('Calling after_request() for the stats blueprint...')
    return response


@stats_blueprint.teardown_request
def stats_teardown_request(error=None):
    current_app.logger.info('Calling teardown_request() for the stats blueprint...')


@stats_blueprint.route('/_update_table', methods=['GET', 'POST'])
def update_table():
    elo = 1900

    # if user has entered an elo value then we update with the user's value
    if request.method == "POST":
        elo = request.args.get('output', 0, type=int)

    # This is jank nightmare fuel but it works for some reason?
    elo = int(list(request.args.keys())[0])

    # get new dataframe based on new elo value
    df = app.uf.get_win_rate_table(app.uf.get_game_set_by_rating(app.chess_games, elo))

    # return the new table out to the client
    return pd.DataFrame(df).to_json(orient='columns')


@stats_blueprint.route('/', methods=['GET', 'POST'])
def index():
    current_app.logger.info('Calling the index() function.')

    df = app.uf.get_win_rate_table(app.uf.get_game_set_by_rating(app.chess_games, 2500))

    # get table headers and rows
    columns = df.columns
    rows = df.values

    # re-render html page with new table values
    return render_template('stats/index.html',
                           columns=columns,
                           rows=rows)

