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
        self.none=None
        self.val=None
        # I want to support ranges not sure how, parse docstring?
        
    def render(self,meta=None):
        # st.write(self.param_index)
        self.label=f"{self.param_name} ( {self.param_type} {', optional ' if self.default else ''}){f' Default:{self.default}' if self.default else ''}"
        # do something smarter here for alignment?
        if meta:
            with self.container[2*self.param_index]:
                st.write(meta)
        with self.container[2*self.param_index+1]:
            self._render(meta)
        # Move None here?
        self.assign()

    def _render(self,meta=None):
        #Custom types may want to do their own thing with meta_data and None
        pass

    def assign(self):
        if self.none:
            self.val=None
        return self.val
        
class StString(StParam):

    def _render(self,meta=None):
        self.val = st.text_input(self.label, value=self.default if self.default else "")
        self.none = st.checkbox('None',key=self.param_name)
        
        
class StInt(StParam):
    def _render(self,meta=None):
        self.val = st.number_input(self.label, value=0 if not self.default else self.default)
        self.none = st.checkbox('None',key=self.param_name)
    
class StFloat(StParam):
    def _render(self,meta=None):
        self.val = st.number_input(self.label, value=0. if not self.default else self.default, step=0.1)
        self.none = st.checkbox('None',key=self.param_name)

    
class StBool(StParam):
    def _render(self,meta=None):
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        self.val = st.radio(self.label, [None,True,False], index=0 if self.default is None else self.default)

    
class StEmpty(StParam):
    def _render(self,meta=None):
        if self.param_name == "self":
            st.write("This is a class method (self,)")
        elif self.param_name == "args":
            st.write("No support for passing args yet")
            st.stop()
        elif self.param_name == "kwargs":
            st.write("No support for passing kwargs yet")
            st.stop()
        return None  