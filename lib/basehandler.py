#!/usr/bin/env python3.4

from tornado import web

class BaseHandler(web.RequestHandler):
    def api_response(self, data, code=200, reason=None):
        self.write(data)
        self.set_status(code, reason)
        self.finish()

    def get_int_argument(self, name, default=None):
        value = None
        if default is None:
            try:
                value = self.get_argument(name)
            except web.MissingArgumentError:
                raise web.HTTPError(400, reason="Missing argument {}".format(name))
        else:
            value = self.get_argument(name, default)
        try:
            result = int(value)
        except (TypeError, ValueError):
            raise web.HTTPError(400, reason="Invalid value for arugment: {}".format(name))
        return result

    def error(self, code, reason=None):
        self.set_status(code, reason)
        self.finish()

    def get_all_arguments(self):
        data = self.request.arguments
        for k, v in data.iteritems():
            if len(v) == 1:
                data[k] = v[0]
        return data

