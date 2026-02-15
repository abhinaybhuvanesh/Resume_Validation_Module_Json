from .structure_checker import check_json_structure, find_field
from .rules import validate_experience, validate_projects, validate_certifications
from .link_validator import validate_all_links

class ResumeValidator:
    def __init__(self):
        pass

    def find_section(self, data, section_names):
        return find_field(data, section_names) or []
    
    def validate(self, input_json):
        structure_result = check_json_structure(input_json)
        info = structure_result["extracted_info"]
        data = structure_result["original_data"]

        experience = self.find_section(data, ["experience", "experiences", "work_experience", "work", "employment"])
        projects = self.find_section(data, ["projects", "project", "portfolio"])
        certifications = self.find_section(data, ["certifications", "certification", "certs", "certificates"])
        sections = {}
        if experience:
            exp_issues = validate_experience(experience)
            sections["experience"] = {
                "status": "PASS" if not exp_issues else "FAIL",
                "issues": exp_issues
            }
        else:
            sections["experience"] = {
                "status": "NOT_FOUND",
                "issues": ["No experience section found"]
            }
        if projects:
            proj_issues = validate_projects(projects)
            sections["projects"] = {
                "status": "PASS" if not proj_issues else "FAIL",
                "issues": proj_issues
            }
        else:
            sections["projects"] = {
                "status": "NOT_FOUND",
                "issues": ["No projects section found"]
            }
        if certifications:
            cert_issues = validate_certifications(certifications)
            sections["certifications"] = {
                "status": "PASS" if not cert_issues else "FAIL",
                "issues": cert_issues
            }
        else:
            sections["certifications"] = {
                "status": "NOT_FOUND",
                "issues": ["No certifications section found"]
            }
        link_issues = validate_all_links(data)
        sections["links"] = {
            "status": "PASS" if not link_issues else "FAIL",
            "issues": link_issues
        }
        return {
            "candidate_id": info["candidate_id"],
            "name": info["name"],
            "email": info["email"],
            "validation_status": "PROCESSED",
            "sections": sections
        }