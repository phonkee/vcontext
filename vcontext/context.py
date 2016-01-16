"""
Context

context is a proxy datastructure that provides advanced  dict-like access to underlying data with dotted notation.
See README.md
"""
import copy
import json


class Context(object):
    """
    Context object

    context is dict-like structure that has custom get/set/del item.
    """

    data = None
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
        parsed = self.parse(item)
        if not parsed:
            raise KeyError('no key provided')

        actual = self.data

        for i, part in enumerate(parsed):

            last = i == len(parsed) - 1

            try:
                if last:
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
        parsed = self.parse(item)
        if not parsed:
            raise KeyError('no key provided')

        actual = self.data
        for i, part in enumerate(parsed):

            try:
                actual = actual[part]
            except (KeyError, IndexError):
                raise KeyError(".".join([str(x) for x in parsed[:i+1]]))

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
        parsed = self.parse(str(item))

        if not parsed:
            raise NameError("Item name not given")

        # copy to new list
        parts = parsed[:]

        item = self._build_item(self.data, parts, value=value)

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
                result = self._build_item(prepare_list([], n), parts, value=value)
            else:
                result = self._build_item(self.dict_(), parts, value=value)
            return result

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
            # @TODO: object handling getattr/setattr
            print "this is object", part, object

        return object

    def build_part(self, part, value=None):
        if isinstance(part, (int, long)):
            result = [None for _ in range(part + 1)]
            return result

        return self.dict_()

    def dumps(self, item=None, **kwargs):
        """
        Dumps returns json string for given item. If no item is given whole dict is returned
        :param item: item name such as 'result.0.user'
        :param kwargs: additional kwargs passed to json.dumps
        :return: json string
        """
        target = self.data
        if item:
            target = self[item]

        return json.dumps(target, **kwargs)

    def clone(self):
        """
        Clone clones context to new one (performs deep copy)
        :return:
        """
        return Context(copy.deepcopy(self.data), dict_=self.dict_)

    def value(self, item=None):
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
    def parse(cls, item):
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


if __name__ == "__main__":
    ctx = Context({
        'hello': {
            'hitty': 'kitty',
            'users': ["techno"],
        },
    })
    ctx['hello.users.5.user.username'] = 'phonkee'
    ctx['hello.users.5.user.name'] = 'Peter Vrba'
    ctx['hello.users.5.user.github'] = 'phonkee'
    ctx['hello.users.5.user.email.0'] = 'phonkee@phonkee.eu'
    ctx['hello.list.0.1.2.3.4.5'] = 'yeah we support deep structures'

    print ctx.dumps(indent=4)

    # ctx['result.users.5.user.name'] = 'Peter'
    # # ctx['result.users.88.user.username'] = 'phonkee'
    # print ctx.dumps()
