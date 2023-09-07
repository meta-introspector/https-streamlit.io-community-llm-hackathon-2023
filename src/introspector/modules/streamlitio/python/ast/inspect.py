import streamlit as st
import ast
import pandas as pd
def myprint(x):
    st.write(x)
    
type_names   = {
    ast.AST : "ast",
    list : "list",
    str : "str",
    int : "int",
}
    
def get_name_of_type(node):
    # lookups up a type name
    for t in type_names :
        if isinstance(node, t):
            return type_names[t]
    return None

def visit_field_abstract(parent, pos, name, node, depth, match):
    indent = "  " * depth
    #myprint(f"{indent}Type: {type(parent).__name__} field={pos}  name={name} node={node} match={match}")
    return dict(parent=parent,
                id_parent = id(parent),
                pos       = pos,
                name      = name,
                id_node   = id(node),
                nodestr   = str(node),
                node_type = str(type(node)),
                depth     = depth,
                match     = match
                )
    
def visit_field_template(parent, pos, name, node, depth):
    # switch on type of node and dispatch
    #select the function based on type of node
    maybe_name = get_name_of_type(node)
    return visit_field_abstract(parent, pos, name, node, depth, maybe_name)
    
def visit_ast(node, depth=0):
    # visit fields
    position = 0
    frame = []
    for field_name, field_value in ast.iter_fields(node):
        position = position + 1
        data = visit_field_template(node, position, field_name, field_value, depth)
        frame.append(data)
    df = pd.DataFrame(frame)
    st.dataframe(df)
    
    #now group by parent
    st.dataframe(df.groupby(["id_parent"]))
    return frame
expression = st.text_area("Enter an expression:")

# Interpret and display the result when the user clicks a button
if st.button("Interpret"):
    tree = ast.parse(expression)
    result =   visit_ast(tree)
    st.write("Interpreted Result:", result)
