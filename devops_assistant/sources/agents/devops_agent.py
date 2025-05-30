from jinja2 import Environment, FileSystemLoader

class DevOpsAgent:
    """
    Composite agent for various DevOps tasks: Docker, Kubernetes, Ansible, CloudFormation, Monitoring.
    """
    def __init__(self, template_dir: str = "templates/deployment"):
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def generate_dockerfile(self, base_image: str = "python:3.9-slim", port: int = 8000) -> str:
        # Uses base_dockerfile.j2
        template = self.env.get_template("base_dockerfile.j2")
        return template.render(image=base_image, port=port)

    def generate_k8s_deployment(self, name: str, image: str, port: int = 8000) -> str:
        # Uses base_k8s.j2
        template = self.env.get_template("base_k8s.j2")
        return template.render(name=name, image=image, port=port)

    def generate_ansible_playbook(self) -> str:
        template = self.env.get_template("playbook.j2")
        return template.render()

    def generate_cloudformation(self, stack_name: str, resources: list) -> str:
        # Stub: load CloudFormation template and inject resources
        cf_template = {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Description": f"CloudFormation template for {stack_name}",
            "Resources": {r['name']: r['definition'] for r in resources}
        }
        import json
        return json.dumps(cf_template, indent=2)

    def generate_monitoring_config(self, system: str, metrics: list) -> str:
        # Example: generate Prometheus scrape config
        if system.lower() == 'prometheus':
            jobs = []
            for m in metrics:
                jobs.append({
                    'job_name': m['job_name'],
                    'static_configs': [{'targets': m['targets']}]
                })
            config = {'scrape_configs': jobs}
            import yaml
            return yaml.dump(config)
        else:
            raise ValueError(f"Unsupported monitoring system: {system}")
