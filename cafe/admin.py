from django.contrib import admin
from .models import Cities
from .models import Cuisine
from .models import Kind
from .models import Cafe
from .models import Areaplace, Photo

admin.site.register(Cities)
admin.site.register(Cuisine)
admin.site.register(Kind)
admin.site.register(Cafe)
admin.site.register(Areaplace)
admin.site.register(Photo)