from jinja2 import Environment, FileSystemLoader, select_autoescape
from .interface import IRenderer

class JinjaRenderer(IRenderer):

    def __init__(self, env: Environment):
        self.env = env

    def render(self, template_path, **kwargs) -> str:
        template = self.env.get_template(template_path)
        return template.render(**kwargs)
    
    def render_string(self, template_string, **kwargs) -> str:
        template = self.env.from_string(template_string)
        return template.render(**kwargs)
    
    def exits_template(self, template_path) -> bool:
        return template_path in self.env.list_templates()
    
def create_env_from_path(path: str) -> Environment:
    return Environment(
        loader=FileSystemLoader(path),
        autoescape=select_autoescape()
    )