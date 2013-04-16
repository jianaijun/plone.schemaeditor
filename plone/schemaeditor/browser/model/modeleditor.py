from zope.component import queryMultiAdapter
from Products.Five import BrowserView
from AccessControl import Unauthorized


class ModelEditorView(BrowserView):
    """ editor view """

    def modelSource(self):
        return self.context.fti.model_source


def authorized(context, request):
    authenticator = queryMultiAdapter((context, request),
                                      name=u"authenticator")
    return authenticator and authenticator.verify()


class AjaxSaveHandler(BrowserView):
    """ handle AJAX save posts """

    def __call__(self):
        """ handle AJAX save post """

        self.request.response.setHeader('Content-Type', 'text/plain')

        if not authorized(self.context, self.request):
            return "Unathorized"

        source = self.request.form.get('source')
        if source:
            fti = self.context.fti
            # XXX add sanity checks
            # fti._setPropValue('model_source', source)
            fti.manage_changeProperties(model_source=source)
            return "Saved"
