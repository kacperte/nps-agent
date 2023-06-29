import jinja2


class Message:
    def __init__(self, template_file, template_path="./"):
        """
        Initialize a new instance of the Message class.

        Args:
            template_file (str): The name of the template file.
            template_path (str, optional): The path to the directory containing the template file. Defaults to "./".

        Raises:
            jinja2.TemplateNotFound: If the template file does not exist.
        """
        # Create a loader for the template files
        template_loader = jinja2.FileSystemLoader(searchpath=template_path)

        # Create a new Jinja2 environment with autoescaping enabled
        self.template_env = jinja2.Environment(loader=template_loader, autoescape=True)

        try:
            # Load the template
            self.template = self.template_env.get_template(template_file)
        except jinja2.TemplateNotFound:
            print(f"Template {template_file} not found.")

    def render(self, **kwargs):
        """
        Render the template with the given variables.

        Args:
            **kwargs: The variables to use when rendering the template.

        Returns:
            str: The rendered template.
        """
        # Render the template with the given variables
        return self.template.render(**kwargs)
