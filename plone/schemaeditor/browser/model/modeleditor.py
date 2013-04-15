from Products.Five import BrowserView


class ModelEditorView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def modelSource(self):
        return self.context.fti.model_source
