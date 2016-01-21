vcontext
========

`vcontext` package provides single object `Context`. 
Context is dictionary like datastructure with custom access to items.
You can access your data by dot access. 
Context does not wrap data in itself, rather just access them. Context has `data` attribute where data is stored.

`__getitem__` vs `__getattribute__`
-------------------------------

For vcontext I have decided to use `__getitem__` approach, since I wanted to have consistent dot access also to lists/tuples.
This would be impossible using `__getattr__`.


Example:
--------
    
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

You can access data like this:
    
    assert context['result.0.user.username'] == 'phonkee'
    assert context['status'] == 200
    
If the data is not found, KeyError is raised on part of item that was not found. Context provides `get` method where 
you can specify default value if value is not found.

Item can have multiple parts. Rules are following:
* string - access to dictionary item or object attribute
* integer - access to list item
* first part must be string (since Context is a dictionary)

Context can also be used to build complicated datastructures with ease.
Lets build a structure from previous example:
    
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

Build items:
------------

Context would be useless if it only supported get of values. Context has support also to create/delete values on 
underlying datas by given `item`. Example:

    context = Context()
    context['result.0'] = 'phonkee'

    del context['result.0']
    assert len(context['result']) == 0

Isn't that cute little helper?

keys:
-----

Context also supports `keys` method. By calling this method context traverses recursively object. It has support for
dict/list, for custom object it returns just the object key.

    context = Context()
    context['hello.world'] = 'yay'
    assert context.keys() == ['hello.world']

Contribute:
-----------

Contributions are welcome, there are still a lot of parts to be enhanced.

TODO:
-----
* add support for special list key __append__ so we can append to list. e.g. `context['result.usernames.__append__'] = 'phonkee'` 

Author
------

Peter Vrba (phonkee)
