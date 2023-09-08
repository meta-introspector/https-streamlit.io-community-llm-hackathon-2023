# To create a basic Streamlit app for viewing and editing Org Mode files, you can build upon the Python script I provided earlier. Here's a simple Streamlit version:

# ```python
import streamlit as st

def read_org_file(file_path):
    with open(file_path, 'r') as file:
        lines =[]
        for line in file:
            lines.append( line)
    return lines

def write_org_file(file_path, org_content):
    with open(file_path, 'w') as file:
        file.write(org_content)

def list_tree(org_structure) :
    #org_structure = [...]  # Replace with your Org Mode structure

    # Convert Org Mode structure to JSON (optional)
    org_json = json.dumps(org_structure)
    
    # Create a Streamlit tree view
    st.title("Org Mode Outline Viewer")
    st.sidebar.text("Outline Structure")
    
    # Display the Org Mode outline as a tree
    selected_node = st.sidebar.tree(data=org_json, key="org_tree")

    # Show details of the selected node (optional)
    if selected_node:
        st.write(f"Selected Node: {selected_node}")

def list_outline(org_structure):
    # Load the Org Mode structure (replace with your own method to load data)
    #org_structure = [...]  # Replace with your Org Mode structure

    # Create a Streamlit list view
    st.title("Org Mode Outline Viewer")
    st.sidebar.text("Outline Structure")

    # Display the Org Mode outline as a list
    def display_outline(node, indent=0):
        for item in node:
            title = item.get("title", "")
            st.write(" " * indent + title)
            children = item.get("children", [])
            display_outline(children, indent + 2)


def parse_org_file(lines):
    outline = []
    current_node = None

    for line in lines:
        if line.startswith("*"):
            st.write(f"debug: {line}")
            level = line.count("*")
            title = line.strip("*").strip()
            node = {"level": level, "title": title, "children": []}
            if not current_node:
                outline.append(node)
            else:
                while level <= current_node["level"]:
                    current_node = current_node.get("parent")
                current_node["children"].append(node)
                node["parent"] = current_node
            current_node = node

    return outline

def main():
    st.title("Org Mode Viewer and Editor")
    file_path = "Hackathon.org"  # Replace with the path to your Org Mode file

    org_content = read_org_file(file_path)
    org_structure = parse_org_file(org_content)
    for x in org_content:
        st.text_area("Org Mode Content", x)
    st.text_area("Org Mode Str", str(org_structure))

    choice = st.radio("Select an option:", ("View", "Edit"))

    #if choice == 'Edit':
    #    edited_content = st.text_area("Edit Org Mode Content")
    #    write_org_file(file_path, edited_content)
    #    st.success("Content saved successfully!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.write("ERR" + str(e))
    
