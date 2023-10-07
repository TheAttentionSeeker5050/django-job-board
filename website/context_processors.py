from django.conf import settings

def tinymce_js_url(request):
    # only return the part after staticfiles' storage location
    return {'TINYMCE_JS_URL': 'libs/tinymce/js/tinymce/tinymce.min.js'}