#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License (the "License").
# You may not use this file except in compliance with the License.
#
# You can obtain a copy of the License in the included LICENSE.txt
# or http://opensource.org/licenses/CDDL-1.0
# See the License for the specific language governing permissions
# and limitations under the License.
#
# When modifying Covered Code, update the affected files' copyright
# notice with the current year and add your name to its contributors
# list.
#
# Copyright 2012-2013 Clubhouse Contributors
#
# File contributors: David Arnold
#
from django import template
from django.conf import settings
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(is_safe=True)
def markdown(value, arg=''):
    """
    Runs Markdown over a given value.

    Syntax::

        {{ value|markdown: }}
    """
    try:
        import markdown
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError("Error in 'markdown' filter: The Python markdown library isn't installed.")
        return force_unicode(value)
    else:
        python_markdown_deprecation = "Error in 'markdown' filter: An outdated (< 2.1) version of the Python markdown library is installed."
        # markdown.version was first added in 1.6b
        if hasattr(markdown, 'version'):
            extensions = ['nl2br', 'tables', 'urlize']
            safe_mode = 'escape'
            output_format = 'xhtml5'
            markdown_vers = getattr(markdown, "version_info", None)
            if markdown_vers >= (2,1):
                    return mark_safe(markdown.markdown(force_unicode(value), extensions=extensions, safe_mode=safe_mode, output_format=output_format))
            else:
                if settings.DEBUG:
                    raise template.TemplateSyntaxError(python_markdown_deprecation)
                return force_unicode(value)
        else:
            if settings.DEBUG:
                raise template.TemplateSyntaxError(python_markdown_deprecation)
            return force_unicode(value)
