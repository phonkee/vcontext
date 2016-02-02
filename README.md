# Context

`vcontext` package provides single object `Context`. 
Context is dictionary like datastructure with custom access to items.
You can access your data by dot access. 
Context does not wrap data in itself, rather just access them. Context has `data` attribute where data is stored.

## Install
vcontext is on [pypi](https://pypi.python.org/pypi/vcontext) so you can simply:

`pip install vcontext`


##### `__getitem__` vs `__getattribute__`

For `Context` I have decided to use `__getitem__` approach, since I wanted to have consistent dot access also to lists/tuples.
This would be impossible using `__getattr__`.

#### Item

Item is dot-separated path to value. This item is splitted and values have following rules
* string - access to dictionary item or object attribute
* integer - access to list item
* first part must be string (since Context is a dictionary)

###### Example:

```python
context = Context({
    'status': 200,
    'message': 'OK',
    'result': [
        {
            'user': {
                'username': 'phonkee',
                'name': 'Peter Vrba'
            }
        }
    ]
})
assert context['result.0.user.username'] == 'phonkee'
assert context['status'] == 200
```

If the data is not found, `KeyError` is raised on part of item that was not found. Context provides `get` method where 
you can specify default value if value is not found and that will never raise exception.

## Build items:

Context would be useless if it only supported get of values. Context has support also to create/delete values on 
underlying datas by given `item`. 
Lets build a structure from previous example:

```python
context = Context()
context['status'] = 200
context['message'] = 'OK'
context['result.0.user.username'] = 'phonkee'
context['result.0.user.name'] = 'Peter Vrba'

assert context.data == {
    'status': 200,
    'message': 'OK',
    'result': [
        {
            'user': {
                'username': 'phonkee',
                'name': 'Peter Vrba'
            }
        }
    ]
}
```

Now we try to delete item

```python
del context['result.0']
assert len(context['result']) == 0
```

Isn't that cute little helper?

## .keys(item=None):

Context also supports `keys` method. By calling this method context traverses recursively object. It has support for
dict/list, for custom object it returns just the object key.

```python
context = Context()
context['hello.world'] = 'yay'
assert context.keys() == ['hello.world']
```

## api:
Context provides following methods:

* `.copy()` - deepcopies data and returns new context
* `.dumps(item=None)` - dump to json, attributes:
    * item - item to be dumped to json
* `.items(**kwargs)` - list of key value items (tuple key, value), **kwargs passed to `keys` method
* `.iteritems(**kwargs)` - generator version of items, **kwargs passed to `keys` method
* `keys(item=None)` - returns list of all keys, attributes:
    * item - item to be dumped to json


## Contribute:

Contributions are welcome, there are still a lot of parts to be enhanced.

## TODO:

* add support for special list key __append__ so we can append to list. e.g: 
```python
context['result.usernames.__append__'] = 'phonkee'
```

## Author

Peter Vrba (phonkee)
