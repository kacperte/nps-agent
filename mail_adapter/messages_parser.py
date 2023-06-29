import jinja2


class Message:
    def __init__(self, template_file, template_path="./"):
        template_loader = jinja2.FileSystemLoader(searchpath=template_path)
        self.template_env = jinja2.Environment(loader=template_loader,autoescape=True)
        try:
            self.template = self.template_env.get_template(template_file)
        except jinja2.TemplateNotFound:
            print(f"Template {template_file} not found.")

    def render(self, **kwargs):
        return self.template.render(**kwargs)
