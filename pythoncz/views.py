# -*- coding: utf-8 -*-


from flask import (render_template as _render_template, url_for,
                   redirect, request)

from . import app, trello, business


# Templating

def render_template(filename, **kwargs):
    template_url = app.config['TEMPLATE_URL'].format(filename=filename)
    kwargs['template_url'] = template_url
    return _render_template(filename, **kwargs)


@app.context_processor
def inject_context():
    return {
        'debug': app.debug,
        'config': app.config,
        'url': request.url,
    }


# Regular views

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/en')
def index_en():
    return render_template('index-en.html')


@app.route('/zapojse')
def get_involved():
    trello_board_id = app.config['TRELLO_BOARD_ID']
    context = {
        'trello_board': trello.get_board(trello_board_id),
        'trello_board_url': 'https://trello.com/b/{}/'.format(trello_board_id),
    }
    return render_template('get_involved.html', **context)


@app.route('/prace')
def jobs():
    groups = business.get_groups(app.config['DATA_DIR'])
    return render_template('jobs.html', business_groups=groups)


@app.route('/en/jobs')
def jobs_en():
    groups = business.get_groups(app.config['DATA_DIR'])
    return render_template('jobs-en.html', business_groups=groups)


# Legacy redirects

@app.route('/index.html')
def index_legacy():
    return redirect(url_for('index'), code=301)


@app.route('/english.html')
def index_en_legacy():
    return redirect(url_for('index_en'), code=301)


@app.route('/pyladies/', defaults={'target': ''})
@app.route('/pyladies/<path:target>')
def pyladies(target):
    return redirect('http://pyladies.cz/' + target, code=301)


@app.route('/talks/<path:target>')
def talks(target):
    base_url = 'https://github.com/pyvec/talks-archive/raw/master/'
    return redirect(base_url + target, code=301)
