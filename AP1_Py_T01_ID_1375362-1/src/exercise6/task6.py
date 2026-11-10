import json

def validate(data):
    if not isinstance(data, dict):
        return "Top-level must be a JSON object"

    for name in ("list1", "list2"):
        if name not in data:
            return f'Missing "{name}"'
        lst = data[name]
        if not isinstance(lst, list):
            return f'"{name}" must be a list'

        prev_year = None
        for i, item in enumerate(lst):
            if not isinstance(item, dict):
                return f'"{name}"[{i}] must be an object'
            if "title" not in item:
                return f'"{name}"[{i}] missing "title"'
            if "year" not in item:
                return f'"{name}"[{i}] missing "year"'
            if not isinstance(item["year"], int):
                return f'"{name}"[{i}]["year"] must be an integer'
            if prev_year is not None and item["year"] < prev_year:
                return f'"{name}" is not sorted by "year"'
            prev_year = item["year"]

    return None

def merge_sorted(list1, list2, key):
    result = []
    i = j = 0
    while i < len(list1) and j < len(list2):
        if list1[i][key] <= list2[j][key]:
            result.append(list1[i])
            i += 1
        else:
            result.append(list2[j])
            j += 1

    result.extend(list1[i:])
    result.extend(list2[j:])
    return result


def main() -> None:
    try:
        with open("input.txt") as file:
            content = file.read().strip()
    except FileNotFoundError:
        print("File not found")
        return
    
    if not content:
        print("Empty file")
        return

    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Not valid JSON: {e}")
        return

    error = validate(data)
    if error:
        print(f"Invalid input: {error}")
        return

    merged = merge_sorted(data["list1"], data["list2"], "year")
    output = {"list0":merged}
    print(json.dumps(output, indent=2, ensure_ascii=False))

    

if __name__ == "__main__":
    main()