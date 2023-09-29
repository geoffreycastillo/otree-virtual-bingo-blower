from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1.00,
    'doc': "",
    'participation_fee': 10
    }

PROLIFIC_SESSIONS = {
    'completion_code': 'TO CHANGE',
    }

SESSION_CONFIGS = [
    {
        'name': 'prolific_randomise_all',
        'display_name': "Measure ambiguity: randomise between all blower and DOW",
        'num_demo_participants': 10,
        'app_sequence': ['intro', 'consent', 'measure_ambiguity_instructions_control', 'measure_ambiguity', 'outro'],
        'treatments': ['blower-10', 'blower-60', 'dow'],
        'DOW_date': '2022-02-05',
        'participation_fee': 1,
        **PROLIFIC_SESSIONS
        },
    {
        'name': 'prolific_dow',
        'display_name': "Measure ambiguity: Dow only",
        'num_demo_participants': 10,
        'app_sequence': ['intro', 'consent', 'measure_ambiguity_instructions_control', 'measure_ambiguity', 'outro'],
        'treatments': ['dow'],
        'DOW_date': '2022-02-05',
        'participation_fee': 2,
        **PROLIFIC_SESSIONS
        },
    {
        'name': 'BOT_measure_ambiguity_blower_10',
        'display_name': "[BOT] Measure ambiguity: blower, 10 balls",
        'num_demo_participants': 10,
        'app_sequence': ['measure_ambiguity_instructions_control', 'measure_ambiguity'],
        'treatments': ['blower-10'],
        'number_balls': [6, 15, 9],
        'show_proportions': True,
        **PROLIFIC_SESSIONS,
        'use_browser_bots': True
        },
    {
        'name': 'BOT_measure_ambiguity_DOW',
        'display_name': "[BOT] Measure ambiguity: DOW",
        'num_demo_participants': 10,
        'app_sequence': ['measure_ambiguity_instructions_control', 'measure_ambiguity'],
        'treatments': ['dow'],
        'DOW_date': '2022-02-05',
        **PROLIFIC_SESSIONS,
        'use_browser_bots': True
        }
    ]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en-gb'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'GBP'
REAL_WORLD_CURRENCY_DECIMAL_PLACES = 0
USE_POINTS = False

ROOMS = [
    dict(
        name='VCEEroom',
        display_name='VCEE Room'
        ),
    dict(
        name='prolific',
        display_name='Prolific'
        ),
    ]

# AUTH_LEVEL:
# this setting controls which parts of your site are freely accessible,
# and which are password protected:
# - If it's not set (the default), then the whole site is freely accessible.
# - If you are launching a study and want visitors to only be able to
#   play your app if you provided them with a start link, set it to STUDY.
# - If you would like to put your site online in public demo mode where
#   anybody can play a demo version of your game, but not access the rest
#   of the admin interface, set it to DEMO.

# for flexibility, you can set it in the environment variable OTREE_AUTH_LEVEL
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

# Consider '', None, and '0' to be empty/false
DEBUG = (environ.get('OTREE_PRODUCTION') in {None, '', '0'})

DEMO_PAGE_INTRO_HTML = """
Bingo blower experiments.
"""

# don't share this with anybody.
SECRET_KEY = 'supersecretkey'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = [
    'otree'
    ]
