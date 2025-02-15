from django.forms import widgets
from django.utils.safestring import mark_safe

class ImagePreviewWidget(widgets.FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and hasattr(value, "url"):
            output.append(f'''
                <div style="margin-bottom: 10px;">
                    <img src="{value.url}" style="max-height: 200px;"/>
                </div>
            ''')
        output.append(super().render(name, value, attrs))
        return mark_safe(''.join(output)) 