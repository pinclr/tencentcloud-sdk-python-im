Usage
=====

.. _installation:

Installation
------------

To use the library, first install it using pip:

.. code-block:: console

   (.venv) $ pip install tencentcloud-sdk-python-im

Creating API Client
-------------------

To get the api client for the tencentcloud-sdk-python-im,
you can use the ``TCIMClient()``

For example:

>>> from tencentcloud_im.tcim_client import TCIMClient
>>> client = TCIMClient(sdk_id, sdk_secret, admin_account)
