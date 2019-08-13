Porting from Aloe
====================

.. toctree::
    :maxdepth: 2

Eucalyptus_ is a fork of Aloe_ and is fully compatible with it. Some notable differences are:

 * Eucalyptus is pytest plugin and should gets invoked by running ```pytest```
 * The :option:`-n` option for running particular scenarios is renamed to
   :option:`--scenario-indices` since pytest does not allow single dash params
 * The :option:`-a` option is renamed to :option:`--tags` since pytest   does not allow 
  single dash params

