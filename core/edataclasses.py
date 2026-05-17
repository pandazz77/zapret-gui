from dataclasses import asdict, is_dataclass
from typing import get_type_hints, Dict, Any, Self, get_origin, get_args, Union
import collections.abc

class EDataclass:
    def to_dict(self) -> Dict[str, Any]:
        if not is_dataclass(self):
            raise TypeError(f"{self.__class__} is not a dataclass")
        return asdict(self)
    
    @classmethod
    def from_dict(cls: type[Self], data: Dict[str, Any]) -> Self:
        if not is_dataclass(cls):
            raise TypeError(f"{cls} is not a dataclass")
        
        # Get the type hints to know which fields are other dataclasses or complex types
        type_hints = get_type_hints(cls)
        kwargs = {}
        
        for field_name, value in data.items():
            field_type = type_hints.get(field_name)
            
            if field_name in type_hints:
                kwargs[field_name] = cls._from_dict_recursive(value, field_type)
            else:
                # If field is not in type hints, just assign the value directly
                kwargs[field_name] = value

        return cls(**kwargs)
    
    @classmethod
    def _from_dict_recursive(cls, value: Any, expected_type: type) -> Any:
        """Recursively create objects from dictionary values based on expected type."""
        if value is None:
            return None
        
        # Get the origin type for generic types like List[Point]
        origin_type = get_origin(expected_type)
        
        # Handle dataclass instances
        if is_dataclass(expected_type):
            if isinstance(value, dict):
                return expected_type.from_dict(value)
            else:
                return value
        
        # Handle list/tuple/generic sequences
        elif origin_type in (list, tuple, set) or (
            hasattr(origin_type, '__origin__') and 
            issubclass(origin_type, collections.abc.Sequence) and 
            origin_type is not str
        ):
            if not isinstance(value, (list, tuple, set)):
                return value
            
            args = get_args(expected_type)
            if args:  # If we have type arguments like List[Point]
                item_type = args[0]  # For List[Point], this would be Point
                converted_items = []
                for item in value:
                    converted_items.append(cls._from_dict_recursive(item, item_type))
                
                if origin_type is tuple:
                    return tuple(converted_items)
                elif origin_type is set:
                    return set(converted_items)
                else:  # list or other sequence types
                    return converted_items
            else:  # No type info available, just return as is
                return value
        
        # Handle dict types
        elif origin_type is dict:
            if not isinstance(value, dict):
                return value
            
            args = get_args(expected_type)
            if len(args) >= 2:  # Dict[key_type, value_type]
                key_type, value_type = args[0], args[1]
                return {
                    cls._from_dict_recursive(k, key_type): cls._from_dict_recursive(v, value_type)
                    for k, v in value.items()
                }
            else:
                return value
        
        # Handle Union types (including Optional which is Union[T, None])
        elif origin_type is Union:
            args = get_args(expected_type)
            # Try each union type until one works
            for arg_type in args:
                if arg_type is type(None):
                    continue
                try:
                    return cls._from_dict_recursive(value, arg_type)
                except Exception:
                    continue
            return value  # If all fail, return original value
        
        # Handle simple types
        else:
            # If it's a primitive type or doesn't match any special handling
            return value