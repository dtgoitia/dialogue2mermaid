def pretty_var(token: any) -> any:
    if type(token) is dict:
        return token.get('var')
    return token


def beautified_decision_node(node: dict) -> str:
    decision = node['rule']
    rule = list(decision.keys())[0]
    left = pretty_var(decision[rule][0])
    right = pretty_var(decision[rule][1])
    return f"{str(left)} {rule} {str(right)}"


def beautified_operation_node(node: dict) -> str:
    operation = node['operation']

    # running methods
    if 'method' in operation:
        method = operation['method']
        method_name = method[1]

        if method_name in ('addItem', 'getItem', 'updateItem'):
            src = method[0]['var']
            i = method[2][0]
            i = i.get('var') if type(i) == dict else i
            return f"{src}.{method_name}({i})"
        return str(operation['unrecognised method'])

    # defining a variable
    elif 'var' in operation:
        return f"{node['output']} = {operation['var']}"

    # default
    return ''


def beautify_nodes(nodes: list) -> list:
    """
    Customize each node content and return all nodes.
    Return each node data as a dictionary.
    """
    for node in nodes:
        node_type = node.get('type')
        if node_type == 'message':
            node.update({'content': 'print'})
        elif node_type == 'operation':
            node.update({'content': beautified_operation_node(node)})
        elif node_type == 'action':
            node.update({'content': 'action'})
        elif node_type == 'decision':
            node.update({'content': beautified_decision_node(node)})
        elif node_type == 'card':
            node.update({'content': 'card'})
        elif node_type == 'customCardCollection':
            node.update({'content': 'customCardCollection'})
        else:
            node.update({'content': 'NOT UNDERSTOOD'})
    return nodes
