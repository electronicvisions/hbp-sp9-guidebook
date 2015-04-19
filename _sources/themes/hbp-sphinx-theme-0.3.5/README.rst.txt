.. _collaboratory: https://collab.humanbrainproject.eu
.. _bower: http://www.bower.io
.. _sphinx: http://www.sphinx-doc.org
.. _sass: http://www.sass-lang.com
.. _wyrm: http://www.github.com/snide/wyrm/
.. _grunt: http://www.gruntjs.com
.. _node: http://www.nodejs.com
.. _demo: https://collab.humanbrainproject.eu/#/collab/54/nav/368
.. _repository: https://github.com/HumanBrainProject/hbp-sphinx-theme
.. _release: https://github.com/HumanBrainProject/hbp-sphinx-theme/releases/latest
.. _documentation example: https://github.com/HumanBrainProject/hbp-collaboratory-doc-example

.. image:: https://travis-ci.org/HumanBrainProject/hbp-sphinx-theme.svg?branch=master
    :target: https://travis-ci.org/HumanBrainProject/hbp-sphinx-theme

******************************
HBP Collaboratory Sphinx Theme
******************************

.. contents::

View a working demo_ over on collaboratory_.

This package provide a Sphinx theme for documentation integrated into the
Collaboratory. It can be used for standalone websites as well.

.. image:: screen_integrated.png
    :width: 100%

Installation
============

Via package
-----------

Download the package or add it to your requirements.txt file:

.. code:: bash

   pip install hbp_sphinx_theme


In your conf.py file:

.. code:: Python

   import hbp_sphinx_theme
   html_theme = "hbp_sphinx_theme"
   html_theme_path = [hbp_sphinx_theme.get_html_theme_path()]


Via download
------------

Download the ``hbp_sphinx_theme.zip`` provided by the latest release_
to your documentation project directory.

As explained in `sphinx documentation`__, in your ``conf.py`` file:

__ http://sphinx-doc.org/theming.html#using-a-theme


.. code:: python

    html_theme = 'hbp_sphinx_theme'
    html_theme_path = ['.']


Contributing or modifying the theme
===================================

HBP Collaboratory Sphinx Theme github project can be included in your documentation
project as a git submodule. This will enable you to modify the theme and see the
changes immediately in your browser. Please have a look at the `documentation example`_
project on how to set up. After you are happy with the changes, you've made to the theme,
please make a pull request for us to review.

Build and release the theme
===========================

The build and release is done using grunt.

.. code:: bash

    grunt release

`Changelog`__

__ CHANGELOG.md
