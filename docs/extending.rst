.. _extending_aloe:

Extending Eucalyptus_
==============

Since Eucalyptus_ is a fork of Aloe_ this pages covers Aloe internals which should not be different from original docs.

.. toctree::
    :maxdepth: 2

.. autoclass:: aloe.testclass.TestCase()

   Eucalyptus runs all tests within a :class:`unittest.TestCase`. You can extend
   this class to run your tests with certain other features, i.e. using
   Django's ``TestCase``.

Extensions
==========

.. toctree::
    :maxdepth: 2

* `aloe_django`_ -- Django integration for `Aloe`.
* `aloe_webdriver`_ -- Selenium integration for `Aloe`.

.. include:: links.rst
