# Django settings for astrobin project.
import os
from django.conf import global_settings

local_path = lambda path: os.path.join(os.path.dirname(__file__), path)

DEBUG = False
TEMPLATE_DEBUG = DEBUG
MAINTENANCE_MODE = False
READONLY_MODE = False
MEDIA_VERSION = '34'

ADMINS = (
    ('Salvatore Iovene', 'salvatore@astrobin.com'),
)

MANAGERS = ADMINS
SERVER_EMAIL = 'noreply@astrobin.com'
DEFAULT_FROM_EMAIL = 'AstroBin <noreply@astrobin.com>'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_SUBJECT_PREFIX = '[AstroBin]'
EMAIL_HOST='127.0.0.1'
if DEBUG:
    EMAIL_PORT='1025'
else:
    EMAIL_PORT='25'
EMAIL_USE_TLS=False
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.environ['ASTROBIN_DATABASE_NAME'],         # Or path to database file if using sqlite3.
        'USER': os.environ['ASTROBIN_DATABASE_USER'],         # Not used with sqlite3.
        'PASSWORD': os.environ['ASTROBIN_DATABASE_PASSWORD'], # Not used with sqlite3.
        'HOST': os.environ['ASTROBIN_DATABASE_HOST'],         # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                                           # Set to empty string for default. Not used with sqlite3.
    }
}
DEFAULT_CHARSET = 'utf-8'

ASTROBIN_BASE_URL = 'http://www.astrobin.com'
ASTROBIN_SHORT_BASE_URL = 'http://astrob.in'

ASTROBIN_BASE_PATH = os.path.abspath(__file__)
UPLOADS_DIRECTORY = '/webserver/www/uploads/'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'
LANGUAGE_COOKIE_NAME = 'astrobin_lang'

gettext = lambda s: s
LANGUAGES = (
    ('en', gettext('English')),
    ('it', gettext('Italian')),
    ('es', gettext('Spanish')),
    ('fr', gettext('French')),
    ('fi', gettext('Finnish')),
    ('de', gettext('German')),
    ('nl', gettext('Dutch')),
    ('tr', gettext('Turkish')),
    ('sq', gettext('Albanian')),
    ('pl', gettext('Polish')),
    ('pt-BR', gettext('Brazilian Portuguese')),
    ('el', gettext('Greek')),
)
MODELTRANSLATION_TRANSLATION_REGISTRY = 'astrobin.translation'

SITE_ID = 1

STATIC_ROOT = '/webserver/www/sitestatic'
STATIC_URL = '/sitestatic/'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ASTROBIN_BASE_PATH + '/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = STATIC_URL + '/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '4a*^ggw_5#w%tdf0q)=zozrw!avlts-h&&(--wy9x&p*c1l10G'

# Django storages
DEFAULT_FILE_STORAGE = 'astrobin.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = os.environ['ASTROBIN_AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['ASTROBIN_AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['ASTROBIN_AWS_STORAGE_BUCKET_NAME']
AWS_STORAGE_BUCKET_CNAME = AWS_STORAGE_BUCKET_NAME

from S3 import CallingFormat
AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN

# see http://developer.yahoo.com/performance/rules.html#expires
AWS_HEADERS = {
    'Expires': 'Thu, 15 Apr 2080 20:00:00 GMT',
    'Cache-Control': 'max-age=31557600',
    'x-amz-acl': 'public-read',
    
    }
S3_URL = 's3.amazonaws.com'
IMAGES_URL = os.environ['ASTROBIN_IMAGES_URL']
RESIZED_IMAGE_SIZE = 620 
THUMBNAIL_SIZE = 184
SMALL_THUMBNAIL_SIZE = 90
IMAGE_OF_THE_DAY_WIDTH = 780
IMAGE_OF_THE_DAY_HEIGHT = 180

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware', # KEEP AT THE BEGINNING
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
#   'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
#   'astrobin.middlewares.ProfilerMiddleware',
#   'astrobin.middlewares.VaryOnLangCacheMiddleware',
    'privatebeta.middleware.PrivateBetaMiddleware',
    'maintenancemode.middleware.MaintenanceModeMiddleware',
#    'pipeline.middleware.MinifyHTMLMiddleware', Enable after dealing with the blank spaces everywhere
    #'johnny.middleware.LocalStoreClearMiddleware',
    #'johnny.middleware.QueryCacheMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware', # KEEP AT THE END
)

ROOT_URLCONF = 'astrobin.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    local_path('/templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.core.context_processors.auth',
    'notification.context_processors.notification',
    'astrobin.context_processors.privatebeta_enabled',
    'astrobin.context_processors.notices_count',
    'astrobin.context_processors.user_language',
    'astrobin.context_processors.common_variables',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'zinnia.context_processors.version',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.markup',
    'staticfiles',
    'astrobin',
    'django.contrib.admin',
    'registration',
    'djangoratings',
    'haystack',
    'notification',
    'debug_toolbar',
    'persistent_messages',
    'djcelery',
    'gunicorn',
    'privatebeta',
    'south',
    'django.contrib.comments',
    'tagging',
    'mptt',
    'zinnia',
    'tinymce',
    'hitcount',
    'pagination',
    'avatar',
    'uni_form',
    'threaded_messages',
    'bootstrap_toolkit',
    'contact_form',
    'pipeline',
    'tastypie',
    'reviews',
    'actstream',
    'modeltranslation',
    'openid_provider',
)

LOGIN_REDIRECT_URL = '/'
ACCOUNT_ACTIVATION_DAYS = 7
AUTH_PROFILE_MODULE = 'astrobin.UserProfile'

FLICKR_API_KEY = os.environ['ASTROBIN_FLICKR_API_KEY']
FLICKR_SECRET  = os.environ['ASTROBIN_FLICKR_SECRET']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    },
    'johnny': dict(
        BACKEND = 'johnny.backends.memcached.MemcachedCache',
        LOCATION = ['127.0.0.1:11211'],
        JOHNNY_CACHE = True,
    )
}
JOHNNY_MIDDLEWARE_KEY_PREFIX='jc_astrobin'

HAYSTACK_SITECONF = 'astrobin.search_sites'
HAYSTACK_SEARCH_ENGINE = 'solr'
HAYSTACK_SOLR_URL = os.environ['ASTROBIN_HAYSTACK_SOLR_URL']
HAYSTACK_DEFAULT_OPERATOR = 'AND'
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 24

#INTERNAL_IPS = ('88.115.221.254',) # for django-debug-toolbar: add own local IP to enable
INTERNAL_IPS = ('',)

MESSAGE_STORAGE = 'persistent_messages.storage.PersistentMessageStorage'

import djcelery
djcelery.setup_loader()

BROKER_HOST = 'localhost'
BROKER_PORT = 5672
BROKER_USER = os.environ['ASTROBIN_BROKER_USER']
BROKER_PASSWORD = os.environ['ASTROBIN_BROKER_PASSWORD']
BROKER_VHOST = 'astrobin'

CELERY_RESULT_BACKEND = 'database'
CELERY_RESULT_DBURI = os.environ['ASTROBIN_CELERY_RESULT_DBURI']
CELERY_IMPORTS = ('astrobin.tasks', )
CELERY_QUEUES = {"default" : {"exchange":"default", "binding_key":"default"},
                 "plate_solve": {"exchange":"plate_solve", "binding_key":"plate_solve_key"}
                }
CELERY_DEFAULT_QUEUE = "default"
CELERY_ROUTES = {"astrobin.tasks.solve_image" : {"queue":"plate_solve", "routing_key":"plate_solve_key"},
                 "astrobin.tasks.image_solved_callback" : {"queue":"plate_solve", "routing_key":"plate_solve_key"},
                }

CELERYD_NODES = "w1 w2 w3 w4"
CELERYD_OPTS = "--time-limit=300 --concurrency=8 --verbosity=2 --loglevel=DEBUG"
CELERYD_CHDIR = ASTROBIN_BASE_PATH
CELERYD_LOG_FILE = "celeryd.log"
CELERYD_PID_FILE = "celeryd.pid"
CELERYD = ASTROBIN_BASE_PATH + "manage.py celeryd"

CELERYBEAT = ASTROBIN_BASE_PATH + "manage.py celerybeat"
CELERYBEAT_OPTS = "--verbosity=2 --loglevel=DEBUG"

ASTROBIN_ENABLE_SOLVING = True

PRIVATEBETA_ENABLE_BETA = False
PRIVATEBETA_ALWAYS_ALLOW_VIEWS = (
    'astrobin.views.help',
    'astrobin.views.faq',
    'astrobin.views.set_language',
)

ASTROBIN_USER='astrobin'


SIMBAD_QUERY_URL="http://simbad.u-strasbg.fr/simbad/sim-nameresolver?data=@,I.0,J,C.0,T,D,M,I&output.max=1&output=json&option=strict&Ident="
SIMBAD_SEARCH_QUERY_URL="http://simbad.u-strasbg.fr/simbad/sim-nameresolver?data=@,I.0,J,C.0,T,D,M,I&output=json&Ident="

NOTIFICATION_LANGUAGE_MODULE = "astrobin.UserProfile"

ZINNIA_COPYRIGHT = 'AstroBin'
ZINNIA_MARKUP_LANGUAGE = 'html'
TINYMCE_JS_URL = MEDIA_URL + 'js/tiny_mce/tiny_mce.js'
TINYMCE_JS_ROOT = MEDIA_ROOT + '/js/tiny_mce'

HITCOUNT_KEEP_HIT_ACTIVE = { 'hours': 1 }
HITCOUNT_HITS_PER_IP_LIMIT = 0

AVATAR_GRAVATAR_BACKUP = False
AVATAR_DEFAULT_URL = 'images/astrobin-default-avatar.png?v=1'

STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'
STATICFILES_FINDERS = (
    'staticfiles.finders.FileSystemFinder',
    'staticfiles.finders.AppDirectoriesFinder',
)
STATICFILES_DIRS = (local_path('static/'),)

PIPELINE_STORAGE = 'pipeline.storage.PipelineFinderStorage'
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.cssmin.CssminCompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.jsmin.JSMinCompressor'

PIPELINE_CSS = {
    'screen': {
        'source_filenames': (
            'css/jquery-ui.css',
            'css/jquery-ui-astrobin/jquery-ui-1.8.17.custom.css',
            'css/ui.multiselect.css',
            'css/validationEngine.jquery.css',
            'css/facebox.css',
            'css/token-input.css',
            'css/jquery.multiselect.css',
            'css/jquery.qtip.css',

            'css/reset.css',
            'css/bootstrap.css',
            'css/bootstrap-responsive.css',
            'css/astrobin.css',
        ),
        'output_filename': 'css/astrobin_pipeline_screen_v' + MEDIA_VERSION + '.css',
        'extra_content':  {
            'media': 'screen, projection',
        },
    },
}

PIPELINE_JS = {
    'scripts': {
        'source_filenames': (
            'js/jquery-1.7.1.js',
            'js/jquery.i18n.js',
            'js/plugins/localization/jquery.localisation.js',
            'js/jquery.uniform.js',
            'js/jquery-ui-1.8.16.custom.min.js',
            'js/jquery.capty.js',
            'js/jquery-ui-timepicker-addon.js',
            'js/jquery.validationEngine-en.js',
            'js/jquery.validationEngine.js',
            'js/jquery.autoSuggest.js',
            'js/jquery.blockUI.js',
            'js/jquery.tmpl.1.1.1.js',
            'js/ui.multiselect.js',
            'js/plugins/scrollTo/jquery.scrollTo.js',
            'js/facebox.js',
            'js/jquery.form.js',
            'js/jquery.tokeninput.js',
            'js/jquery.flot.js',
            'js/jquery.flot.pie.min.js',
            'js/jquery.cycle.all.js',
            'js/jquery.easing.1.3.js',
            'js/jquery.multiselect.js',
            'js/jquery.qtip.js',
            'js/jquery.raty.js',
            'js/respond.src.js',
            'js/bootstrap.js',
            'js/astrobin.js',
        ),
        'output_filename': 'js/astrobin_pipeline_v' + MEDIA_VERSION + '.js',
    },
}

ACTSTREAM_ACTION_MODELS = (
    'auth.user',
    'astrobin.gear',
    'astrobin.telescope',
    'astrobin.camera',
    'astrobin.mount',
    'astrobin.filter',
    'astrobin.software',
    'astrobin.accessory',
    'astrobin.focalreducer',
    'astrobin.image',
    'astrobin.imagerevision',
)
