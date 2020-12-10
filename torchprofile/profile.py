import warnings

from .utils.trace import trace
from .macs_handlers import handlers as macs_handlers
from .acts_handlers import handlers as acts_handlers

__all__ = ['profile_macs']

def profile(model, handlers, args, kwargs, reduction):
    results = dict()

    graph = trace(model, args, kwargs)
    for node in graph.nodes:
        for operators, func in handlers:
            if isinstance(operators, str):
                operators = [operators]
            if node.operator in operators:
                if func is not None:
                    results[node] = func(node)
                break
        else:
            warnings.warn('No handlers found: "{}". Skipped.'.format(
                node.operator))

    if reduction is not None:
        return reduction(results.values())
    else:
        return results

def profile_macs(model, args=(), kwargs=None, reduction=sum):
    return profile(model, macs_handlers, args, kwargs, reduction)
    
def profile_acts(model, args=(), kwargs=None, reduction=sum):
    return profile(model, acts_handlers, args, kwargs, reduction)