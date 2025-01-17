import typing as t

import pdfkit
from django.conf import settings
from django.template import Template
from django.template.loader import get_template
from markdown_it import MarkdownIt
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.front_matter import front_matter_plugin
from weasyprint import HTML

from core.services import BaseService


class MarkdownToPDFConverter:
    def __init__(self, text: str) -> None:
        self.text = text
        self.md = MarkdownIt("commonmark", {"html": True}).use(front_matter_plugin).use(footnote_plugin)

    @staticmethod
    def get_base_styles() -> str:
        return """
        <style type="text/css">
            body {
                font-family: 'Arial Cyr';
                font-size: 14px;
                line-height: 1.5;
            }
        </style>
    """

    def convert_markdown_to_html(self) -> str:
        return self.md.render(self.text)

    def create_html_bytes(self) -> bytes:
        return pdfkit.from_string(
            self.get_base_styles() + self.convert_markdown_to_html(),
            options={"enable-local-file-access": None, "encoding": "UTF-8"},
        )


class HTMLToPDFExporter(BaseService):
    def __init__(self, template_name: str, context: t.Any, **kwargs: t.Any) -> None:
        self.template = self.get_template(template_name)
        self.context = self.get_context(context=context, additional_context=kwargs)

    def act(self) -> bytes:
        html = self.render_html()
        return self.export_pdf(html)

    @staticmethod
    def get_template(template_name: str) -> Template:
        return get_template(template_name)  # type: ignore[return-value]

    @staticmethod
    def get_context(context: t.Any, additional_context: dict) -> dict:
        ctx = vars(context) if hasattr(context, "__dict__") else context

        return {
            **ctx,
            **additional_context,
            "service_name": settings.SERVICE_NAME,
        }

    def add_title_to_context_if_required(self) -> None:
        if "title" not in self.context:
            self.context["title"] = settings.ABSOLUTE_HOST

    def render_html(self) -> str:
        return self.template.render(self.context)

    @staticmethod
    def export_pdf(html: str) -> bytes:
        return HTML(string=html).write_pdf()
