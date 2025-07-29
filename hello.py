print("hello world")
from typing import Callable
import inspect


class Tool:
    """
    A class representing a reusable piece of code (Tool).

    Attributes:
        name (str): Name of the tool.
        description (str): A textual description of what the tool does.
        func (callable): The function this tool wraps.
        arguments (list): A list of arguments.
        outputs (str or list): The return type(s) of the wrapped function.
    """
    def __init__(self,
                 name: str,
                 description: str,
                 func: Callable,
                 arguments: list,
                 outputs: str):
        self.name = name
        self.description = description
        self.func = func
        self.arguments = arguments
        self.outputs = outputs

    def to_string(self) -> str:
        """
        Return a string representation of the tool,
        including its name, description, arguments, and outputs.
        """
        args_str = ", ".join([
            f"{arg_name}: {arg_type}" for arg_name, arg_type in self.arguments
        ])

        return (
            f"Tool Name: {self.name},"
            f" Description: {self.description},"
            f" Arguments: {args_str},"
            f" Outputs: {self.outputs}"
        )

    def __call__(self, *args, **kwargs):
        """
        Invoke the underlying function (callable) with provided arguments.
        """
        return self.func(*args, **kwargs)
   
def tool(func): # uses Python's inspect module to look at the function you are decorating and automatically extracts its name (__name__), its description (__doc__), its parameters, and its return type.
    # It populates the blueprint: It takes all the information it just extracted and neatly plugs it into the Tool class blueprint by creating a new instance (Tool(...)).
    """
    A decorator that creates a Tool instance from the given function.
    """
    # Get the function signature
    signature = inspect.signature(func)
    print(f"Creating tool for function: {func.__name__}")
    print(f"Function signature: {signature}")

    # Extract (param_name, param_annotation) pairs for inputs
    print(f"signature.parameters:", signature.parameters.values()) 
    arguments = []
    for param in signature.parameters.values():
        annotation_name = (
            param.annotation.__name__
            if hasattr(param.annotation, '__name__')
            else str(param.annotation)
        )
        arguments.append((param.name, annotation_name))
    print(f"Arguments: {arguments}")
    # Determine the return annotation
    return_annotation = signature.return_annotation
    if return_annotation is inspect._empty:
        outputs = "No return annotation"
    else:
        outputs = (
            return_annotation.__name__
            if hasattr(return_annotation, '__name__')
            else str(return_annotation)
        )

    # Use the function's docstring as the description (default if None)
    description = func.__doc__ or "No description provided."

    # The function name becomes the Tool name
    name = func.__name__

    # Return a new Tool instance
    return Tool(
        name=name,
        description=description,
        func=func,
        arguments=arguments,
        outputs=outputs
    )

@tool
def calculator(a: int, b: int) -> int:
    """Multiply two integers."""
    print(f"Calculating: {a} * {b}")
    return a * b
print("Tool created:")
print(calculator.name)
print(calculator.description)
print("Arguments:", calculator.arguments)
print("Outputs:", calculator.outputs)
print("Tool representation:")
print(calculator.to_string())




