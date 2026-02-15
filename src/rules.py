from .utils import validate_date, calculate_days
from .structure_checker import find_field

def get_field(item, possible_names, default=None):
    if isinstance(item, dict):
        for name in possible_names:
            if name in item:
                return item[name]
    return default

def validate_experience(exp_list):
    issues = []  
    if not exp_list:
        return issues
    for idx, exp in enumerate(exp_list, 1):
        title = get_field(exp, ["title", "job_title", "position", "role", "designation"])
        if not title:
            issues.append(f"Experience {idx}: Missing title/job title")
        elif len(str(title).strip()) < 2:
            issues.append(f"Experience {idx}: Title too short")

        company = get_field(exp, ["company", "employer", "organization", "firm"])
        if not company:
            issues.append(f"Experience {idx}: Missing company name")

        start_date = get_field(exp, ["start_date", "startDate", "from", "start"])
        if not start_date:
            issues.append(f"Experience {idx}: Missing start date")
        elif not validate_date(str(start_date)):
            issues.append(f"Experience {idx}: Invalid start date format")
        
        end_date = get_field(exp, ["end_date", "endDate", "to", "end", "current"])
        if end_date and str(end_date).lower() not in ["present", "current", "now"]:
            if not validate_date(str(end_date)):
                issues.append(f"Experience {idx}: Invalid end date format")
            elif start_date and validate_date(str(start_date)):
                days = calculate_days(str(start_date), str(end_date))
                if days < 1:
                    issues.append(f"Experience {idx}: End date must be after start date")
        
        desc = get_field(exp, ["description", "desc", "details", "responsibilities"])
        if not desc:
            issues.append(f"Experience {idx}: Missing description")
        elif len(str(desc).strip()) < 10:
            issues.append(f"Experience {idx}: Description too short")
    return issues

def validate_projects(proj_list):
    issues = []
    if not proj_list:
        return issues
    for idx, proj in enumerate(proj_list, 1):
        title = get_field(proj, ["title", "name", "project_name", "projectName"])
        if not title:
            issues.append(f"Project {idx}: Missing title")

        desc = get_field(proj, ["description", "desc", "details", "overview"])
        if not desc:
            issues.append(f"Project {idx}: Missing description")
        elif len(str(desc).strip()) < 10:
            issues.append(f"Project {idx}: Description too short")

        tech = get_field(proj, ["technologies", "tech", "tech_stack", "techStack", "tools"])
        if not tech:
            issues.append(f"Project {idx}: Missing technologies")
        elif isinstance(tech, (list, tuple)) and len(tech) == 0:
            issues.append(f"Project {idx}: No technologies listed")
    
    return issues

def validate_certifications(cert_list):
    issues = []
    if not cert_list:
        return issues    
    for idx, cert in enumerate(cert_list, 1):
        name = get_field(cert, ["name", "cert_name", "certification_name", "title"])
        if not name:
            issues.append(f"Certification {idx}: Missing name")
        issuer = get_field(cert, ["issuer", "issued_by", "issuing_organization", "organization"])
        if not issuer:
            issues.append(f"Certification {idx}: Missing issuer")
        
        url = get_field(cert, ["verification_url", "verify_url", "credential_url", "url", "link"])
        if url:
            from .utils import validate_url
            if not validate_url(str(url)):
                issues.append(f"Certification {idx}: Invalid verification URL")
                
    return issues