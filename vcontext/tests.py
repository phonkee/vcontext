import unittest
from context import Context


class ContextTest(unittest.TestCase):

    def test_set(self):

        context = Context()
        context['hello.how.are.you.0'] = 'world'
        self.assertEqual(len(context['hello.how.are.you']), 1)

        context['hello.how.are.you.1'] = 'world'
        self.assertEqual(len(context['hello.how.are.you']), 2)

        context['python'] = 'yeah'
        self.assertEqual(context['python'], 'yeah')

    def test_delete(self):
        context = Context()
        context['hello.how.are.you.0'] = 'world'
        del context['hello.how.are.you.0']
        self.assertEqual(len(context['hello.how.are.you']), 0)


if __name__ == "__main__":
    unittest.main()
