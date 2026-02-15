from .utils import validate_url
from .structure_checker import find_field

def extract_all_urls(data):
    urls = []
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str) and (value.startswith(('http://', 'https://')) or 'github.com' in value or 'linkedin.com' in value):
                urls.append((key, value))
            else:
                urls.extend(extract_all_urls(value))
    elif isinstance(data, list):
        for item in data:
            urls.extend(extract_all_urls(item))
    return urls

def validate_all_links(data):
    issues = []
    all_urls = extract_all_urls(data) 
    for field_name, url in all_urls:
        if not validate_url(url):
            issues.append(f"Invalid URL in '{field_name}': {url}")

    github = find_field(data, ["github", "github_url", "githubLink", "git"])
    if github and not validate_url(github):
        issues.append(f"Invalid GitHub URL: {github}")
    
    linkedin = find_field(data, ["linkedin", "linkedin_url", "linkedinLink"])
    if linkedin and not validate_url(linkedin):
        issues.append(f"Invalid LinkedIn URL: {linkedin}")
    
    portfolio = find_field(data, ["portfolio", "portfolio_url", "website", "personal_website"])
    if portfolio and not validate_url(portfolio):
        issues.append(f"Invalid portfolio URL: {portfolio}")
        
    return issues