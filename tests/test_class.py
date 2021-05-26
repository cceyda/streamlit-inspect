from typing import Tuple, List, Union, Dict, Optional

# Native: bool,float,str,int,
# list,set,dict?
# typing: tuple,union,
# list,dict,callable?,TypeVar,Any,optional


class Native_types:
    def input_float(inp: float, inp_def: float = 1.0) -> str:
        return inp, inp_def

    def input_int(inp: int, inp_def: int = 1) -> str:
        return inp, inp_def

    def input_bool(inp: bool, inp_def: bool = True) -> str:
        return inp, inp_def

    def input_str(inp: str, inp_def: str = "Predefined value") -> str:
        return inp, inp_def

    def input_multi(inp: str, inp_int: int, inp_bool: bool) -> str:
        return inp, inp_int, inp_bool

    def input_selfy(self, inp: str, inp_def: str = "Predefined") -> str:
        return inp, inp_def

    def input_args(*args) -> str:
        return args

    def input_kwargs(**kwargs) -> str:
        return kwargs


class Typing_types:
    def input_tuple(inp: Tuple[int, str]) -> str:
        return inp

    def input_tuple_w_defaults(inp: Tuple[int, str] = (5, "5")) -> str:
        return inp

    def input_union(inp: Union[int, str]) -> str:
        return inp

    def input_union_nested(inp: Union[int, Tuple[int, str]]) -> str:
        return inp
