#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from collective.outgoingLoan import MessageFactory as _
# # # # # # # # # # # # # #
# Vocabularies            #
# # # # # # # # # # # # # #


def _createReviewStatusVocabulary():
    status = {
        "authorised": _(u"authorised"),
        "refused": _(u"refused"),
    }

    terms = []
    terms.append(SimpleTerm(value="No value", token=str("No value"), title=_(u" ")))
    for key, name in status.items():
        term = SimpleTerm(value=key, token=str(key), title=name)
        terms.append(term)
    
    return terms

def _createPermissionResultVocabulary():
    results = {
        "granted": _(u"Granted"),
        "refused": _(u"Refused")
    }

    terms = []
    terms.append(SimpleTerm(value="No value", token=str("No value"), title=_(u" ")))
    for key, name in results.items():
        term = SimpleTerm(value=key, token=str(key), title=name)
        terms.append(term)
    
    return terms

def _createStatusVocabulary():
    status = {
        "under consideration": _(u"under consideration"),
        "under discussion": _(u"under discussion"),
        "approved": _(u"approved"),
        "refused": _(u"refused"),
        "withdrawn": _(u"withdrawn"),
        "dispatched": _(u"dispatched"),
        "on_loan": _(u"on loan"),
        "renewed": _(u"renewed"),
        "returned": _(u"returned"),
    }

    terms = []
    terms.append(SimpleTerm(value="No value", token=str("No value"), title=_(u" ")))
    for key, name in status.items():
        term = SimpleTerm(value=key, token=str(key), title=name)
        terms.append(term)
    
    return terms

def _createReasonVocabulary():
    reasons = {
        "exhibition": _(u"exhibition"),
        "long term loan": _(u"long term loan"),
        "conservation/restoration": _(u"conservation/restoration")
    }

    terms = []
    terms.append(SimpleTerm(value="No value", token=str("No value"), title=_(u" ")))
    for key, name in reasons.items():
        term = SimpleTerm(value=key, token=str(key), title=name)
        terms.append(term)
    
    return terms

def _createTemplateVocabulary():
    templates = {
        "English": _(u"English"),
        "Dutch": _(u"Dutch"),
        "German": _(u"German")
    }

    terms = []
    terms.append(SimpleTerm(value="No value", token=str("No value"), title=_(u" ")))
    for key, name in templates.items():
        term = SimpleTerm(value=key, token=str(key), title=name)
        terms.append(term)
    
    return terms

reason_vocabulary = SimpleVocabulary(list(_createReasonVocabulary()))
template_vocabulary = SimpleVocabulary(list(_createTemplateVocabulary()))
permission_result_vocabulary = SimpleVocabulary(list(_createPermissionResultVocabulary()))
status_vocabulary = SimpleVocabulary(list(_createStatusVocabulary()))
review_status_vocabulary = SimpleVocabulary(list(_createReviewStatusVocabulary()))
