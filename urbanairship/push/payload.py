import re

# Valid autobadge values: auto, +N, -N
VALID_AUTOBADGE = re.compile(r'^(auto|[+-][\d]+)$')


def notification(alert=None, ios=None, android=None, blackberry=None, wns=None,
        mpns=None):
    """Create a notification payload.

    :keyword alert: A simple text alert, applicable for all platforms.
    :keyword ios: An iOS platform override, as generated by :py:func:`ios`.
    :keyword android: An Android platform override, as generated by :py:func:`android`.
    :keyword blackberry: A BlackBerry platform override, as generated by :py:func:`blackberry`.
    :keyword wns: A WNS platform override, as generated by :py:func:`wns`.
    :keyword mpns: A MPNS platform override, as generated by :py:func:`mpns`.

    """
    payload = {}
    if alert is not None:
        payload['alert'] = alert
    if ios is not None:
        payload['ios'] = ios
    if android is not None:
        payload['android'] = android
    if blackberry is not None:
        payload['blackberry'] = blackberry
    if wns is not None:
        payload['wns'] = wns
    if mpns is not None:
        payload['mpns'] = mpns
    if not payload:
        raise ValueError("Notification body may not be empty")
    return payload


def ios(alert=None, badge=None, sound=None, content_available=False,
        extra=None, expiry=None):
    """iOS/APNS specific platform override payload.

    :keyword alert: iOS format alert, as either a string or dictionary.
    :keyword badge: An integer badge value or an *autobadge* string.
    :keyword sound: An string sound file to play.
    :keyword content_available: If True, pass on the content_available command
        for Newsstand iOS applications.
    :keyword extra: A set of key/value pairs to include in the push payload
        sent to the device.
    :keyword expiry: An integar or time set in UTC as a string
    >>> ios(alert='Hello!', sound='cat.caf',
    ...     extra={'articleid': '12345'})
    {'sound': 'cat.caf', 'extra': {'articleid': '12345'}, 'alert': 'Hello!'}

    """
    payload = {}
    if alert is not None:
        if not (isinstance(alert, basestring) or isinstance(alert, dict)):
            raise ValueError("iOS alert must be a string or dictionary")
        payload['alert'] = alert
    if badge is not None:
        if not (isinstance(badge, basestring) or isinstance(badge, int)):
            raise ValueError("iOS badge must be an integer or string")
        if isinstance(badge, basestring) and not VALID_AUTOBADGE.match(badge):
            raise ValueError("Invalid iOS autobadge value")
        payload['badge'] = badge
    if sound is not None:
        payload['sound'] = sound
    if content_available:
        payload['content-available'] = 1
    if extra is not None:
        payload['extra'] = extra
    if expiry is not None:         
        payload['expiry'] = expiry 
    return payload


def android(alert=None, collapse_key=None, time_to_live=None,
        delay_while_idle=False, extra=None):
    """Android specific platform override payload.

    All keyword arguments are optional.

    :keyword alert: String alert text.
    :keyword collapse_key: String
    :keyword time_to_live: Integer
    :keyword delay_while_idle: Boolean
    :keyword extra: A set of key/value pairs to include in the push payload
        sent to the device. All values must be strings.

    See
    `GCM Advanced Topics <http://developer.android.com/google/gcm/adv.html>`_
    for details on ``collapse_key``, ``time_to_live``, and
    ``delay_while_idle``.

    >>> ios(alert='Hello!', sound='cat.caf',
    ...     extra={'articleid': '12345'})
    {'sound': 'cat.caf', 'extra': {'articleid': '12345'}, 'alert': 'Hello!'}

    """
    payload = {}
    if alert is not None:
        payload['alert'] = alert
    if collapse_key is not None:
        payload['collapse_key'] = collapse_key
    if time_to_live is not None:
        payload['time_to_live'] = time_to_live
    #add validation function - needs testing
        if not (isinstance(time_to_live, basestring) or isinstance(time_to_live, int)):
            raise ValueError("Android time_to_live value must be an integar or time set in UTC as a string")
    if delay_while_idle:
        payload['delay_while_idle'] = True
    if extra is not None:
        payload['extra'] = extra
    return payload

    #soon-to-be merged code will include
    #Amazon payload: expires_after
    #add validation function


def blackberry(alert=None, body=None, content_type=None):
    """BlackBerry specific platform override payload.

    Include either ``alert`` or both ``body`` and ``content_type``.

    :keyword alert: String alert text. Shortcut for ``content_type``
        ``text/plain``.
    :keyword body: String value.
    :keyword content_type: MIME type describing body.

    """
    payload = {}
    if alert is not None:
        payload['body'] = alert
        payload['content_type'] = 'text/plain'
    elif body is not None and content_type is not None:
        payload['body'] = body
        payload['content_type'] = content_type
    else:
        raise ValueError("BlackBerry body and content_type may not be empty")
    return payload


def wns_payload(alert=None, toast=None, tile=None, badge=None):
    """WNS specific platform override payload.

    Must include exactly one of ``alert``, ``toast``, ``tile``, or ``badge``.

    """
    if len(filter(None, (alert, toast, tile, badge))) != 1:
        raise ValueError("WNS payload must have one notification type.")
    payload = {}
    if alert is not None:
        payload['alert'] = alert
    if toast is not None:
        payload['toast'] = toast
    if tile is not None:
        payload['tile'] = tile
    if badge is not None:
        payload['badge'] = badge
    return payload


def mpns_payload(alert=None, toast=None, tile=None):
    """MPNS specific platform override payload.

    Must include exactly one of ``alert``, ``toast``, or ``tile``.

    """
    if len(filter(None, (alert, toast, tile))) != 1:
        raise ValueError("MPNS payload must have one notification type.")
    payload = {}
    if alert is not None:
        payload['alert'] = alert
    if toast is not None:
        payload['toast'] = toast
    if tile is not None:
        payload['tile'] = tile
    return payload


def message(title, body, content_type=None, content_encoding=None, extra=None, expiry=None):
    """Rich push message payload creation.

    :param title: Required, string
    :param body: Required, string
    :keyword content_type: Optional, MIME type of the body
    :keyword content_encoding: Optional, encoding of the data in body, e.g.
        ``utf-8``.
    :keyword extra: Optional, dictionary of string values.
    :keyword expiry: time when message will delete from Inbox (UTC time or in seconds)

    """
    payload = {
        'title': title,
        'body': body,
    }
    if content_type is not None:
        payload['content_type'] = content_type
    if content_encoding is not None:
        payload['content_encoding'] = content_encoding
    if extra is not None:
        payload['extra'] = extra
    if expiry is not None:     
        payload['expiry'] = expiry
    # add validation function
    return payload


def device_types(*types):
    """Create a device type specifier.

    >>> device_types('ios', 'wns')
    ['ios', 'wns']
    >>> device_types('ios', 'symbian')
    Traceback (most recent call last):
        ...
    ValueError: Invalid device type 'symbian'

    """
    if len(types) == 1 and types[0] == 'all':
        return 'all'
    for t in types:
        if t not in ('ios', 'android', 'blackberry', 'wns', 'mpns'):
            raise ValueError("Invalid device type '%s'" % t)
    return [t for t in types]

def options(expiry=None):
    if expiry is not None:
        payload['expiry'] = expiry
    return payload
