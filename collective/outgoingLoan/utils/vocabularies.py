#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from collective.outgoingLoan import MessageFactory as _
# # # # # # # # # # # # # #
# Vocabularies            #
# # # # # # # # # # # # # #

def _createReasonVocabulary():
    reasons = {
        "exhibition": _(u"exhibition"),
        "long term loan": _(u"long term loan"),
        "conservation/restoration": _(u"conservation/restoration")
    }

    for key, name in reasons.items():
        term = SimpleTerm(value=key, token=str(key), title=name)
        yield term

def _createTemplateVocabulary():
    templates = {
        "English": _(u"English"),
        "Dutch": _(u"Dutch")
    }

    for key, name in templates.items():
        term = SimpleTerm(value=key, token=str(key), title=name)
        yield term

reason_vocabulary = SimpleVocabulary(list(_createReasonVocabulary()))
template_vocabulary = SimpleVocabulary(list(_createTemplateVocabulary()))
