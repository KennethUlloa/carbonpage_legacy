import os
from .utils import list_files_in_folder
from .renderer.jinja_renderer import JinjaRenderer, create_env_from_path


class TemplateGenerator:
    renderer: JinjaRenderer

    def __init__(self, template_root: str = ""):
        self.template_root = template_root

    def process_file(self, template_dir, file, out_folder, context):
        file = file.replace("\\", "/")
        template_file = file
        if self.template_root:
            template_file = os.path.join(template_dir, file).replace("\\", "/")
        content = self.renderer.render(template_file, **context)
        rendered_file = os.path.join(out_folder, file)
        rendered_file = self.renderer.render_string(rendered_file, **context)
        os.makedirs(os.path.dirname(rendered_file), exist_ok=True)
        with open(rendered_file, "w") as f:
            print(f"Writing to {rendered_file}")
            f.write(content)

    def create(self, template_dir: str, output_dir: str, context: dict = {}):
        template_dir = os.path.join(self.template_root, template_dir)
        template_dir = template_dir.replace("\\", "/")
        template_dir = template_dir.removeprefix("/")
        files = list_files_in_folder(template_dir)
        self.__load_renderer(template_dir)
        template_dir = template_dir.removeprefix(self.template_root + "/")
        for file in files:
            if file.endswith(".omit"):
                continue
            self.process_file(template_dir, file, output_dir, context)
    
    def __load_renderer(self, template_dir: str):
        if not self.template_root:
            self.renderer = JinjaRenderer(create_env_from_path(template_dir))
        else:
            self.renderer = JinjaRenderer(create_env_from_path(self.template_root))