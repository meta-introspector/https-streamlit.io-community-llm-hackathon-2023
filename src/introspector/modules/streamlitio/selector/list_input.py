import streamlit as st

def list_input(title, choices, key, default_value):
    opt_index = 0
    if default_value in choices:
        opt_index = choices.index(default_value)

    selected_choice = st.selectbox(
        title,
        choices,
        key=key,
        index=opt_index,
    )

    return selected_choice
```

Now, you can use this `list_input` function to create list-based inputs. Here's how you can use it for your `get_concept` function:

```python
