import streamlit as st
from streamlit_inspect import functions as stf
import typing

import tests.test_class as t

modules_list = stf.get_modules(t)

module = st.sidebar.selectbox("Select module:", modules_list)

if not module:
    module = t
else:
    module = getattr(t, module)

class_list = stf.get_classes(module)

class_ = st.sidebar.selectbox("Select class:", class_list)

if not class_:
    class_ = t
else:
    class_ = getattr(module, class_)

functions = stf.get_functions(class_)


selected_function = st.sidebar.selectbox("Select a function:", functions)
if selected_function:
    selected_function = getattr(class_, selected_function)

    st.write(f"# {selected_function.__module__}.{selected_function.__qualname__}")
    # simple_signature = stf.render_signature(selected_function)
    # st.markdown(f"Signature: ```{simple_signature}```")
    st.help(selected_function)
    

    required_container = st.beta_container()
    optional_params = st.beta_expander("Optional", expanded=True)
    optional_container = optional_params.beta_container()

    #     typing.get_type_hints(selected_function)
    functionView = stf.StFunctionView(
        selected_function, None, optional_container, required_container
    )
    ret = functionView.get_function_params()
    st.write("Inputs:",ret)
    st.write("args:",ret.args)
    st.write("kwargs:",ret.kwargs)
    result=functionView.call_func(ret)
    st.write("result:",result)


# inspect.getdoc(fn)
# inspect.getsource(fn)
