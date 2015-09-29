#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface
from collective.outgoingLoan import MessageFactory as _
from ..utils.vocabularies import *
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from collective.object.utils.widgets import SimpleRelatedItemsFieldWidget, AjaxSingleSelectFieldWidget
from collective.object.utils.source import ObjPathSourceBinder
from plone.directives import dexterity, form

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

class INotes(Interface):
    note = schema.Text(title=_(u'Notes'), required=False)

class IDocumentationDocumentation(Interface):
    article = schema.TextLine(title=_(u'Article'), required=False)
    title = schema.TextLine(title=_(u'Title'), required=False)
    author = schema.TextLine(title=_(u'Author'), required=False)
    pageMark = schema.TextLine(title=_(u'Page mark'), required=False)
    shelfMark = schema.TextLine(title=_(u'Shelf mark'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)

class IObjects(Interface):
    objectNumber = RelationList(
        title=_(u'Object number'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='Object')
        ),
        required=False
    )
    form.widget('objectNumber', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    loanTitle = schema.TextLine(title=_(u'Loan title'), required=False)
    status = schema.Choice(
        vocabulary=status_vocabulary,
        title=_(u'Status'),
        required=False
    )

    date = schema.TextLine(title=_(u'label_date', default=u'Date'), required=False)
    authoriserInternal = RelationList(
        title=_(u'Authoriser (internal)'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution')
        ),
        required=False
    )
    form.widget('authoriserInternal', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

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
    miscellaneous_currency = schema.List(
        title=_(u'Currency'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[],
        default=[]
    )
    form.widget('miscellaneous_currency', AjaxSingleSelectFieldWidget, vocabulary="collective.object.currency")


    miscellaneous_conditions = schema.TextLine(title=_(u'Conditions'), required=False)
    miscellaneous_notes = schema.Text(title=_(u'Notes'), required=False)

## Contract
class IExtension(Interface):
    request_newEndDate = schema.TextLine(title=_(u'New end date'), required=False)
    request_date = schema.TextLine(title=_(u'label_date', default=u'Date'), required=False)
    request_digRef = schema.TextLine(title=_(u'(Dig.) ref.'), required=False)

    # Review
    review_status = schema.Choice(
        vocabulary=review_status_vocabulary,
        title=_(u'Status'),
        required=False
    )

    review_date = schema.TextLine(title=_(u'label_date', default=u'Date'), required=False)
    review_authoriser = RelationList(
        title=_(u'Authoriser'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution')
        ),
        required=False
    )
    form.widget('review_authoriser', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    review_newEndDate = schema.TextLine(title=_(u'New end date'), required=False)
    review_notes = schema.Text(title=_(u'Notes'), required=False)

    # Result
    result_template = schema.Choice(
        vocabulary=template_vocabulary,
        title=_(u'Template'),
        required=False
    )
    result_date = schema.TextLine(title=_(u'label_date', default=u'Date'), required=False)
    result_digRef = schema.TextLine(title=_(u'(Dig.) ref.'), required=False)

## Correspondence
class ICorrespondence(Interface):
	digitalReference = schema.TextLine(title=_(u'(Digital) Reference'), required=False)
	date = schema.TextLine(title=_(u'label_date'), required=False)
	sender = schema.TextLine(title=_(u'Sender'), required=False)
	destination = schema.TextLine(title=_(u'Destination'), required=False)
	subject = schema.TextLine(title=_(u'Subject'), required=False)

class IDespatchDetails(Interface):
    despatchNumber = schema.TextLine(title=_(u'Despatch number'), required=False)

class IEntryDetails(Interface):
    entryNumber = RelationList(
        title=_(u'Entry number'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='ObjectEntry')
        ),
        required=False
    )
    form.widget('entryNumber', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')


class IRelatedLoans(Interface):
    loanNumber = RelationList(
        title=_(u'Loan number'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='OutgoingLoan')
        ),
        required=False
    )
    form.widget('loanNumber', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    relationType = schema.TextLine(title=_(u'Relation type'), required=False)





