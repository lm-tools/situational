from django.template import Library, Node, resolve_variable

register = Library()

"""
A modified version of https://djangosnippets.org/snippets/2428/
"""


class AddGetParameter(Node):
    def __init__(self, values):
        self.values = values

    def render(self, context):
        req = resolve_variable('request', context)
        params = req.GET.copy()
        for key, value in self.values.items():
            value = value.resolve(context)
            key = key.resolve(context)
            if key.endswith('[]'):
                value_list = params.getlist(key)
                value_list.append(value)
                params[key] = ",".join(set(value_list))
            else:
                params[key] = value
        return '?%s' % params.urlencode(True)


@register.tag
def add_get(parser, token):
    pairs = token.split_contents()[1:]
    values = {}
    for pair in pairs:
        s = pair.split('=', 1)
        values[parser.compile_filter(s[0])] = parser.compile_filter(s[1])
    return AddGetParameter(values)
