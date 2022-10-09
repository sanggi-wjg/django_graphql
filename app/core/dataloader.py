from promise import Promise
from promise.dataloader import DataLoader

from app.core.colorful import yellow


def _get_model_batch_load_fn(model):
    """Create batch load function for model.  """

    def batch_load_fn(keys):
        # keys = [int(i) for i in keys]
        # result = model.objects.in_bulk(keys)
        # yellow("batch_load_fn:", model, keys, result)
        # return Promise.resolve([result[i] for i in keys])
        keys = [int(i) for i in keys]
        result = model.objects.in_bulk(keys)
        yellow("batch_load_fn:", model, keys, result)
        return Promise.resolve([result[i] for i in keys])

    return batch_load_fn


def _get_model_cache_key(v):
    if isinstance(v, int):
        return str(v)
    return v


def dataloader(model):
    """Create dataloader for model.  """

    return DataLoader(
        _get_model_batch_load_fn(model),
        get_cache_key=_get_model_cache_key
    )
