from django.utils.html import format_html
from .models import Tags
from django.contrib.admin import ModelAdmin, display, register


@register(Tags)
class TagAdmin(ModelAdmin):
    '''Администрирование тэгов'''
    list_display = ("name", "slug", "color_code")
    search_fields = ("name", "color")

    save_on_top = True
    empty_value_display = 'Значение не указано'

    @display(description="Colored")
    def color_code(self, obj: Tags):
        return format_html(
            '<span style="color: #{};">{}</span>', obj.color[1:], obj.color
        )

    color_code.short_description = "Цветовой код тэга"
