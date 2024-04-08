import os
from .utils import list_files_in_folder
from .renderer.jinja_renderer import JinjaRenderer, create_env_from_path


class TemplateGenerator:
    renderer: JinjaRenderer

    def process_file(self, file, out_folder, context):
        file = file.replace("\\", "/")
        content = self.renderer.render(file, **context)
        rendered_file = os.path.join(out_folder, file)
        rendered_file = self.renderer.render_string(rendered_file, **context)
        os.makedirs(os.path.dirname(rendered_file), exist_ok=True)
        with open(rendered_file, "w") as f:
            f.write(content)

    def create(self, template_dir: str, output_dir: str, context: dict = {}):
        files = list_files_in_folder(template_dir)
        self.renderer = JinjaRenderer(create_env_from_path(template_dir))
        print(files)
        for file in files:
            self.process_file(file, output_dir, context)
        