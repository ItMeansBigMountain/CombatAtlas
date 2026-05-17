import json
import yaml
import os

def yaml_to_json(file_path):
    with open(file_path, 'r') as yaml_file:
        yaml_content = yaml.safe_load(yaml_file)
    return json.dumps(yaml_content, indent=2)

def json_to_yaml(file_path):
    with open(file_path, 'r') as json_file:
        json_content = json.load(json_file)
    return yaml.dump(json_content)

def main():
    
    choice = input("Convert file from YAML to JSON (1) or JSON to YAML (2)? Enter 1 or 2: ")
    file_name = "ChatGPT-Schema"

    if choice == '1':
        file_path = f"{file_name}.yaml"
        if os.path.exists(file_path):
            converted_content = yaml_to_json(file_path)
            print("Converted YAML to JSON:\n", converted_content)
            with open("ChatGPT-Schema.json", "a") as f:
                f.write(converted_content)
        else:
            print("YAML file not found.")
    elif choice == '2':
        file_path = f"{file_name}.json"
        if os.path.exists(file_path):
            converted_content = json_to_yaml(file_path)
            print("Converted JSON to YAML:\n", converted_content)
            with open("ChatGPT-Schema.yml", "a") as f:
                f.write(converted_content)
        else:
            print("JSON file not found.")
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
