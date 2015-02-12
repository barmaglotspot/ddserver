'''
Copyright 2013 Dustin Frisch <fooker@lab.sh>

This file is part of ddserver.

ddserver is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

ddserver is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with ddserver. If not, see <http://www.gnu.org/licenses/>.
'''

import bottle

from require import extend, export, require

from ddserver.config import parse_bool



@extend('ddserver.config:ConfigDeclaration')
def config_web(config_decl):
  with config_decl.declare('wsgi') as s:
    s('host',
      conv = str,
      default = '0.0.0.0')
    s('port',
      conv = int,
      default = 8080)
    s('debug',
      conv = parse_bool,
      default = False)



@export()
def WebApp():
  # Create a new bottle application
  return bottle.Bottle()



@export(webapp = 'ddserver.web:WebApp')
def Middleware(webapp):
  # Return the webapp as initial middleware
  return webapp



def route(*args, **kwargs):
  def wrapper(func):

    @extend('ddserver.web:WebApp')
    def extender(webapp):
      webapp.route(*args, **kwargs)(func)

    return extender
  return wrapper



@export()
class Web(object):
  @require(config = 'ddserver.config:Config',
           middleware = 'ddserver.web:Middleware')
  def run(self,
          config,
          middleware):
    bottle.run(app = middleware,
               host = config.wsgi.host,
               port = config.wsgi.port,
               debug = config.wsgi.debug)



import ddserver.interface.pages.index  # @UnusedImport: for web application
import ddserver.interface.pages.signup  # @UnusedImport: for web application
import ddserver.interface.pages.lostpasswd  # @UnusedImport: for web application
import ddserver.interface.pages.login  # @UnusedImport: for web application
import ddserver.interface.pages.user.account  # @UnusedImport: for web application
import ddserver.interface.pages.user.hosts  # @UnusedImport: for web application
import ddserver.interface.pages.user.host  # @UnusedImport: for web application
import ddserver.interface.pages.admin.users  # @UnusedImport: for web application
import ddserver.interface.pages.admin.suffixes  # @UnusedImport: for web application

import ddserver.updater.nic  # @UnusedImport: for web application

