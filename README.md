`django-stagin` allows you to easily manage your fixtures for testing or staging server

# Installation

Add `'staging'` to your `INSTALLED_APPS` and this to `settings.py`:

    import os

    def rel(*x):
        return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

    FIXTURE_DIRS = (
        rel('fixtures'),
    )

# Usage

`save_staging` command saves data from your database to fixtures:

    $ ./manage.py save_staging auth main
    $ ./manage.py save_staging auth.User main

Fixtures are saved in `fixtures` folder of your project's application or in 'fixtures' folder in your project, with prefix `'staging_'`. All files from FileField or ImageField are saved in MEDIA_ROOT+'staging' folder, so you should not worry that files' urls are broken.

`load_staging` load all saved fixtures to your database:

    $ ./manage.py load_staging

'reset_staging' command recreate your database and load all saved fixtures:

    $ ./manage.py reset_staging

# Configuration

`STAGING_MEDIA_PATH` - folder in `MEDIA_ROOT` where files are saved. Default value is 'staging'.
