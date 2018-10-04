Defining and Sending Push Notifications
=======================================

The Urban Airship Python Library strives to match the standard Urban
Airship JSON format for specifying push notifications. When creating a
push notification, you:

#. Select the audience
#. Define the notification payload
#. Specify device types.
#. Deliver the notification.

This example performs a broadcast with the same alert to all recipients
and device types:

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, master_secret)

   push = airship.create_push()
   push.audience = ua.all_
   push.notification = ua.notification(alert='Hello, world!')
   push.device_types = ua.all_
   push.send()


Audience Selectors
------------------

An audience should specify one or more devices. An audience can be a
device, such as a ``channel``, ``device_token`` or ``apid``; a tag,
alias, or segment; a location; or a combination. Audience selectors are
combined with ``and_``, ``or_``, and ``not_``.

.. py:data:: urbanairship.push.all_

   Select all, to do a broadcast.

   Used in both ``audience`` and ``device_types``.

   .. code-block:: python

      push.audience = ua.all_


.. automodule:: urbanairship.push.audience
   :members:
   :noindex:


Notification Payload
--------------------

The notification payload determines what message and data is sent to a
device. At its simplest, it consists of a single string-valued
attribute, ``alert``, which sends a push notification consisting of a
single piece of text:

.. code-block:: python

   push.notification = ua.notification(alert='Hello, world!')

You can override the payload with platform-specific values as well.

.. automodule:: urbanairship.push.payload
   :members: notification, ios, android, wns_payload, open_platform, sms, email


In-App Message
--------------

The in-app message payload is an object assigned to the in_app attribute
on a push object. Aside from the display and display_type attributes,
which specify the appearance of the in-app message, the in_app object looks
very similar to a push object.  In-app messages do not require
push.notification to be set:

.. code-block:: python

    push.in_app = ua.in_app(
      alert='Alert Message',
      display_type='banner'
      display={
        'position':'top'
      }
    )

.. automodule:: urbanairship.push.payload
   :members: in_app
   :noindex:


Actions
-------

Urban Airship Actions provides a convenient way to automatically
perform tasks by name in response to push notifications,
Rich App Page interactions and JavaScript. More information at
http://docs.urbanairship.com/api/ua.html#actions, example:

.. code-block:: python

   push.notification = ua.notification(
          alert='Hello, world!',
          actions=ua.actions(
              add_tag='new_tag',
              remove_tag='old_tag',
              share='Check out Urban Airship!',
              open_={
                  'type': 'url',
                  'content': 'http://www.urbanairship.com'
              },
              app_defined={
                  'some_app_defined_action': 'some_values'
              }
          )
   )

.. automodule:: urbanairship.push.payload
   :members: notification, actions, ios, android, amazon
   :noindex:


Interactive Notifications
-------------------------

The interactive notification payload determines the ways you can interact
with a notification. It contains two attributes: ``type`` (mandatory) and
``button_actions`` (optional). More information at
http://docs.urbanairship.com/api/ua.html#interactive-notifications
Example:

.. code-block:: python

    push.notification = ua.notification(
        alert='Hello, world!',
        interactive=ua.interactive(
            type = 'ua_share',
            button_actions = {
                    'share' : { 'share' : 'Sharing is caring!'}
            }
        )
    )

Button actions can also be mapped to *actions* objects as shown below:

.. code-block:: python

    shared = ua.actions(share='Sharing is caring!')
    push.notification = ua.notification(
        alert='Hello, world!',
        interactive=ua.interactive(
            type = 'ua_share',
            button_actions = {
                    'share' : shared
            }
        )
    )

.. automodule:: urbanairship.push.payload
   :members: notification, interactive
   :noindex:


Device Types
------------

In addition to specifying the audience, you must specify the device
types you wish to target, either with a list of strings:

.. code-block:: python

   push.device_types = ua.device_types('ios', 'android', 'web')

or with the ``all_`` shortcut.

.. code-block:: python

   push.device_types = ua.all_

.. autofunction:: urbanairship.push.payload.device_types


Delivery
--------

Once you have set the ``audience``, ``notification``, and ``device_types``
attributes, the notification is ready for delivery.

.. code-block:: python

   push.send()

If the delivery is unsuccessful, an :py:class:`AirshipFailure` exception
will be raised.

.. autoclass:: urbanairship.push.core.Push
   :members:


Scheduled Delivery
------------------

Scheduled notifications build upon the Push object, and have two other
components: the scheduled time(s) and an optional name.

This example schedules the above notification for delivery in one
minute.

.. code-block:: python

   import datetime

   schedule = airship.create_scheduled_push()
   schedule.push = push
   schedule.name = 'optional name for later reference'
   schedule.schedule = ua.scheduled_time(
       datetime.datetime.utcnow() + datetime.timedelta(minutes=1))
   response = schedule.send()

   print ('Created schedule. url:', response.schedule_url)

If the schedule is unsuccessful, an :py:class:`AirshipFailure`
exception will be raised.

.. autoclass:: urbanairship.push.core.ScheduledPush
   :members:


Scheduled Delivery in Device Local Time
---------------------------------------

Scheduled notifications build upon the Push object, and have two other
components: the scheduled time(s) and an optional name.

This example schedules the above notification for delivery in device
local time.

.. code-block:: python

   import datetime

   schedule = airship.create_scheduled_push()
   schedule.push = push
   schedule.name = 'optional name for later reference'
   schedule.schedule = ua.local_scheduled_time(
       datetime.datetime(2015, 4, 1, 8, 5))
   response = schedule.send()

   print ('Created schedule. url:', response.schedule_url)

If the schedule is unsuccessful, an :py:class:`AirshipFailure` exception
will be raised.

.. autoclass:: urbanairship.push.core.ScheduledPush
   :members:


Schedule Push Time Send Optimization
------------------------------------

Scheduled notifications build upon the Push object, and have two other
components: the date for best time delivery and an optional name.

This example schedules the above notification for delivery to the
devices' best time.

.. code-block:: python

    import datetime

    schedule = airship.create_scheduled_push()
    schedule.push = push
    schedule.name = 'optional name for later reference'
    schedule.schedule = ua.best_time(
       datetime.datetime(2018, 10, 2))
    response = schedule.send()

    print ('Created schedule. url:', response.schedule_url)

If the schedule is unsuccessful, an :py:class:`AirshipFailure` exception
will be raised.

.. autoclass:: urbanairship.push.core.ScheduledPush
   :members:


Updating or Canceling a Schedule
--------------------------------

If you have the ``schedule_url`` returned from creating a scheduled
notification, you can update or cancel it before it's sent.

.. code-block:: python

   schedule = ua.ScheduledPush.from_url(airship, url)
   # change scheduled time to tomorrow
   schedule.schedule = ua.scheduled_time(
       datetime.datetime.utcnow() + datetime.timedelta(days=1))
   schedule.update()

   # Cancel
   schedule.cancel()


Scheduled Message Listing
-------------------------

List all pending Scheduled and Scheduled to Device Local Time messages on a project:

   .. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, master_secret)

   for schedule in ua.ScheduledList(airship):
      print(
         schedule.name, schedule.url, schedule.push_ids,
         schedule.schedule, schedule.push
      )

.. autoclass:: urbanairship.push.schedule.ScheduledList
   :members:


Personalized Push with a Template
---------------------------------

If you want to use an existing template to send a push, follow this example:

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, master_secret)

   push = airship.create_template_push()
   push.audience = ua.ios_channel('b8f9b663-0a3b-cf45-587a-be880946e881')
   push.device_types = ua.device_types('ios')
   push.merge_data = ua.merge_data(
       template_id='ef34a8d9-0ad7-491c-86b0-aea74da15161',
       substitutions={
           'FIRST_NAME': 'Bob',
           'LAST_NAME': 'Smith',
           'TITLE': ''
       }
   )
   push.send()


Notice that you do not include a notification, as that is already defined by
the template. Instead, you include merge data, which is made up of the template
ID and the field substitutions. The example above sends to a particular iOS
channel.

.. autoclass:: urbanairship.push.core.TemplatePush
   :members:


Template Lookup
---------------

Look up a previously created template:

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, master_secret)

   template_id = 'ef34a8d9-0ad7-491c-86b0-aea74da15161'
   template = ua.Template(airship).lookup(template_id)
   print (
       template.template_id, template.created_at, template.modified_at,
       template.last_used, template.name, template.description,
       template.variables, template.push
   )

.. autoclass:: urbanairship.push.template.Template
   :members:
   :exclude-members: from_payload


Template Listing
----------------

List all previously created templates on an app:

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, master_secret)

   for template in ua.TemplateList(airship):
      template_id = template.template_id
      print (
          template.template_id, template.created_at, template.modified_at,
          template.last_used, template.name, template.description,
          template.variables, template.push
      )


.. autoclass:: urbanairship.push.template.TemplateList
   :members:
   :exclude-members: instance_class


Template Creation
-----------------

Create a new template:

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, master_secret)

   new_template = ua.Template(airship)
   new_template.name = 'Welcome Message'
   new_template.description = 'Our welcome message'
   new_template.variables = [
        {
            'key': 'TITLE',
            'name': 'Title',
            'description': 'e.g. Mr., Ms., Dr., etc.',
            'default_value': ''
        },
        {
            'key': 'FIRST_NAME',
            'name': 'First Name',
            'description': 'Given name',
            'default_value': None
        },
        {
            'key': 'LAST_NAME',
            'name': 'Last Name',
            'description': 'Family name',
            'default_value': None
        }
   ]
   new_template.push = {
       'notification': {
           'alert': 'Hello {{TITLE}} {{FIRST_NAME}} {{LAST_NAME}}!'
       }
   }
   new_template.create()
   print (new_template.template_id)  # To get the template ID for future use


Template Update
---------------

Create a new template object and define only the components of the template
that you want to change:

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, master_secret)

   template_id = 'ef34a8d9-0ad7-491c-86b0-aea74da15161'

   updated_template = ua.Template(airship)
   updated_template.push = {
       'notification': {
           'alert': 'Goodbye {{TITLE}} {{FIRST_NAME}} {{LAST_NAME}}!'
       }
   }
   updated_template.update(template_id)


You can also look up an existing template, put it in a Template object (where
you can check out what's currently in there), then change only what you want
to change:

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, master_secret)

   template_id = 'ef34a8d9-0ad7-491c-86b0-aea74da15161'

   updated_template = ua.Template(airship).lookup(template_id)
   updated_template.push = {
       'notification': {
           'alert': 'Goodbye {{TITLE}} {{FIRST_NAME}} {{LAST_NAME}}!'
       }
   }
   updated_template.update()


Template Deletion
-----------------

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, master_secret)

   template_id = 'ef34a8d9-0ad7-491c-86b0-aea74da15161'

   # Delete via template lookup
   ua.Template(airship).lookup(template_id).delete()

   # OR, if you want to delete a template without fetching it from the API
   ua.Template(airship).delete(template_id)

