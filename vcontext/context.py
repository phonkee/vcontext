"""
Context

context is a proxy datastructure that provides advanced  dict-like access to underlying data with dotted notation.
See README.md
"""
import copy
import json

import itertools


class Context(object):
    """
    Context object

    context is dict-like structure that has custom get/set/del item.
    """

    data = None

    # custom dict functionality currently isn't supported
    dict_ = dict

    def __init__(self, *args, **kwargs):
        self.dict_ = kwargs.pop('dict_', self.dict_)
        self.data = self.dict_()
        for d in args:
            self.data.update(d)
        self.data.update(kwargs)

    def __delitem__(self, item):
        """
        Delete item by dotted key
        :param item:
        :return:
        """
        parsed = self._parse_item(item)
        if not parsed:
            raise KeyError('no key provided')

        actual = self.data

        for i, part in enumerate(parsed):

            is_last = i == len(parsed) - 1

            try:
                if is_last:
                    del actual[part]
                    return
                actual = actual[part]

            except (KeyError, IndexError):
                raise KeyError(".".join([str(x) for x in parsed[:i+1]]))

    def __getitem__(self, item):
        """
        Return item
        :param item: dotted syntax
        :return:
        """
        parsed = self._parse_item(item)
        if not parsed:
            raise KeyError('no key provided')

        actual = self.data
        for i, part in enumerate(parsed):
            try:
                actual = actual[part]
            except TypeError:
                actual = getattr(actual, part)
            except (KeyError, IndexError):
                raise KeyError(".".join([str(x) for x in parsed[:i+1]]))

            while callable(actual):
                actual = actual()

        return actual

    def __setitem__(self, item, value):
        """
        setitem is more complicated one, because it needs to update values if exists, if not create appropriate one.
        Steps:
            * split item to parts
            * start with self.data
        :param item:
        :param value:
        :return:
        """

        # get parsed parts of item
        parsed = self._parse_item(str(item))

        if not parsed:
            raise NameError("Item name not given")

        # copy to new list
        parts = parsed[:]
        self._build_item(self.data, parts, value=value)

    def _build_item(self, object, parts, value=None):
        """
        Get item
        :param object:
        :param parts:
        :return:
        """
        if not parts:
            return value

        part = parts.pop(0)

        try:
            next_part = parts[0]
        except IndexError:
            next_part = None

        def prepare_list(l, index):
            """
            Prepare list updates length of list (inplace and also returns)
            :param l: list
            :param index: index to be used
            :return: list
            """
            if len(l) < index + 1:
                for i in range(index + 1):
                    try:
                        l[i]
                    except:
                        l.append(None)
            return l

        def prepare_next(n):
            """
            Prepare nex value by part
            :param n: part
            :return:
            """
            if isinstance(n, (int, long)):
                new_item = prepare_list([], n)
            else:
                new_item = self.dict_()
            return self._build_item(new_item, parts, value=value)

        if isinstance(object, list):
            # Handling list
            try:
                result = object[part]
                if result is None:
                    # look at next part
                    result = prepare_next(next_part)
                else:
                    object[part] = self._build_item(result, parts, value=value)
            except IndexError:
                prepare_list(object, part)

                # look at next part
                result = prepare_next(next_part)

            object[part] = result

        elif isinstance(object, dict):
            try:
                result = object[part]

                # check list length!!
                if isinstance(next_part, (int, long)):
                    prepare_list(result, next_part)
                else:
                    # check item in dictionary
                    if not isinstance(result, dict):
                        result = self.dict_()

                object[part] = self._build_item(result, parts, value=value)
            except KeyError:
                object[part] = prepare_next(next_part)

        else:
            raise NotImplementedError('settings of object not supported currently')

        return object

    def dumps(self, item=None, **kwargs):
        """
        Dumps returns json string for given item. If no item is given whole dict is returned
        :param item: item name such as 'result.0.user'
        :param kwargs: additional kwargs passed to json.dumps
        :return: json string
        """
        target = self.data
        if item:
            target = self.get(item, default=None)

        return json.dumps(target, **kwargs)

    def copy(self):
        """
        Copy performs deep copy of underlying data and returns context with this data
        :return:
        """
        return Context(copy.deepcopy(self.data), dict_=self.dict_)

    def get(self, item, default=None):
        """
        If not found return/set default value
        :param item: dotted syntax item
        :param default: default value
        :return:
        """

        try:
            return self[item]
        except KeyError:
            self[item] = default

        return default

    def copy_value(self, item=None):
        """
        value deep copies just value and returns. If not found raise error
        :param item:
        :return:
        """
        if item is None:
            obj = self.data
        else:
            obj = self[item]
        return copy.deepcopy(obj)

    @classmethod
    def _parse_item(cls, item):
        """
        PArse item into parts. Currently we use just split with some type conversions.
        :param item:
        :return: list of parts
        """
        result = []

        for part in item.split('.'):
            try:
                result.append(int(part))
            except:
                result.append(part)

        return result

    def keys(self, item=None, strip=False):
        """
        Return all stored keys in sorted order.
        :param item: item to start with ([] is used)
        :param strip: if item is given whether to strip item from keys
        :return:
        """

        result = []
        if item is not None:
            current, prepend = self[item], True

            # if item is not dict/list/tuple we just return key (found key)
            if not isinstance(current, (list, tuple, dict)):
                return [item] if not strip else ['']
        else:
            current, prepend = self.data, False

        result = sorted(self._list_keys(current))

        # prepend item to list or not?
        if prepend and not strip:
            """
            item was given so we should prepend key names with item
            """
            for i, value in enumerate(result):
                result[i] = '.'.join((item, value))

        return result

    def _list_keys(self, object):
        """
        Recursively lists keys
        :param object: object to be
        :return:
        """

        result = []

        if isinstance(object, (dict, list, tuple)):
            if isinstance(object, dict):
                iterable = object.iteritems()
            else:
                iterable = enumerate(object)
            for k, v in iterable:
                if isinstance(v, (list, tuple, dict)):
                    result += ["{}.{}".format(k, key) for key in self._list_keys(v)]
                else:
                    result.append(k)

        return result

    def items(self, **kwargs):
        """
        Return key/value items (tuple)
        **kwargs are passed directly to keys method.
        :return:
        """

        return list(self.iteritems(**kwargs))

    def iteritems(self, **kwargs):
        """
        Return key/value items (tuple)
        **kwargs are passed directly to keys method.
        :return:
        """

        for key in self.keys(**kwargs):
            yield (key, self[key])

        raise StopIteration

    def __contains__(self, key):
        """
        Support for "in"
        :param key:
        :return:
        """
        try:
            self[str(key)]
        except KeyError:
            return False
        return True

    def expand(self):
        """
        expand

        This method adds functionality to expand data. Expansion is applied on all levels deep structures built with
        dict/list/tuple. Expand supports top level just dict (since vcontext nature), but that's not a limitation since
        you can have nested lists/dicts.
        Expand makes cartesian product of all expanded values on all levels deep!

        If a value is a dict and has one of followint keys provided it is a subject to expansion:
        * __range__ - value will chosen from defined range, arguments are directly passed to pythons `range`.
        * __choices__ - value will be chosen from given list

        If there is `__format__` key in this dictionary, it's used as format string. Expander uses `format` method on string and
        passes the value as `value` key. Otherwise raw value will be returned.

        Example of valid `__format__`:

            '__format__': 'count_me_in_{value}'

        Example:

            data = {
                'range_value': {
                    '__range__': [2],
                    '__format__': 'ranged_%s',
                    '__exclude__': [0],
                },
                'choice_value': {
                    '__choices__': ['a', 'b'],
                    '__format__': 'value_{value}'
                },
            }
            expanded = list(expand(data)
            assert len(expanded) == 1

            assert expanded == [{
                'range_value': 'ranged_1',
                'choice_value': 'a'
            }
            {
                "range_value": 'ranged_1',
                'choice_value': 'b'
            }]
        :return: generator of items
        """

        choices = []
        ranges = []
        other = []

        # find expandable variables, currently detected by __choices__, __range__ keys.
        for key in self.keys():
            splitted = key.split('.__choices__.')
            if len(splitted) > 1 and splitted[0] not in choices:
                choices.append(splitted[0])
                continue
            splitted = key.split('.__range__.')
            if len(splitted) > 1 and splitted[0] not in ranges:
                ranges.append(splitted[0])
                continue

            if '.__format__' not in key:
                other.append(key)

        # prepare keys(choices, ranges) and list of expanded values to pass to cartesian product later in the code
        keys = []
        values = []

        # get values for choices and ranges
        for item in itertools.chain(choices, ranges):
            formatter = self.get('{}.__format__'.format(item), None)
            keys.append(item)

            # all available values for expanded value.
            tmp_values = []

            # get iterator for either choice or range, otherwise KeyError is raised.
            try:
                iterator = self['{}.__choices__'.format(item)]
            except KeyError:
                try:
                    iterator = range(*self['{}.__range__'.format(item)])
                except KeyError:
                    raise KeyError('Key not found: {}'.format(item))

            # excluded values
            try:
                excluded = self['{}.__exclude__'.format(item)]
            except KeyError:
                excluded = []

            # iterate over changes and prepare values
            for value in iterator:

                # check if value is not excluded
                if value in excluded:
                    continue

                if formatter is not None:
                    value = str(formatter).format(value=value)

                # check if value is not excluded
                if value in excluded:
                    continue

                tmp_values.append(value)

            # add list of values for given key
            values.append(tmp_values)

        # make all combinations (itertools.product) - cartesian product
        for combination in list(itertools.product(*values)):
            # prepare new context
            new = self.copy()

            # add current combination data to new context
            for i, v in enumerate(combination):
                new[keys[i]] = v
            yield new.data


if __name__ == "__main__":

    class Test(object):
        something = 'else'
        data = {
            'mamma': 'mia'
        }

    ctx = Context({
        'hello': {
            'hitty': 'kitty',
            'users': ["techno"],
            'test': Test(),
        },
    })
    ctx['hello.users.5.user.username'] = 'phonkee'
    ctx['hello.users.5.user.github'] = 'phonkee'
    ctx['hello.users.5.user.email.0'] = 'test@example.com'
    ctx['hello.list.0'] = 'yeah we support deep structures'

    ctx['hello.object'] = Test()
    # print ctx.dumps(indent=4)

    ctx['hello.test.data.mamma'] = 'hell'
    # print ctx.data
    # print ctx.keys()
    # ctx['result.users.5.user.name'] = 'Peter'
    # # ctx['result.users.88.user.username'] = 'phonkee'
    # print ctx.dumps()

    context = Context()
    context['hello.world'] = "yeah"
    context['hello.0.something.key'] = "yay"
    context['hello.1.something.key'] = "yay"

    print context, context.copy()
    print "Keys:", context.keys()
    print "Items:", context.items()
