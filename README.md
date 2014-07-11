`django-staging` allows you to easily manage your fixtures for testing or staging server

# Installation

Add `'staging'` to your `INSTALLED_APPS` and this to `settings.py`:

    import os

    def rel(*x):
        return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

    FIXTURE_DIRS = (
        rel('fixtures'),
    )

In order to use visual fixtures generation feature in Django1.7+, `'staging'` app should be placed before `'django.contrib.admin'` in `INSTALLED_APPS`.

# Usage

`save_staging` command saves data from your database to fixtures:

    $ ./manage.py save_staging auth main
    $ ./manage.py save_staging auth.User main

Fixtures are saved in `fixtures` folder of your project's application or in 'fixtures' folder in your project, with prefix `'staging_'`. All files from FileField or ImageField are saved in `MEDIA_ROOT+'staging'` folder, so you should not worry that files' urls are broken.

`load_staging` load all saved fixtures to your database:

    $ ./manage.py load_staging

'reset_staging' command recreate your database and load all saved fixtures:

    $ ./manage.py reset_staging

# Fixtures prefix

You can use option `--env` to save and load fixtures for some enviroment. `load_staging` load at first all staging fixtures, then fixtures saved with same `--env` option.

# Configuration

`STAGING_MEDIA_PATH` - folder in `MEDIA_ROOT` where files are saved. Default value is 'staging'.

# Visual fixtures generation

`staging_generator` command runs development server on 8000 port for localhost. If you access Django admin application using server started this way, you will see extra "Bulk data generation" button next to "Add object". It links to the page where you can define rules for bulk objects generation. Objects created in admin then can be saved to fixtures using `save_staging` command.

Examples are below:

    $ ./manage.py staging_generator

![Example1](https://github.com/code-on/django-staging/raw/master/examples/example1.png)

![Example2](https://github.com/code-on/django-staging/raw/master/examples/example2.png)

You can add your own generators. More details on generator attributes/methods in staging/generators/example.py. Generators are automatically loaded on start from this locations:

- generators directory in staging application
- path specified in `GENERATORS_DIR` environmental variable
- path specified with `--generators-dir` option for `staging_generator` command