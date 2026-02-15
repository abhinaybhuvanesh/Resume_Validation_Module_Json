def find_field(data, possible_names):
    if isinstance(data, dict):
        for name in possible_names:
            if name in data:
                return data[name]
        for key, value in data.items():
            result = find_field(value, possible_names)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_field(item, possible_names)
            if result is not None:
                return result
    return None

def extract_candidate_info(data):
    info = {
        "candidate_id": None,
        "name": None,
        "email": None
    }
    id_names = ["candidate_id", "candidateId", "id", "user_id", "userId", "candidateid"]
    name_names = ["name", "full_name", "fullName", "candidate_name", "candidateName", "username"]
    email_names = ["email", "email_id", "emailId", "mail", "e-mail"]

    info["candidate_id"] = find_field(data, id_names) or "unknown"
    info["name"] = find_field(data, name_names) or "unknown"
    info["email"] = find_field(data, email_names) or "unknown"
    return info

def check_json_structure(data):
    info = extract_candidate_info(data)
    return {
        "valid": True,
        "issues": [],
        "extracted_info": info,
        "original_data": data
    }