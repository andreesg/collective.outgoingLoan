#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Zope dependencies
#
from zope import schema
from zope.interface import invariant, Invalid, Interface, implements
from zope.interface import alsoProvides
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.fieldproperty import FieldProperty
from zope.component import getMultiAdapter

#
# Plone dependencies
#
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.supermodel import model
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

#
# z3c.forms dependencies
#
from z3c.form import group, field
from z3c.form.form import extends
from z3c.form.browser.textlines import TextLinesFieldWidget

#
# plone.app.widgets dependencies
#
from plone.app.widgets.dx import DatetimeFieldWidget

#
# DataGridFields dependencies
#
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from collective.z3cform.datagridfield.blockdatagridfield import BlockDataGridFieldFactory

# # # # # # # # # # # # # # # 
# Dexterity imports         # 
# # # # # # # # # # # # # # # 
from five import grok
from collective import dexteritytextindexer
from plone.dexterity.browser.view import DefaultView
from plone.dexterity.content import Container
from plone.dexterity.browser import add, edit

# # # # # # # # # # # # # # # # # #
# !OutgoingLoan specific imports!   #
# # # # # # # # # # # # # # # # # #
from collective.outgoingLoan import MessageFactory as _
from .utils.vocabularies import *
from .utils.interfaces import *
from .utils.views import *

# # # # # # # # # # # # #
# # # # # # # # # # # # #
# OutgoingLoan schema     #
# # # # # # # # # # # # #
# # # # # # # # # # # # #

class IOutgoingLoan(form.Schema):
    
    text = RichText(
        title=_(u"Body"),
        required=False
    )

    # # # # # # # # # # #
    # Loan Request      # 
    # # # # # # # # # # #

    # General
    model.fieldset('loan_request', label=_(u'Loan Request'), 
        fields=['loanRequest_general_loanNumber',
                'loanRequest_general_requester', 'loanRequest_general_contact',
                'loanRequest_internalCoordination_coordinator', 'loanRequest_internalCoordination_administrConcerned',
                'loanRequest_requestDetails_periodFrom', 'loanRequest_requestDetails_to',
                'loanRequest_requestDetails_reason', 'loanRequest_requestDetails_exhibition',
                'loanRequest_requestLetter_date', 'loanRequest_requestLetter_digRef',
                'loanRequest_requestConfirmation_template', 'loanRequest_requestConfirmation_date',
                'loanRequest_requestConfirmation_digRef']
    )

    loanRequest_general_loanNumber = schema.TextLine(
        title=_(u'Loan number'),
        required=False
    )
    dexteritytextindexer.searchable('loanRequest_general_loanNumber')

    loanRequest_general_requester = schema.TextLine(
        title=_(u'Requester'),
        required=False
    )
    dexteritytextindexer.searchable('loanRequest_general_requester')

    loanRequest_general_contact = schema.TextLine(
        title=_(u'Contact'),
        required=False
    )
    dexteritytextindexer.searchable('loanRequest_general_contact')

    # Internal coordination
    loanRequest_internalCoordination_coordinator = schema.TextLine(
        title=_(u'Coordinator'),
        required=False
    )
    dexteritytextindexer.searchable('loanRequest_internalCoordination_coordinator')

    loanRequest_internalCoordination_administrConcerned = ListField(title=_(u'Administr. concerned'),
        value_type=DictRow(title=_(u'Administr. concerned'), schema=IAdministrConcerned),
        required=False)
    form.widget(loanRequest_internalCoordination_administrConcerned=DataGridFieldFactory)
    dexteritytextindexer.searchable('loanRequest_internalCoordination_administrConcerned')

    # Request details
    loanRequest_requestDetails_periodFrom = schema.TextLine(
        title=_(u'Period from'),
        required=False
    )
    dexteritytextindexer.searchable('loanRequest_requestDetails_periodFrom')

    loanRequest_requestDetails_to = schema.TextLine(
        title=_(u'to'),
        required=False
    )
    dexteritytextindexer.searchable('loanRequest_requestDetails_to')

    loanRequest_requestDetails_reason = schema.Choice(
        vocabulary=reason_vocabulary,
        title=_(u'Reason'),
        required=False
    )
    dexteritytextindexer.searchable('loanRequest_requestDetails_reason')

    loanRequest_requestDetails_exhibition = schema.TextLine(
        title=_(u'Exhibition'),
        required=False
    )
    dexteritytextindexer.searchable('loanRequest_requestDetails_exhibition')

    # Request letter
    loanRequest_requestLetter_date = schema.TextLine(
        title=_(u'Date'),
        required=False
    )
    dexteritytextindexer.searchable('loanRequest_requestLetter_date')

    loanRequest_requestLetter_digRef = schema.TextLine(
        title=_(u'Dig. ref.'),
        required=False
    )
    dexteritytextindexer.searchable('loanRequest_requestLetter_digRef')

    # Request confirmation
    loanRequest_requestConfirmation_template = schema.Choice(
        vocabulary=template_vocabulary,
        title=_(u'Template'),
        required=False
    )
    dexteritytextindexer.searchable('loanRequest_requestConfirmation_template')

    loanRequest_requestConfirmation_date = schema.TextLine(
        title=_(u'Date'),
        required=False
    )
    dexteritytextindexer.searchable('loanRequest_requestConfirmation_date')

    loanRequest_requestConfirmation_digRef = schema.TextLine(
        title=_(u'Dig. ref.'),
        required=False
    )
    dexteritytextindexer.searchable('loanRequest_requestConfirmation_digRef')

    # # # # # # # # # #
    # Documentation   #
    # # # # # # # # # #
    model.fieldset('documentation', label=_(u'Documentation'), 
        fields=['documentation_documentation']
    )

    documentation_documentation = ListField(title=_(u'Documentation'),
        value_type=DictRow(title=_(u'Documentation'), schema=IDocumentationDocumentation),
        required=False)
    form.widget(documentation_documentation=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('documentation_documentation')



# # # # # # # # # # # # # # #
# OutgoingLoan declaration  #
# # # # # # # # # # # # # # #

class OutgoingLoan(Container):
    grok.implements(IOutgoingLoan)
    pass

# # # # # # # # # # # # # # # # # 
# OutgoingLoan add/edit views   # 
# # # # # # # # # # # # # # # # #

class AddForm(add.DefaultAddForm):
    template = ViewPageTemplateFile('outgoingLoan_templates/add.pt')
    def update(self):
        super(AddForm, self).update()
        for group in self.groups:
            for widget in group.widgets.values():
                alsoProvides(widget, IFormWidget)

class AddView(add.DefaultAddView):
    form = AddForm
    

class EditForm(edit.DefaultEditForm):
    template = ViewPageTemplateFile('outgoingLoan_templates/edit.pt')
    
    def update(self):
        super(EditForm, self).update()
        for group in self.groups:
            for widget in group.widgets.values():
                alsoProvides(widget, IFormWidget)

