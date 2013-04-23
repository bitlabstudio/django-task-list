Django Task List
================

A reusable Django app to attach task lists to models and let them be managed by
multiple users.


Installation
------------

You need to install the following prerequisites in order to use this app::

    pip install Django
    pip install South

If you want to install the latest stable release from PyPi::

    $ pip install django-task-list

If you feel adventurous and want to install the latest commit from GitHub::

    $ pip install -e git://github.com/bitmazk/django-task-list.git#egg=task_list

Add ``task_list`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...,
        'task_list',
    )

Run the South migrations::

    ./manage.py migrate task_list


Usage
-----

TODO: describte usage

Contribute
----------

If you want to contribute to this project, please perform the following steps::

    # Fork this repository
    # Clone your fork
    $ mkvirtualenv -p python2.7 django-task-list
    $ pip install -r requirements.txt
    $ ./logger/tests/runtests.sh
    # You should get no failing tests

    $ git co -b feature_branch master
    # Implement your feature and tests
    # Describe your change in the CHANGELOG.txt
    $ git add . && git commit
    $ git push origin feature_branch
    # Send us a pull request for your feature branch

Whenever you run the tests a coverage output will be generated in
``tests/coverage/index.html``. When adding new features, please make sure that
you keep the coverage at 100%.


Roadmap
-------

Check the issue tracker on github for milestones and features to come.
