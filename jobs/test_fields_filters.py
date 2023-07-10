# jobs/test_fields_filters

from models import Client

queryset = Client.objects.all()
for row in queryset:
    print(row)
