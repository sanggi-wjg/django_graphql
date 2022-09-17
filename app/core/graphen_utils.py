from graphql_relay import from_global_id, to_global_id


def get_id_from_gid(gid):
    try:
        _type, _id = from_global_id(gid)
    except Exception:
        from app.core.colorful import red
        red(f"get_id_from_gid() ERROR: {gid}")
        return None
    return _id


def get_gid_from_id(type, id):
    try:
        _gid = to_global_id(type, id)
    except Exception:
        from app.core.colorful import red
        red(f"get_gid_from_id() ERROR: {type, id}")
        return None
    return _gid
