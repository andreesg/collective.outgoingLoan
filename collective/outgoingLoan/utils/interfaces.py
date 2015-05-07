#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface
from collective.outgoingLoan import MessageFactory as _
from ..utils.vocabularies import *
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

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

class IObjects(Interface):
    objectNumber = schema.TextLine(title=_(u'Object number'), required=False)
    loanTitle = schema.TextLine(title=_(u'Loan title'), required=False)
    status = schema.Choice(
        vocabulary=status_vocabulary,
        title=_(u'Status'),
        required=False
    )

    date = schema.TextLine(title=_(u'Date'), required=False)
    authoriserInternal = schema.TextLine(title=_(u'Authoriser (internal)'), required=False)
    authorisationDate = schema.TextLine(title=_(u'Authorisation date'), required=False)

    # Review request
    reviewRequest_template = schema.Choice(
        vocabulary=template_vocabulary,
        title=_(u'Template'),
        required=False
    )

    reviewRequest_date = schema.TextLine(title=_(u'Date'), required=False)
    reviewRequest_digRef = schema.TextLine(title=_(u'Dig. ref.'), required=False)

    # Permission owner 
    permissionOwner_requestTemplate = schema.Choice(
        vocabulary=template_vocabulary,
        title=_(u'Request template'),
        required=False
    )

    permissionOwner_date = schema.TextLine(title=_(u'Date'), required=False)
    permissionOwner_digRef = schema.TextLine(title=_(u'Dig. ref.'), required=False)
    permissionOwner_permissionResult = schema.Choice(
        vocabulary=permission_result_vocabulary,
        title=_(u'Permission result'),
        required=False
    )
    permissionOwner_permissionDigRef = schema.TextLine(title=_(u'Dig. ref.'), required=False)

    # Miscellaneous
    miscellaneous_insuranceValue = schema.TextLine(title=_(u'Insurance Value'), required=False)
    miscellaneous_currency = schema.TextLine(title=_(u'Currency'), required=False)
    miscellaneous_conditions = schema.TextLine(title=_(u'Conditions'), required=False)
    miscellaneous_notes = schema.TextLine(title=_(u'Notes'), required=False)


