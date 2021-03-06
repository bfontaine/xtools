.. xtools documentation master file, created by
   sphinx-quickstart on Sun May 10 18:13:31 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ``xtools``' documentation!
=====================================

``xtools`` is a Python wrapper around XTools_’ API.

Note this project is not affiliated with nor endorsed by XTools.

.. _XTools: https://xtools.wmflabs.org/

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Install
~~~~~~~

::

   pip install xtools

Usage
~~~~~

Functions are divided in four modules, exactly like the XTools API. They are also available under the top-level
``xtools`` module: ``xtools.top_edits`` is the same as ``xtools.user.top_edits``, etc.


``xtools.project``
------------------

.. automodule:: xtools.project
   :members:


``xtools.page``
---------------

.. automodule:: xtools.page
   :members:


``xtools.user``
---------------

.. automodule:: xtools.user
   :members:


``xtools.quote``
----------------

.. automodule:: xtools.quote
   :members:
