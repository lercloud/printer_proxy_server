def json_headers(f):
    def wrapped(*args, **kwargs):
        resp = f(*args, **kwargs)
        resp.headers['Content-Type'] = 'application/json'
        return resp
    return wrapped

