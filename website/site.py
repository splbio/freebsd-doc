import os
import config

from flask import Flask, render_template, abort, g, request
from distros_installs import distros_installs

from flask.ext.babel import Babel

app = Flask(__name__)
app._static_folder = os.getcwd() + '/website/static'
app.config['SECRET_KEY'] = os.urandom(64)
if app.debug:
    from flaskext.lesscss import lesscss
    lesscss(app)
#app.config.from_pyfile('translations.cfg')
babel = Babel(app, default_locale="en_US.ISO8859-1")

from events import get_rss


@babel.localeselector
def get_locale():
    lang = request.cookies.get('lang')
    if lang in config.LANGUAGES:
        return lang
    return request.accept_languages.best_match(config.LANGUAGES)

@app.route('/')
def index():
    from placeholders import news, events, press, security
    return render_template('index.html',
            news=get_rss('news')[:5],
            events=get_rss('upcoming')[:5],
            press=get_rss('press')[:5],
            security=get_rss('security')[:5],
    )

@app.route('/about/')
def about():
    return render_template('about/index.html')

@app.route('/about/<sub>/')
def about_route(sub=None):
    subs = ['advocacy', 'news', 'media', 'donations', 'marketing', 'privacy-policy']
    if sub in subs:
        return render_template('about/%s.html' % sub)

@app.route('/docs/')
def docs():
    return render_template('docs/index.html')

@app.route('/docs/<sub>/')
def docs_route(sub=None):
    subs = ['beginners', 'man-pages', 'handbook', 'publications', 'documentation-project', 'archive']
    if sub in subs:
        return render_template('docs/%s.html' % sub)

@app.route('/community/')
def community():
    return render_template('community/index.html')

@app.route('/community/<sub>/')
def community_route(sub=None):
    subs = ['contributing', 'release-engineering', 'platforms', 'events']
    if sub in subs:
        return render_template('community/%s.html' % sub)

@app.route('/ports/')
def ports():
    return render_template('ports/index.html')

@app.route('/ports/<sub>/')
def ports_route(sub=None):
    subs = ['contributing', 'tickets']
    if sub in subs:
        return render_template('ports/%s.html' % sub)

@app.route('/support/')
def support():
    return render_template('support/index.html')

@app.route('/support/<sub>/')
def support_route(sub=None):
    subs = ['vendors', 'security-information', 'web-resources']
    if sub in subs:
        return render_template('support/%s.html' % sub)

@app.route('/download/<distro>/')
def simple_install(distro=None):
    distro = distros_installs.get(distro)
    if not distro: abort(404)
    return render_template('simple_install.html', distro=distro)


if __name__ == '__main__':
    app.run(debug=True)

