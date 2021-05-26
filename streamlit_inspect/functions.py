import typing_inspect as tp
from .classes import *
import streamlit as st
from inspect import signature
from inspect import getmembers, isfunction, ismodule, isclass, ismethod, isbuiltin
import inspect

from enum import Enum


#Native: bool,float,str,int
#typing: tuple,union
#special/custom: tensor
# enums?

# this code is ugly ㅠㅠ
# typing.get_type_hints does not work with *args,**kwargs
# Limit to functions defined in code only (difficult?)
# Don't import (use __import__)? https://pymotw.com/2/pyclbr/?

#Use sliders when there is a value range available?


def is_in(a,b, return_dunder=False, return_external=False):
    if a.__name__.startswith("_") and not return_dunder:
        return False
    if not return_external:
        if inspect.ismodule(b):
            return b.__name__ in a.__module__
        elif inspect.isclass(b):
            return b.__module__ == a.__module__
    return True

def get_type(inp,type_of,return_dunder=False,return_external=False):
    return [name for name,func in getmembers(inp,type_of) if is_in(func,inp,return_dunder=return_dunder,return_external=return_external)]

def get_functions(inp,return_dunder=False,return_external=False):
    return get_type(inp,isfunction,return_dunder=return_dunder,return_external=return_external)

def get_classes(inp,return_dunder=False,return_external=False):
    return get_type(inp,isclass,return_dunder=return_dunder,return_external=return_external)

def get_modules(inp,return_dunder=False,return_external=False):
    return get_type(inp,ismodule,return_dunder=return_dunder,return_external=return_external)

def has_default(a):
    if a == inspect._empty:
        return False
    else:
        return True

def is_typing(type_):
    return (tp.is_union_type(type_) or  tp.is_tuple_type(type_))

class StFunctionView():
    def __init__(self,fn,custom_types=None,optional_container=st,required_container=st):
        # custom_types={"type_name":class inheriting(StParam)}
        
        self.fn=fn
        self.signature=signature(fn)
        self.parameters=self.signature.parameters
        self.optional_container=optional_container
        self.required_container=required_container
        if custom_types is not None:
            self.custom_types=custom_types
        else:
            self.custom_types={}
        
    # POSITIONAL_ONLY
    # POSITIONAL_OR_KEYWORD
    # VAR_POSITIONAL
    # KEYWORD_ONLY
    # VAR_KEYWORD
    def get_function_params(self):

        new_params=[]
        for param_name,p in self.parameters.items(): #Each param is a row in streamlit
            if has_default(p.default):
                with self.optional_container:
                    value=self.param2st(p)
            else:
                with self.required_container:
                    value=self.param2st(p)
    #         st.write(value)
            p=p.replace(default=value) #Fake user inputs as defaults
    #         st.write(p)
            new_params.append(p)
        new_signature=self.signature.replace(parameters=new_params)
        bounds=new_signature.bind_partial()
        bounds.apply_defaults()
        return bounds

    def call_func(self,bounds):
        try:
            res=self.fn(*bounds.args, **bounds.kwargs)
            return res
        except TypeError as e:
            st.write(f"Something went wrong {e}")
            st.write(f"Try changing paramater values {e}")
            return None
    
    
    def param2st(self,param):
        param_name=param.name
        # typing doesn't have __name__ (Is basic type)
        if type(param.annotation).__name__ == 'type':
            param_type=param.annotation.__name__
            if has_default(param.default):
                default=param.default
            else:
                default=None
            return self.basic2st(param_name,param_type,default)
        else:
            param_type=type(param.annotation).__name__
            #Is union or tuple
            return self.typing2st(param_name,param_type,param)
        
        
    def typing2st(self,param_name,param_type,param):
        args=tp.get_last_args(param.annotation)
#         if has_default(param.default):
#             default=param.default
#         else:
#             default=[None]*len(args)
        return self._typing2st(param_name,param.annotation,args,param.default)

    def _typing2st(self,param_name,p_annotation,args,default,meta=None):
        if tp.is_tuple_type(p_annotation):
            if not has_default(default):
                default=[None]*len(args)
            tuple_values=[]
            with st.beta_container():
                for i,(type_,param_default) in enumerate(zip(args,default)):
                    if i!=0:
                        meta="AND"
                    p_name = f'{param_name} [{i}]'
                    param_type=type_.__name__
                    ret=self.basic2st(p_name,param_type,param_default,meta)
                    tuple_values.append(ret)
                return tuple(tuple_values)
        elif tp.is_union_type(p_annotation):
            with st.beta_container():
                return_value=None
#                 st.write(param_name)
#                 st.write(default)
                if not has_default(default):
                    default=None

                for i,type_ in enumerate(args):
                    if i!=0:
                        meta="OR"
                    p_name = f'{param_name} [{i}]'
                    if is_typing(type_):
                        nargs=tp.get_last_args(type_)
                        if not default:
                            default=[None]*len(nargs)
                        ret=self._typing2st(p_name,type_,nargs,default,meta) # Not supporting nested defaults?
                        
                    else:    
                        param_type=type_.__name__
                        ret=self.basic2st(p_name,param_type,default,meta)
                    if ret is not None and return_value is None:
                        return_value=ret
                return return_value

    def basic2st(self,param_name,param_type,default,meta=None):

        if param_type == "_empty":
            type_class = StEmpty()
        elif param_type == "str":
            type_class = StString()
        elif param_type == "bool":
            type_class = StBool()
        elif param_type == 'float':
            type_class = StFloat()
        elif param_type == 'int':
            type_class = StInt()
        elif param_type in self.custom_types.keys():
            type_class=self.custom_types[param_type]
        else:
            st.write(f"UNK input type: {param_type} for {param_name}")
            return None
        type_class.init_param(param_name,param_type,default=default)  
        return type_class.render(meta=meta)
        
def render_signature(fn):
    s=signature(fn)
    return _render_signature(s, fn.__name__)
    
    
#_render_signature code snippet stolen from https://github.com/ipython/ipython/blob/62eec6978a54f743039f857f4fddba62488d0bb4/IPython/core/oinspect.py#L991       
def _render_signature(obj_signature, obj_name) -> str:
    """
    This was mostly taken from inspect.Signature.__str__.
    Look there for the comments.
    The only change is to add linebreaks when this gets too long.
    """
    result = []
    pos_only = False
    kw_only = True
    for param in obj_signature.parameters.values():
        if param.kind == inspect._POSITIONAL_ONLY:
            pos_only = True
        elif pos_only:
            result.append('/')
            pos_only = False

        if param.kind == inspect._VAR_POSITIONAL:
            kw_only = False
        elif param.kind == inspect._KEYWORD_ONLY and kw_only:
            result.append('*')
            kw_only = False

        result.append(str(param))

    if pos_only:
        result.append('/')

    # add up name, parameters, braces (2), and commas
    if len(obj_name) + sum(len(r) + 2 for r in result) > 75:
        # This doesn’t fit behind “Signature: ” in an inspect window.
        rendered = '{}(\n{})'.format(obj_name, ''.join(
            '    {},\n'.format(r) for r in result)
        )
    else:
        rendered = '{}({})'.format(obj_name, ', '.join(result))

    if obj_signature.return_annotation is not inspect._empty:
        anno = inspect.formatannotation(obj_signature.return_annotation)
        rendered += ' -> {}'.format(anno)

    return rendered
    



        
        