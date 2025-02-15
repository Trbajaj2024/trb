from django.http import JsonResponse

class AjaxFormMixin:
    """Mixin to handle form submissions via AJAX"""
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'message': 'Successfully submitted form.'
            }
            return JsonResponse(data)
        return response 