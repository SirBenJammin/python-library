import unittest

import urbanairship as ua


class TestAudience(unittest.TestCase):
    def test_basic_selectors(self):
        selectors = (
            (
                ua.ios_channel,
                '074e84a2-9ed9-4eee-9ca4-cc597bfdbef3',
                {'ios_channel': '074e84a2-9ed9-4eee-9ca4-cc597bfdbef3'}
            ),
            (
                ua.android_channel,
                '074e84a2-9ed9-4eee-9ca4-cc597bfdbef3',
                {'android_channel': '074e84a2-9ed9-4eee-9ca4-cc597bfdbef3'}
            ),
            (
                ua.amazon_channel,
                '074e84a2-9ed9-4eee-9ca4-cc597bfdbef3',
                {'amazon_channel': '074e84a2-9ed9-4eee-9ca4-cc597bfdbef3'}
            ),
            (
                ua.open_channel,
                '074e84a2-9ed9-4eee-9ca4-cc597bfdbef3',
                {'open_channel': '074e84a2-9ed9-4eee-9ca4-cc597bfdbef3'}
            ),
            (
                ua.device_token,
                'f' * 64,
                {'device_token': 'F' * 64},
            ),
            (
                ua.device_token,
                '0' * 64,
                {'device_token': '0' * 64}
            ),
            (
                ua.apid,
                '074e84a2-9ed9-4eee-9ca4-cc597bfdbef3',
                {'apid': '074e84a2-9ed9-4eee-9ca4-cc597bfdbef3'}
            ),
            (
                ua.wns,
                '074e84a2-9ed9-4eee-9ca4-cc597bfdbef3',
                {'wns': '074e84a2-9ed9-4eee-9ca4-cc597bfdbef3'}
            ),
            (
                ua.tag,
                'test',
                {'tag': 'test'}
            ),
            (
                ua.alias,
                'test',
                {'alias': 'test'}
            ),
            (
                ua.segment,
                'test',
                {'segment': 'test'}
            )
        )

        for selector, value, result in selectors:
            self.assertEqual(selector(value), result)


    def test_sms_selectors(self):
        sms_id_selector = ua.sms_id('01230984567', '76543210')

        self.assertEqual(
            sms_id_selector,
            {'sms_id': {'sender': '76543210', 'msisdn': '01230984567'}}
        )

        sms_sender_selector = ua.sms_sender('76543210')

        self.assertEqual(
            sms_sender_selector,
            {'sms_sender': '76543210'}
        )


    def test_invalid_device_selectors(self):
        selectors = (
            (ua.ios_channel, '074e84a2-9ed9-4eee-9ca4-cc597bfdbef34'),
            (ua.android_channel, '074e84a2-9ed9-Beee-9ca4-ccc597bfdbef3'),
            (ua.amazon_channel, '074e84a2-Red9-5eee-0ca4-cc597bfdbef3'),
            (ua.open_channel, '074e84a2-OPEN-UP-0ca4-cc597bfdbef3'),
            (ua.device_token, 'f' * 63),
            (ua.device_token, 'f' * 65),
            (ua.device_token, '0123'),
            (ua.device_token, 'X' * 64),
            (ua.apid, 'foobar'),
            (ua.apid, '074e84a2-9ed9-4eee-9ca4-cc597bfdbef33'),
            (ua.apid, '074e84a2-9ed9-4eee-9ca4-cc597bfdbef'),
            (ua.wns, '074e84a2-9ed9-4eee-9ca4-cc597bfdbef'),
        )

        for selector, value in selectors:
            self.assertRaises(ValueError, selector, value)

    def test_compound_selectors(self):
        self.assertEqual(
            ua.or_(
                ua.tag('foo'),
                ua.tag('bar')
            ),
            {'or': [
                {'tag': 'foo'},
                {'tag': 'bar'}
            ]}
        )

        self.assertEqual(
            ua.and_(
                ua.tag('foo'),
                ua.tag('bar')
            ),
            {
                'and': [
                    {'tag': 'foo'},
                    {'tag': 'bar'}
                ]
            }
        )

        self.assertEqual(
            ua.not_(
                ua.tag('foo')
            ),
            {
                'not': {
                    'tag': 'foo'
                }
            }
        )

    def test_time_period_selector(self):
        self.assertEqual(
            ua.recent_date(days=4),
            {
                'recent': {
                    'days': 4
                }
            }
        )
        self.assertEqual(
            ua.absolute_date(
                resolution='days',
                start='2012-01-01',
                end='2012-01-15'
            ),
            {
                'days': {
                    'start': '2012-01-01',
                    'end': '2012-01-15'
                }
            }
        )
        self.assertEqual(
            ua.absolute_date(
                resolution='weeks',
                start='2012-01-01',
                end='2012-01-15'
            ),
            {
                'weeks': {
                    'start': '2012-01-01',
                    'end': '2012-01-15'
                }
            }
        )

        # Invalid time periods
        self.assertRaises(ValueError, ua.recent_date, hours=1, minutes=1)
        self.assertRaises(ValueError, ua.recent_date, eons=1)
        self.assertRaises(
            ValueError,
            ua.absolute_date,
            'eons',
            'alpha',
            'omega'
        )

    def test_location_selector(self):
        self.assertEqual(
            ua.location(
                id='a_location_id',
                date=ua.recent_date(days=4)
            ),
            {
                'location': {
                    'id': 'a_location_id',
                    'date': {'recent': {'days': 4}}
                }
            }
        )

        self.assertRaises(ValueError, ua.location)
        self.assertRaises(ValueError, ua.location, alias=1, id=1)
        self.assertRaises(ValueError, ua.location, date=None, id='foobar')
