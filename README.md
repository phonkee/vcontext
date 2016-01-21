vcontext
========

`vcontext` package provides single object `Context`. 
Context is dictionary like datastructure with custom access to items.
You can access your data by dot access. 
Context does not wrap data in itself, rather just access them. Context has `data` attribute where data is stored.

`__getitem__` vs `__getattribute__`
-------------------------------

For vcontext I have decided to use `__getitem__` approach, since I wanted to be consistend with access to array indices.
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
    
Key can have multiple parts. Rules are following:
* string - access to dictionary key or object attribute
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

Context has also support for delete so let's assume that we use context from previous example:

    del context['result.0']
    assert len(context['result']) == 0

Isn't that neat small helper for your next projects?

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
