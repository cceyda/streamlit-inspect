import streamlit as st

class StParam():
    
    def __init__(self,*args,**kwargs):
        pass
        
    def init_param(self,container,param_name,param_type,param_index,default=None,input_range=None): 
        self.container=container
        self.param_name=param_name
        self.param_type=param_type
        self.param_index=param_index
        self.default=default
        self.input_range=input_range 
        # Iwant to support ranges not sure how, parse docstring?
        
    def render(self,meta=None):
        # st.write(self.param_index)
        self.label=f"{self.param_name} ( {self.param_type} {', optional ' if self.default else ''}){f' Default:{self.default}' if self.default else ''}"
        if meta:
            # with self.container:
            st.write(meta)
        
class StString(StParam):

    def render(self,meta=None):
        super().render(meta)
        # cols=st.beta_columns([7,1])
        with self.container:
            val = st.text_input(self.label, value=self.default if self.default else "")
            none = st.checkbox('None',key=self.param_name)
        if none:
            val=None
        return val
        
class StInt(StParam):
    def render(self,meta=None):
        super().render(meta)
        # cols=st.beta_columns([7,1])
        with self.container:
            val = st.number_input(self.label, value=0 if not self.default else self.default)
            none = st.checkbox('None',key=self.param_name)
        if none:
            val=None
        return val
    
class StFloat(StParam):
    def render(self,meta=None):
        super().render(meta)
        # cols=st.beta_columns([7,1])
        with self.container:
            val = st.number_input(self.label, value=0. if not self.default else self.default, step=0.1)
            none = st.checkbox('None',key=self.param_name)
        if none:
            val=None
        return val
    
class StBool(StParam):

    def render(self,meta=None):
        super().render(meta)
        # cols=st.beta_columns([7,1])
        with self.container:
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            val = st.radio(self.label, [None,True,False], index=0 if self.default is None else self.default)
        return val
    
class StEmpty(StParam):
    def render(self,meta=None):
        super().render(meta)
#         cols=st.beta_columns([7,1])
        if self.param_name == "self":
            st.write("This is a class method (self,)")
        elif self.param_name == "args":
            st.write("No support for passing args yet")
            st.stop()
        elif self.param_name == "kwargs":
            st.write("No support for passing kwargs yet")
            st.stop()
        return None  
    
    
######
def custom_type():
    st.write("This is a custom type")
    return 0