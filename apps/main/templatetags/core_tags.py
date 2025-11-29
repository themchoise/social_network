from django import template
from django.utils.html import format_html

register = template.Library()

@register.filter(name="truncate_chars")
def truncate_chars(value, arg=100):
    """Trunca el texto a N caracteres agregando '…' si supera el límite."""
    try:
        length = int(arg)
    except (ValueError, TypeError):
        length = 100
    if not isinstance(value, str):
        value = str(value)
    if len(value) <= length:
        return value
    return value[:length].rstrip() + "…"

@register.filter(name="points_format")
def points_format(value):
    """Formatea puntos con separador de miles y sufijo 'pts'."""
    try:
        num = int(value)
    except (ValueError, TypeError):
        return value
    return f"{num:,} pts".replace(",", ".")  # Usar punto como separador miles

@register.filter(name="level_badge")
def level_badge(level):
    """Devuelve un badge estilizado para el nivel."""
    try:
        lvl = int(level)
    except (ValueError, TypeError):
        lvl = 0
    # Color mapping básico
    if lvl < 5:
        classes = "bg-blue-100 text-blue-700"
    elif lvl < 10:
        classes = "bg-indigo-100 text-indigo-700"
    else:
        classes = "bg-purple-100 text-purple-700"
    return format_html(
        '<span class="badge-level inline-flex items-center px-2 py-0.5 rounded text-xs font-medium {}">Nivel {}</span>',
        classes,
        lvl,
    )
