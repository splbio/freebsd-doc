import os
import config

from flask import Flask, abort, g, request, url_for, redirect
from flask import render_template as flask_render_template
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

def render_template(template, *args, **kwargs):
    lang_path = config.LANG_MAP.get(g.current_lang, 'en_US.ISO8859-1')
    kwargs['include_template'] = "%s/htdocs/%s" % (lang_path, template)
    return flask_render_template(template, *args, **kwargs)

@app.before_request
def before():
    if request.view_args and 'lang_code' in request.view_args:
        if request.view_args['lang_code'] not in config.LANG_CODES:
            print 'aborting'
            return abort(404)
        g.current_lang = request.view_args['lang_code']
        request.view_args.pop('lang_code')

@babel.localeselector
def get_locale():
    lang = config.LANG_LOCALE.get(g.get('current_lang'), 'en_US.ISO8859-1')
    return lang

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
    return render_template('about.html')

@app.route('/<lang_code>/about/<sub>/')
def about_route(sub=None):
    subs = ['advocacy', 'news', 'media', 'donations', 'marketing', 'privacy-policy']
    if sub in subs:
        return render_template('about.html', sub=sub)

@app.route('/<lang_code>/docs/')
def docs():
    return render_template('docs.html')

@app.route('/<lang_code>/docs/<sub>/')
def docs_route(sub=None):
    subs = ['beginners', 'man-pages', 'handbook', 'publications', 'documentation-project', 'archive']
    if sub in subs:
        return render_template('docs.html', sub=sub)

@app.route('/<lang_code>/community/')
def community():
    return render_template('community.html')

@app.route('/<lang_code>/community/<sub>/')
def community_route(sub=None):
    subs = ['contributing', 'release-engineering', 'platforms', 'events']
    if sub in subs:
        return render_template('community.html', sub=sub)

@app.route('/<lang_code>/ports/')
def ports():
    return render_template('ports.html')

@app.route('/<lang_code>/ports/<sub>/')
def ports_route(sub=None):
    subs = ['contributing', 'tickets']
    if sub in subs:
        return render_template('ports.html', sub=sub)

@app.route('/<lang_code>/support/')
def support():
    return render_template('support.html')

@app.route('/<lang_code>/support/<sub>/')
def support_route(sub=None):
    subs = ['vendors', 'security-information', 'web-resources']
    if sub in subs:
        return render_template('support.html', sub=sub)

@app.route('/<lang_code>/download/<distro>/')
def simple_install(distro=None):
    distro = distros_installs.get(distro)
    if not distro: abort(404)
    return render_template('simple_install.html', distro=distro)

if __name__ == '__main__':
    args = {}
    if os.environ.get("FLASK_DEBUG", None) is not None:
	args["debug"] = True
    if os.environ.get("FLASK_HOST", None) is not None:
	args["host"] = os.environ.get("FLASK_HOST")
    if os.environ.get("FLASK_PORT", None) is not None:
	args["port"] = os.environ.get("FLASK_PORT")

    app.run(**args)

