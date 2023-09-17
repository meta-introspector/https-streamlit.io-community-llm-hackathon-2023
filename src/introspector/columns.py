import streamlit as st

(col1,col_concept,col_workflow,col2) = st.columns(4)

# with col1:
#     #aapp_args["mode"] = st.text_input("Mode", help="Mode to use", key="mode",value=params.get("mode","concept-inputs"))
#     app_args["app_id"] = st.text_input("app_id", help="id" , value ="Introspector-LLama2-Hackathon-Demo1")
#     app_args["input_id"] = st.text_ainput(

# with col_4:    
#     page_size = st.number_input("Page Size", min_value=1,key="page_size",
#                                 help="Use a number input widget to allow users to specify the page size. This will control how many items are displayed per page",
#                                 value=int(params.get("page_size", "3")))

# with col_workflows:
#     app_args["workflow"] = st.text_input(
#         "Workflow",
#         value=params.get(
#             "workflow",
#             "RakeItUpV3Critical_Reconstruction_of4"),
#         key="workflow"
#     )

