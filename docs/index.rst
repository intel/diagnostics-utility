.. sphinx bkms sandbox documentation master file, created by
   sphinx-quickstart on Thu Dec 17 04:58:51 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _index:

Diagnostics Utility for Intel® oneAPI Toolkits User Guide
=========================================================

.. raw:: latex

   \begingroup
   \textcolor{IntelClassicBlue-S2}{\rule{\textwidth}{.9pt}}
   \endgroup

The Diagnostics Utility for Intel® oneAPI Toolkits is designed to check your
configuration to verify it meets the requirements for using Intel® products.

With this utility, you can identify issues such as:

•	Permissions errors for the current user
•	Missing driver or an incompatible version of a driver
•	Incompatible version of the Operating System
•  Resource limits

Syntax
------

If you are viewing this document on GitHub, some text may appear as RST code.
To view a rendered version of this document, go to the
`User Guide on Intel Developer Zone <https://software.intel.com/content/www/us/en/develop/documentation/diagnostic-utility-user-guide/top.html>`_.



Supported Operating Systems
---------------------------

•	Ubuntu 18.04 LTS
•	Ubuntu 20.04 LTS
•	Ubuntu 22.04 LTS
•	RHEL 8.2
•	RHEL 8.3
•	SLES 15 SP2
•	SLES 15 SP3
•	Rocky Linux 8.5

Windows support is not included in the oneAPI toolkits. 
Very limited Windows support is available when building from the `public open source release <https://github.com/intel/diagnostics-utility>`_. 

•	Windows 10
•	Windows 11
•	Windows Server 2022


Requirements
------------

* Python 3.6 and newer

If your system meets the Diagnostics Utility for Intel® oneAPI Toolkits
requirements, click here to :ref:`cli-options`.

After running the Diagnostics Utility for Intel® oneAPI Toolkits for the first time,
explore :ref:`group-checks` and :ref:`verbosity` to see the flexibility of this
utility.

``---------------------``

.. toctree::
   :hidden:

   cli-options
   diagnose
   group-checks
   single-check
   verbosity
   customization
   custom-check
   pkg-contents

.. you may also add to the toctree, :caption: Contents

.. Indices and tables
.. ==================

.. * :ref:`search`

.. you may also add to the header above these

.. 	* :ref:`genindex`
.. 	* :ref:`modindex`

