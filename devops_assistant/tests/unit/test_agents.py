import pytest
from sources.agents.terraform_agent import TerraformAgent
from sources.agents.cicd_agent import CICDAgent

@pytest.fixture
def terraform_agent():
    return TerraformAgent()

@pytest.fixture
def cicd_agent():
    return CICDAgent()

def test_terraform_template_exists(terraform_agent):
    # Should load AWS template without error
    code = terraform_agent.generate_infrastructure(type('R', (), {'provider':'aws','resources':[]})())
    assert "provider \"aws\"" in code


def test_cicd_template_loads(cicd_agent):
    from types import SimpleNamespace
    req = SimpleNamespace(platform='github', steps=[{'name':'Test','run':'echo hi'}])
    code = cicd_agent.generate_pipeline(req)
    assert "name: CI" in code