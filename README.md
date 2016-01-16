vcontext
========

Context is dictionary datastructure with custom access to items.
You can access your data by dot access. 
Context does not wrap data in itself, rather just access them. Context has `data` attribute where data is stored.

Let show an example:
    
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
* first part must be string (since Context is a dictionary

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

Contribute
----------

Contributions are welcome, there are still a lot of parts to be enhanced.

Author
------

Peter Vrba (phonkee)
