from jinja2 import Environment, FileSystemLoader

class TemplateEngine:
    def __init__(self, template_dir: str):
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render(self, template_name: str, **context) -> str:
        template = self.env.get_template(template_name)
        return template.render(**context)