#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface
from collective.outgoingLoan import MessageFactory as _
from ..utils.vocabularies import _createReasonVocabulary, _createTemplateVocabulary
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

reason_vocabulary = SimpleVocabulary(list(_createReasonVocabulary()))
template_vocabulary = SimpleVocabulary(list(_createTemplateVocabulary()))

class ListField(schema.List):
    """We need to have a unique class for the field list so that we
    can apply a custom adapter."""
    pass

# # # # # # # # # # # # #
# Widget interface      #
# # # # # # # # # # # # #

class IFormWidget(Interface):
    pass


# # # # # # # # # # # # # #
# DataGrid interfaces     # 
# # # # # # # # # # # # # #

class IAdministrConcerned(Interface):
    name = schema.TextLine(title=_(u'Administr. concerned'), required=False)

class IDocumentationDocumentation(Interface):
    article = schema.TextLine(title=_(u'Article'), required=False)
    title = schema.TextLine(title=_(u'Title'), required=False)
    author = schema.TextLine(title=_(u'Author'), required=False)
    pageMark = schema.TextLine(title=_(u'Page mark'), required=False)
    shelfMark = schema.TextLine(title=_(u'Shelf mark'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)

