import streamlit as st
from streamlit_inspect import functions as stf
from streamlit_inspect.classes import StParam
import typing

import kornia as k
import torch
from inspect import getmembers, isfunction,ismodule,isclass
# from torchvision.io import decode_image, read_image
from torchvision.transforms import functional as F
from inspect import signature
from PIL import Image
import typing_inspect as tp


class StTensorKornia(StParam):
    def __init__(self,image):
        super().__init__()
        self.image=image
        
    def render(self,meta=None):
        super().render()
#         cols=st.beta_columns([7,1])
        if meta=="OR":  
           return None 
        else: # Assuming if torch.Tensor and is not Union type it is an image
            if meta:
                st.write(meta)
            input_=F.pil_to_tensor(self.image).float()/255
            input_=torch.stack(1*[input_])
            return input_
        return None    

uploaded_file = st.sidebar.file_uploader("Upload Image/s", type=['png','jpg','jpeg'] ,accept_multiple_files=False)
  

if not uploaded_file:
    angry_bird=Image.open("./Red_Legged_Kittiwake.jpg")
    image=angry_bird
else:
    image = Image.open(uploaded_file)    

st.sidebar.write("Input image")    
st.sidebar.image(image)
    
    
# submodules=['augmentation','enhance','contrib','feature','filters','geometry','losses','utils']       
# submodule=st.sidebar.selectbox("Select a module:", submodules)
# if submodule:
#     sm = getattr(K, submodule)
#     is_functional=any([x[0]=='functional' for x in getmembers(sm,ismodule)])
#     if is_functional:
#         sm=getattr(sm, 'functional')
#     functions_list = [o[0] for o in getmembers(sm,isfunction)]
    
    
with open("./supported_functional.txt") as f:
    functions_list=f.readlines()
    functions_list=[a.split("#")[0].strip() for a in functions_list if not a.startswith("#")]

    #use batch view for randoms 
    random_functions_list=[a for a in functions_list if a.startswith("random")]
    loss_functions_list=[a for a in functions_list if "loss" in a]
    functions_list=list((set(functions_list)-set(random_functions_list))-set(loss_functions_list))
    functions_list.sort()


selected_function=st.sidebar.selectbox("Select a function:", functions_list)
if selected_function:
    selected_function=getattr(k, selected_function)

    st.write(f"# {selected_function.__module__}.{selected_function.__qualname__}")
    simple_signature=stf.render_signature(selected_function)
    st.markdown(f"Signature: ```{simple_signature}```")

    required_container = st.beta_container()
    optional_params = st.beta_expander("Optional Parameters", expanded=True)
    optional_container = optional_params.beta_container()
    custom_types={"Tensor":StTensorKornia(image=image)}
    functionView=stf.StFunctionView(selected_function,custom_types,optional_container,required_container)
    applied_params=functionView.get_function_params()
#         st.write(ret.args)
#         st.write(ret.kwargs)
    result=functionView.call_func(applied_params)
#         st.write(applied_params)
#         st.write(result)
    cols=st.beta_columns(2)

    cols[0].image(image)
    if result is not None:
        try:#try as image
            if isinstance(result,list):
                for r in result:
                    cols[1].image(F.to_pil_image(r[0]))
            else:
                cols[1].image(F.to_pil_image(result[0]))
        except Exception as e:
            st.write(e)
            st.write(result)

    

# inspect.getdoc(fn)
# inspect.getsource(fn)
    


    


