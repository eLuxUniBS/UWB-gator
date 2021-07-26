from srv.pubs.cmd_simulation import transform_coordinates_into_message
list_node = [

]
dict_node = {single["id"]: transform_coordinates_into_message(
    **single) for single in list_node}


def echo(*args, input_message: dict = None, **kwargs):
    global dict_node
    dict_node[input_message.get("id")] = transform_coordinates_into_message(
        **input_message)
    print("DICT NODE @ ", input_message.get("id"),
          " IS ", dict_node[input_message.get("id")])
    return None, [dict_node[x] for x in dict_node.keys()]
