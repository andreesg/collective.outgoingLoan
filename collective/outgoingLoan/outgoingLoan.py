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
from collective.z3cform.datagridfield.interfaces import IDataGridField
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


from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from collective.object.utils.widgets import SimpleRelatedItemsFieldWidget, AjaxSingleSelectFieldWidget, ExtendedRelatedItemsFieldWidget
from collective.object.utils.source import ObjPathSourceBinder
from plone.directives import dexterity, form

# # # # # # # # # # # # #
# # # # # # # # # # # # #
# OutgoingLoan schema     #
# # # # # # # # # # # # #
# # # # # # # # # # # # #

from plone.app.content.interfaces import INameFromTitle
class INameFromLoanNumber(INameFromTitle):
    def title():
        """Return a processed title"""

class NameFromLoanNumber(object):
    implements(INameFromLoanNumber)
    
    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        return self.context.title

class IOutgoingLoan(form.Schema):

    priref =  schema.TextLine(
        title=_(u'priref'),
        required=False
    )
    dexteritytextindexer.searchable('priref')

    # # # # # # # # # # #
    # Loan Request      # 
    # # # # # # # # # # #

    # General
    model.fieldset('loan_request', label=_(u'Loan Request'), 
        fields=['title',
                'loanRequest_general_requester', 'loanRequest_general_contact',
                'loanRequest_internalCoordination_coordinator', 'loanRequest_internalCoordination_administrConcerned',
                'loanRequest_requestDetails_periodFrom', 'loanRequest_requestDetails_to',
                'loanRequest_requestDetails_reason', 'loanRequest_requestDetails_exhibition',
                'loanRequest_requestLetter_date', 'loanRequest_requestLetter_digRef',
                'loanRequest_requestConfirmation_template', 'loanRequest_requestConfirmation_date',
                'loanRequest_requestConfirmation_digRef', 'loanRequest_requestConfirmation_templateCheck']
    )

    title = schema.TextLine(
        title=_(u'Loan number'),
        required=True
    )
    dexteritytextindexer.searchable('title')

    loanRequest_general_requester = RelationList(
        title=_(u'Requester'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution')
        ),
        required=False
    )
    form.widget('loanRequest_general_requester', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    loanRequest_general_contact = RelationList(
        title=_(u'Contact'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution')
        ),
        required=False
    )
    form.widget('loanRequest_general_contact', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    # Internal coordination
    loanRequest_internalCoordination_coordinator = RelationList(
        title=_(u'Coordinator'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution')
        ),
        required=False
    )
    form.widget('loanRequest_internalCoordination_coordinator', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

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
        required=True,
        default="No value",
        missing_value=" "
    )
    dexteritytextindexer.searchable('loanRequest_requestDetails_reason')

    loanRequest_requestDetails_exhibition = RelationList(
        title=_(u'Exhibition'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='Exhibition')
        ),
        required=False
    )
    form.widget('loanRequest_requestDetails_exhibition', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    # Request letter
    loanRequest_requestLetter_date = schema.TextLine(
        title=_(u'label_date', default=u'Date'),
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
        required=True,
        default="No value",
        missing_value=" "
    )
    dexteritytextindexer.searchable('loanRequest_requestConfirmation_template')

    loanRequest_requestConfirmation_templateCheck = schema.Bool(
        title=_(u''),
        required=False,
        default=False,
        missing_value=False
    )
    dexteritytextindexer.searchable('loanRequest_requestConfirmation_templateCheck')

    loanRequest_requestConfirmation_date = schema.TextLine(
        title=_(u'label_date', default=u'Date'),
        required=False
    )
    dexteritytextindexer.searchable('loanRequest_requestConfirmation_date')

    loanRequest_requestConfirmation_digRef = schema.TextLine(
        title=_(u'Dig. ref.'),
        required=False
    )
    dexteritytextindexer.searchable('loanRequest_requestConfirmation_digRef')

    # # # # # #
    # Objects #
    # # # # # #
    
    model.fieldset('objects', label=_(u'Objects'), 
        fields=['objects_object']
    )

    # Object
    objects_object = ListField(title=_(u'Object'),
        value_type=DictRow(title=_(u'Object'), schema=IObjects),
        required=False)
    form.widget(objects_object=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('objects_object')


    # # # # # # #
    # Contract  #
    # # # # # # #
    model.fieldset('contract', label=_(u'Contract'), 
        fields=['contract_contractDetails_requestPeriodFrom',
                'contract_contractDetails_to', 'contract_contractDetails_conditions',
                'contract_contractDetails_notes', 'contract_contractLetter_template',
                'contract_contractLetter_date', 'contract_contractLetter_digRef',
                'contract_contractLetter_signedReturned', 'contract_contractLetter_signedReturnedDigRef',
                'contract_conditionReport_template', 'contract_conditionReport_date',
                'contract_conditionReport_digRef', 'contract_extension', 'contract_contractLetter_returned',
                'contract_conditionReport_templateCheck', 'contract_contractLetter_templateCheck']
    )

    # Contract details
    contract_contractDetails_requestPeriodFrom = schema.TextLine(
        title=_(u'Request period from'),
        required=False
    )
    dexteritytextindexer.searchable('contract_contractDetails_requestPeriodFrom')

    contract_contractDetails_to = schema.TextLine(
        title=_(u'to'),
        required=False
    )
    dexteritytextindexer.searchable('contract_contractDetails_to')

    contract_contractDetails_conditions = schema.TextLine(
        title=_(u'Conditions'),
        required=False
    )
    dexteritytextindexer.searchable('contract_contractDetails_conditions')

    contract_contractDetails_notes = ListField(title=_(u'label_notes', default=u'Notes'),
        value_type=DictRow(title=_(u'label_notes', default=u'Notes'), schema=INotes),
        required=False)
    form.widget(contract_contractDetails_notes=DataGridFieldFactory)
    dexteritytextindexer.searchable('contract_contractDetails_notes')

    # Contract letter
    contract_contractLetter_template = schema.Choice(
        vocabulary=template_vocabulary,
        title=_(u'Template'),
        required=True,
        default="No value",
        missing_value=" "
    )
    dexteritytextindexer.searchable('contract_contractLetter_template')

    contract_contractLetter_templateCheck = schema.Bool(
        title=_(u''),
        required=False,
        default=False,
        missing_value=False
    )

    contract_contractLetter_date = schema.TextLine(
        title=_(u'label_date', default=u'Date'),
        required=False
    )
    dexteritytextindexer.searchable('contract_contractLetter_date')

    contract_contractLetter_digRef = schema.TextLine(
        title=_(u'(Dig.) ref.'),
        required=False
    )
    dexteritytextindexer.searchable('contract_contractLetter_digRef')

    contract_contractLetter_signedReturned = schema.TextLine(
        title=_(u'Signed & returned'),
        required=False
    )
    dexteritytextindexer.searchable('contract_contractLetter_signedReturned')

    contract_contractLetter_returned = schema.Bool(
        title=_(u''),
        required=False,
        default=False,
        missing_value=False
    )

    contract_contractLetter_signedReturnedDigRef = schema.TextLine(
        title=_(u'(Dig.) ref.'),
        required=False
    )
    dexteritytextindexer.searchable('contract_contractLetter_signedReturnedDigRef')

    # Condition report
    contract_conditionReport_template = schema.Choice(
        vocabulary=template_vocabulary,
        title=_(u'Template'),
        required=True,
        default="No value",
        missing_value=" "
    )
    dexteritytextindexer.searchable('contract_conditionReport_template')

    contract_conditionReport_templateCheck = schema.Bool(
        title=_(u''),
        required=False,
        default=False,
        missing_value=False
    )
    dexteritytextindexer.searchable('contract_conditionReport_templateCheck')

    contract_conditionReport_date = schema.TextLine(
        title=_(u'label_date', default=u'Date'),
        required=False
    )
    dexteritytextindexer.searchable('contract_conditionReport_date')

    contract_conditionReport_digRef = schema.TextLine(
        title=_(u'(Dig.) ref.'),
        required=False
    )
    dexteritytextindexer.searchable('contract_conditionReport_digRef')

    # Extension
    contract_extension = ListField(title=_(u'Extension'),
        value_type=DictRow(title=_(u'Extension'), schema=IExtension),
        required=False)
    form.widget(contract_extension=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('contract_extension')

    # # # # # # # # #
    # Transport     #
    # # # # # # # # #
    model.fieldset('transport', label=_(u'Transport'), 
        fields=['transport_despatchDetails', 'transport_entrydetails']
    )

    transport_despatchDetails = ListField(title=_(u'Despatch details'),
        value_type=DictRow(title=_(u'Despatch details'), schema=IDespatchDetails),
        required=False)
    form.widget(transport_despatchDetails=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('transport_despatchDetails')

    transport_entrydetails = RelationList(
        title=_(u'Entry number'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='ObjectEntry')
        ),
        required=False
    )
    form.widget('transport_entrydetails', ExtendedRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    # # # # # # # # # #
    # Correspondence  #
    # # # # # # # # # #
    model.fieldset('correspondence', label=_(u'Correspondence'), 
        fields=['correspondence_otherCorrespondence']
    )

    correspondence_otherCorrespondence = ListField(title=_(u'Correspondence'),
        value_type=DictRow(title=_(u'Correspondence'), schema=ICorrespondence),
        required=False)
    form.widget(correspondence_otherCorrespondence=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('correspondence_otherCorrespondence')


    # # # # # # # # # #
    # Related loans   #
    # # # # # # # # # #
    model.fieldset('related_loans', label=_(u'Related loans'), 
        fields=['relatedLoans_relatedLoans']
    )

    relatedLoans_relatedLoans = ListField(title=_(u'Related loans'),
        value_type=DictRow(title=_(u'Related loans'), schema=IRelatedLoans),
        required=False)
    form.widget(relatedLoans_relatedLoans=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('relatedLoans_relatedLoans')
    
    



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
                if IDataGridField.providedBy(widget):
                    widget.auto_append = False
                    widget.allow_reorder = True
                alsoProvides(widget, IFormWidget)

class AddView(add.DefaultAddView):
    form = AddForm
    

class EditForm(edit.DefaultEditForm):
    template = ViewPageTemplateFile('outgoingLoan_templates/edit.pt')
    
    def update(self):
        super(EditForm, self).update()
        for group in self.groups:
            for widget in group.widgets.values():
                if IDataGridField.providedBy(widget):
                    widget.auto_append = False
                    widget.allow_reorder = True
                alsoProvides(widget, IFormWidget)

