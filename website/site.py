import os
import config

from flask import Flask, abort, g, request, url_for, redirect, render_template
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

@app.before_request
def before():
    if request.view_args and 'lang_code' in request.view_args:
        if request.view_args['lang_code'] not in config.LANG_CODES:
            print 'aborting'
            return abort(404)
        g.current_lang = request.view_args['lang_code']
        request.view_args.pop('lang_code')

def get_locale():
    return g.get('current_lang', 'en')

@app.route('/')
def root():
    return redirect(url_for('index', lang_code='en'))

@app.route('/<lang_code>/')
def index():
    from placeholders import news, events, press, security
    return render_template('index.html',
            news=get_rss('news')[:5],
            events=get_rss('upcoming')[:5],
            press=get_rss('press')[:5],
            security=get_rss('security')[:5],
    )

@app.route('/<lang_code>/about/')
def about():
    return render_template('about/index.html')

@app.route('/<lang_code>/about/<sub>/')
def about_route(sub=None):
    subs = ['advocacy', 'news', 'media', 'donations', 'marketing', 'privacy-policy']
    if sub in subs:
        return render_template('about/%s.html' % sub, sub=sub)

@app.route('/<lang_code>/docs/')
def docs():
    return render_template('docs/index.html')

@app.route('/<lang_code>/docs/<sub>/')
def docs_route(sub=None):
    subs = ['beginners', 'man-pages', 'handbook', 'publications', 'documentation-project', 'archive']
    if sub in subs:
        return render_template('docs/%s.html' % sub, sub=sub)

@app.route('/<lang_code>/community/')
def community():
    return render_template('community/index.html')

@app.route('/<lang_code>/community/<sub>/')
def community_route(sub=None):
    subs = ['contributing', 'release-engineering', 'platforms', 'events']
    if sub in subs:
        return render_template('community/%s.html' % sub, sub=sub)

@app.route('/<lang_code>/ports/')
def ports():
    return render_template('ports/index.html')

@app.route('/<lang_code>/ports/<sub>/')
def ports_route(sub=None):
    subs = ['contributing', 'tickets']
    if sub in subs:
        return render_template('ports/%s.html' % sub, sub=sub)

@app.route('/<lang_code>/support/')
def support():
    return render_template('support/index.html')

@app.route('/<lang_code>/support/<sub>/')
def support_route(sub=None):
    subs = ['vendors', 'security-information', 'web-resources']
    if sub in subs:
        return render_template('support/%s.html' % sub, sub=sub)

@app.route('/<lang_code>/download/<distro>/')
def simple_install(distro=None):
    distro = distros_installs.get(distro)
    if not distro: abort(404)
    return render_template('simple_install.html', distro=distro)


if __name__ == '__main__':
    app.run(debug=True)

