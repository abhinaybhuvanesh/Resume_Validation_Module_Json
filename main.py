import sys
import json
from src.validator import ResumeValidator

def main():
    validator = ResumeValidator()
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            data = json.load(f)
        if isinstance(data, list):
            results = []
            for resume in data:
                results.append(validator.validate(resume))
            print(json.dumps(results, indent=2))
        else:
            print(json.dumps(validator.validate(data), indent=2))
    else:
        data = json.load(sys.stdin)
        if isinstance(data, list):
            results = [validator.validate(r) for r in data]
            print(json.dumps(results, indent=2))
        else:
            print(json.dumps(validator.validate(data), indent=2))
            
if __name__ == "__main__":
    main()