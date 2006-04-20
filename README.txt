==================
CPSResourceLibrary
==================

What it does
============

CPSResourceLibrary keeps a registery of JavaScript, CSS, and other resources
files in memory, and let the different page parts ask for them to be included
when the page is rendered.

This is useful for example, to include Javascripts within a CPS Portlet
without having to change the main header lib template, and therefore
make the page, even if the portlet is not shown, loads unecessary resources.

How it does
===========

The product work in three steps:

    - a registery hooked to the response object, keeps a list of registered
      resources to be append.

    - a portlet, or any kind of zpt based renderer, signals
      that it needs a given resource, by adding a call to the view.

    - the publisher, just before sending back the result page,
      inject in the header the library calls


Where it heads
==============

This product works exactly like Zope 3 product from Zope Corp,
`zc.resourcelibrary`.

This product is intended to work for Zope 2 publisher, so it can be used
as is in CPS 3.4. When Zope 3 publisher will be fully integrated to Zope 2,
and when `zc.resourcelibrary` will be usable through Five, this
product won't be necessary anymore, as `zc.resourcelibrary` provide
a smoother way to ask for library, through a simple tal:expression.
