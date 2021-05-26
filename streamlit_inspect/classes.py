import streamlit as st

class StParam():
    
    def __init__(self,*args,**kwargs):
        pass
        
    def init_param(self,param_name,param_type,default=None,input_range=None):
        self.param_name=param_name
        self.param_type=param_type
        self.default=default
        self.input_range=input_range 
        # Iwant to support ranges not sure how, parse docstring?
        
    def render(self,meta=None):
        self.label=f"{self.param_name} ( {self.param_type} {', optional ' if self.default else ''}){f' Default:{self.default}' if self.default else ''}"
        
class StString(StParam):

    def render(self,meta=None):
        super().render(meta)
        if meta:
            st.write(meta)
        cols=st.beta_columns([7,1])
        val = cols[0].text_input(self.label, value=self.default if self.default else "")
        none = cols[1].checkbox('None',key=self.param_name)
        if none:
            val=None
        return val
        
class StInt(StParam):
    def render(self,meta=None):
        super().render(meta)
        if meta:
            st.write(meta)
        cols=st.beta_columns([7,1])
        val = cols[0].number_input(self.label, value=0 if not self.default else self.default)
        none = cols[1].checkbox('None',key=self.param_name)
        if none:
            val=None
        return val
    
class StFloat(StParam):
    def render(self,meta=None):
        super().render(meta)
        if meta:
            st.write(meta)
        cols=st.beta_columns([7,1])
        val = cols[0].number_input(self.label, value=0. if not self.default else self.default, step=0.1)
        none = cols[1].checkbox('None',key=self.param_name)
        if none:
            val=None
        return val
    
class StBool(StParam):

    def render(self,meta=None):
        super().render(meta)
        if meta:
            st.write(meta)
        cols=st.beta_columns([7,1])
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        val = cols[0].radio(self.label, [None,True,False], index=0 if self.default is None else self.default)
        return val
    
class StEmpty(StParam):
    def render(self,meta=None):
        super().render(meta)
        if meta:
            st.write(meta)
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