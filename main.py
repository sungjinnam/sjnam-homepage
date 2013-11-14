#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
# import logging
# import wsgiref.handlers
from google.appengine.ext.webapp import template

def doRender(handler, tname = 'index.html', values = { }):
    temp = os.path.join(os.path.dirname(__file__), 'htmls/' + tname)
    if not os.path.isfile(temp): 
        return False

    #supposed to be rendering a non-html file?
    binary = False
    if temp.endswith(".jpg") or temp.endswith(".jpeg"):
        handler.response.headers['Content-Type'] = 'image/jpeg'
        binary = True
    elif temp.endswith(".png"):
        handler.response.headers['Content-Type'] = 'image/png'
        binary = True

    if binary:
        outstr = open(temp, "rb").read()
        handler.response.out.write(outstr)
        return True

    newval = dict(values)
    newval['path'] = handler.request.path
    outstr = template.render(temp, newval)
    handler.response.out.write(outstr)
    return True

class WorksHandler(webapp2.RequestHandler):
    def get(self):
        doRender(self, '/works.html')
class MainHandler(webapp2.RequestHandler):
    def get(self):
        # self.response.write('Hello world!')
        # self.response.write("<h1>Hello world!</h1>")
        if doRender(self, self.request.path):
            return
        doRender(self, 'index.html')

# # def main():
# #     app = webapp2.WSGIApplication([
# #         ('/', MainHandler)
# #     ], debug=True)
# #     wsgiref.handlers.CGIHandler().run(app)

# # if __name__ == '__main__':
# #     main()
# app = webapp2.WSGIApplication([('/', MainHandler)], debug=True)
# # app = webapp2.WSGIApplication([('/', IndexHandler)], debug=True)

# class MainHandler(webapp2.RequestHandler):
#     def get(self):
#         self.response.headers['Content-Type'] = 'text/plain'
#         self.response.write('Hello World')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/works', WorksHandler)
    ], debug=True)

