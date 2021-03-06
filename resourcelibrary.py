# -*- coding: ISO-8859-15 -*-
# Copyright (c) 2006 Nuxeo SARL <http://nuxeo.com>
# Authors: Tarek Ziad� <tz@nuxeo.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#
# $Id$
""" This module patches the publisher, in order
to provide the same feature as zc.resourcelibrary, see README.txt
"""
from Products.Five import BrowserView

RC_REGISTER = 'ResourceRegisterer.libraries'

class Library(object):
    """ library object used to hold resource infos """

    def __init__(self, name):
        self.name = name

class ResourceRegisterer(BrowserView):
    """ used to register a library in the response
    object """

    def _checkResource(self, rcname):
        """ checked the type of the resource """
        if rcname.endswith('.js') or rcname.endswith('.css'):
            return None
        raise ValueError('%s not recognized as a resource' % rcname)

    def need(self, library_name):
        """ add the resource to the list of resources to be injected """
        if self.request is None:
            return None

        # XXX would use an annotation in pure Zope 3 here
        response = self.request.response
        if not hasattr(response, 'rc_libraries'):
            response.rc_libraries = register = []
        else:
            register = response.rc_libraries

        libnames = [ob.name for ob in register]
        if library_name not in libnames:
            register.append(Library(library_name))


from ZPublisher.HTTPResponse import HTTPResponse
HTTPResponse.old_setBody = HTTPResponse.setBody
old_setBody = HTTPResponse.old_setBody

def setBodyWithResource(*args, **kw):
    """ calls the injector with the response """
    response = old_setBody(*args, **kw)
    # need to inject headers here
    return injectResources(response)

HTTPResponse.setBody = setBodyWithResource


def injectResources(response):
    """ injects the collected library into the header """
    if not hasattr(response, 'rc_libraries'):
        return None

    resources = response.rc_libraries

    html = []
    for resource in resources:
        name = resource.name
        if name.endswith('.js'):
            html.append('<script src="++resource++%s" ' % (name))
            html.append('    type="text/javascript">')
            html.append('</script>')
        elif name.endswith('.css'):
            html.append('<style type="text/css" media="all">')
            html.append('  <!--')
            html.append('    @import url("++resource++%s");'
                        % (name))
            html.append('  -->')
            html.append('</style>')
        else:
            raise RuntimeError('Resource library doesn\'t know how to '
                                'include this file: "%s"' % name)

    if html:
        body = response.body.replace('<head>', '<head>\n    %s\n' %
                                     '\n    '.join(html))
        response.old_setBody(body)
    return response
