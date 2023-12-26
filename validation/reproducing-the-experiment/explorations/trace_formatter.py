import json
import os

def transform_json(input_json):
    transformed_json = []

    for item_list in input_json:
        for item in item_list:
            transformed_item = {
                "xpath": item["xpath"],
                "css": item["css"],
                "event": item["event"],
                "info": item["info"]
            }

            transformed_json.append(transformed_item)

    return transformed_json

def process_file(input_path, output_folder):
    input_filename = os.path.basename(input_path)
    output_filename = f"formatted_{input_filename}"
    output_path = os.path.join(output_folder, output_filename)

    print(f"Input path: {input_path}")
    print(f"Output path: {output_path}")

    os.makedirs(output_folder, exist_ok=True)

    with open(input_path, 'r') as file:
        input_data = json.load(file)

    output_data = transform_json(input_data)

    with open(output_path, 'w') as file:
        json.dump(output_data, file, indent=4)

def main():
    input_folder = "."
    output_folder = "formatted_traces"

    input_folder = os.path.abspath(input_folder)

    for i in range(1, 51):
        input_filename = f"exploration_falcon_7M_{i}.json"
        input_path = os.path.join(input_folder, input_filename)
        process_file(input_path, output_folder)


if __name__ == "__main__":
    main()
