from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.views import View


class S3StorageView(View):

    def get(self, request, *args, **kwargs):
        d = default_storage.exists('public/default_product.png')

        file = default_storage.open("public/sample.txt", 'w')
        file.write("sample sample sample\n sample\t sample\n\n sample")
        file.close()

        return HttpResponse("hello")
