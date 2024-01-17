import json
import os

def process_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    result = {"total_time": 0, "total_average_time": 0, "groups": {}}
    
    for key in ["0", "1", "2", "3", "4"]:
        total_time = 0
        max_time = float('-inf')

        if key in data:
            entries = data[key]
            if entries:
                for entry in entries:
                    time = entry[-2]
                    total_time += time
                    max_time = max(max_time, time)

                average_time = total_time / len(entries)
            else:
                average_time = 0
        else:
            average_time = 0

        result["groups"][key] = {"total_time": total_time, "average_time": average_time}

    result["total_time"] = sum(entry[-2] for key in data for entry in data[key])
    
    if result["total_time"] > 0:
        result["total_average_time"] = result["total_time"] / sum(len(data[key]) for key in data)
    else:
        result["total_average_time"] = 0

    return result

def main():
    input_directory = '.'  # Change this to the directory where your JSON files are located
    output_directory = '.' # Change this to the directory where you want to save the output files

    for i in range(1, 51):
        file_name = f"summary_falcon_7M_{i}.json"
        input_file_path = os.path.join(input_directory, file_name)

        if os.path.exists(input_file_path):
            result = process_json_file(input_file_path)

            output_file_name = f"output_{i}.json"
            output_file_path = os.path.join(output_directory, output_file_name)

            with open(output_file_path, 'w') as output_file:
                json.dump(result, output_file, indent=2)

if __name__ == "__main__":
    main()
