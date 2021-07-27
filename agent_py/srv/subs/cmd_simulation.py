from agent_py.srv.pubs.cmd_simulation import transform_coordinates_into_message
list_node = [

]
dict_node = {single["id"]: transform_coordinates_into_message(
    **single) for single in list_node}


def echo(*args, input_message: dict = None, **kwargs):
    global dict_node
    if input_message is None:
        print("jump", dict_node)
        return None, [dict_node[x] for x in dict_node.keys()]
    print("ARGS ECHO", args)
    print("KWARGS ECHO", kwargs, "\nINPUTNODE", input_message)
    # Se il dato arriva strutturato in x,y,z allora lo pongo direttamente in input alla funzione transform, altrimenti, utilizzo il parametro allert_distance
    translate = True
    for single in ["x", "y", "z"]:
        if single in list(input_message.keys()):
            translate = False
    if translate and input_message.get("allert_distance", None) is not None:
        if input_message.get("id").find("->") != -1:
            #id = indirizzo tag -> indirizzo ancora == indirizzo mittente -> indirizzo ricevente
            dict_node[input_message.get("id").split("->")[-1].upper()] = transform_coordinates_into_message(
                x=input_message["allert_distance"], y=input_message["allert_distance"])
    else:
        dict_node[input_message.get("id")] = transform_coordinates_into_message(
            **input_message)
    print("DICT NODE @ ", input_message.get("id"),
          " IS ", dict_node[input_message.get("id")])
    return None, [dict_node[x] for x in dict_node.keys()]
