from jinja2 import Environment, FileSystemLoader
from pathlib import Path

class CICDAgent:
    def __init__(self, template_dir: str = "templates/deployment"):
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def generate_pipeline(self, req) -> str:
        """
        Render CI/CD pipeline based on platform and steps list.
        req.platform: 'github' | 'gitlab' | 'jenkins'
        req.steps: list of dicts, each with 'name' and 'run' or 'uses'
        """
        if req.platform == 'github':
            template = self.env.get_template("github_actions.yml.j2")
        elif req.platform == 'gitlab':
            template = self.env.get_template("gitlab_ci.yml.j2")
        elif req.platform == 'jenkins':
            template = self.env.get_template("Jenkinsfile.j2")
        else:
            raise ValueError(f"Unsupported platform: {req.platform}")

        return template.render(steps=req.steps)