# -*- encoding: iso-8859-15 -*-
# (C) Copyright 2006 Nuxeo SARL <http://nuxeo.com>
# Author: Tarek Ziadé <tz@nuxeo.com>
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
import os, sys
import doctest
import unittest

from Testing.ZopeTestCase import FunctionalDocFileSuite
from Testing.ZopeTestCase import FunctionalDocTestSuite
from Testing.ZopeTestCase import FunctionalTestCase
from Testing.ZopeTestCase import user_name, folder_name

from Products.PageTemplates.ZopePageTemplate import ZopePageTemplate

from Products.CPSResourceLibrary.resourcelibrary import ResourceRegisterer

directory = os.path.dirname(__file__)

from OFS.SimpleItem import SimpleItem

class fakeScript(SimpleItem):

    def __call__(self, libname, **kw):
        request = self.REQUEST
        context = self
        reg = ResourceRegisterer(context, request)
        reg.need(libname)

class TestCase(FunctionalTestCase):

    def afterSetUp(self):
        # creating a page template
        pt_file = os.path.join(directory, 'example.pt')
        code = open(pt_file).read()
        pt_ob = ZopePageTemplate('example', code)
        self.folder._setObject('example', pt_ob)

        # let's bind here 'needResource' to the context
        self.folder._setObject('needResource', fakeScript())

        # making sure it works (ie the pt compiles OK)
        self.folder.example()

def test_suite():
    return unittest.TestSuite((
        FunctionalDocFileSuite('../resourcelibrary.txt',
                               optionflags = doctest.REPORT_ONLY_FIRST_FAILURE|
                                             doctest.ELLIPSIS,
                               package='Products.CPSResourceLibrary.tests',
                               test_class=TestCase),
        ))

if __name__ == '__main__':
    unittest.TextTestRunner().run(test_suite())