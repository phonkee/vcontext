import operator
import unittest

from context import Context


class ContextTest(unittest.TestCase):

    def test_set(self):

        prefix = "oops.i.did.it.again"
        data = [
            {'value': 'Hello', 'index': 0},
            {'value': 'Sandy', 'index': 44},
            {'value': 'World', 'index': 5},
        ]

        data.sort(key=lambda x: x['index'])

        context = Context()
        for item in data:
            key = '.'.join((prefix, str(item['index'])))
            context[key] = item['value']
            self.assertEqual(len(context[prefix]), item['index'] + 1)

        mi = max(data, key=lambda item: item['index'])
        self.assertEqual(len(context[prefix]), mi['index'] + 1)

    def test_delete(self):
        context = Context()
        context['hello.how.are.you.0'] = 'world'
        del context['hello.how.are.you.0']
        self.assertEqual(len(context['hello.how.are.you']), 0)

    def test_getitem_method_call(self):
        class Shout(object):
            def shout(self):
                return "shout"

        class Shine(object):
            def shine(self):
                return "shine"

        context = Context()
        context['hello.test_call'] = Shout
        self.assertEqual(context['hello.test_call.shout'], "shout")

    def test_object(self):
        """
        Test access to object attributes
        """

if __name__ == "__main__":
    unittest.main()
