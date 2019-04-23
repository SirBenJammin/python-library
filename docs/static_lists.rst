Static Lists
============

With the Static List endpoint, you can easily target and manage
lists of devices that are defined in your systems outside of Airship.
Any list or grouping of devices for which the canonical source of data about
the members is elsewhere is a good candidate for Static Lists, e.g., members
of a customer loyalty program.
For more information, see `the documentation on Static Lists
<https://docs.airship.com/api/ua/#tag/static-lists>`__


Create List
-----------

Creates a static list. The body of the request will contain several of the list
object parameters, but the actual list content will be provided by a second call
to the upload endpoint.

The StaticList class has two optional parameters including "description," which is a
user-provided description of the list, and "extra," which is a dictionary of
string keys to arbitrary JSON values.

.. code-block:: python

    airship = ua.Airship('app_key', 'master_secret')
    static_list = ua.devices.StaticList(airship, 'list_name')
    static_list.description = 'description'
    static_list.extra = { 'key': 'value' }
    static_list.create()


Upload List
-----------

Lists target identifiers are specified or replaced with an upload to this endpoint.
Uploads must be newline delimited identifiers (text/CSV) as described in RFC 4180,
with commas as the delimiter.

The CSV format consists of two columns: 'identifier_type' and 'identifier'.
'identifier_type' must be one of 'alias', 'named_user', 'ios_channel', 'android_channel',
or 'amazon_channel'. 'identifier' is the associated identifier you wish to send to.

The maximum number of 'identifier_type,identifier' pairs that may be uploaded to a list
is 10 million.

.. code-block:: python

    airship = ua.Airship('app_key', 'master_secret')
    static_list = ua.devices.StaticList(airship, 'list_name')
    csv_file = open(path, 'rb')
    resp = static_list.upload(csv_file)
    csv_file.close()


Update List
-----------

Updates the metadata of a static list.

.. code-block:: python

    airship = ua.Airship('app_key', 'master_secret')
    static_list = ua.devices.StaticList(airship, 'list_name')
    static_list.description = 'description'
    static_list.extra = { 'key': 'value' }
    static_list.update()


Delete List
-----------

Delete a static list.

.. code-block:: python

    airship = ua.Airship('app_key', 'master_secret')
    static_list = ua.devices.StaticList(airship, 'list_name')
    static_list.delete()

.. note::
    If you are attempting to update a current list by deleting it
    and then recreating it with new data, use the upload
    endpoint. There is no need to delete a list before uploading a
    new CSV file. Moreover, once you delete a list you will be unable
    to create a list with the same name as the deleted list.


Lookup List
-----------

Retrieve information about one static list.

.. code-block:: python

    airship = ua.Airship('app_key', 'master_secret')
    static_list = ua.devices.StaticList(airship, 'list_name')
    static_list.lookup()

.. note::
    When looking up lists, the returned information may actually be a combination
    of values from both the last uploaded list and the last successfully processed
    list. If you create a list successfully, and then you update it and the
    processing step fails, then the list status will read "failed", but the
    channel_count and last_modified fields will contain information on the last
    successfully processed list.


Lookup All Lists
----------------

Retrieve information about all static lists. This call returns a paginated list of
metadata that will not contain the lists of users.

.. code-block:: python

    airship = ua.Airship('app_key', 'master_secret')
    static_list = ua.devices.StaticLists(airship)

    for resp in static_list:
        print(
            resp.name,
            resp.description,
            resp.extra,
            resp.created,
            resp.last_updated,
            resp.channel_count,
            resp.status
        )
