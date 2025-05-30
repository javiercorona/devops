# sources/agents/terraform_agent.py

from jinja2 import Environment, FileSystemLoader

class TerraformAgent:
    def __init__(self, template_dir: str = "templates/scripts/terraform"):
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def generate_infrastructure(self, req) -> str:
        """
        Render Terraform code based on provider and resource definitions.
        req.provider: str, e.g. 'aws'
        req.resources: List[ResourceDefinition]
        """
        # Turn Pydantic models into plain dicts
        resources = [r.dict() for r in req.resources]

        template = self.env.get_template(f"{req.provider}_main.tf.j2")
        return template.render(resources=resources)
