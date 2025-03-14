import base64
import sys

def file_to_base64(file_path):
    try:
        with open(file_path, 'rb') as file:
            file_data = file.read()
            base64_data = base64.b64encode(file_data).decode('utf-8')
            return base64_data
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    base64_data = file_to_base64(file_path)
    if base64_data:
        print("Base64 encoded data:")
        print(base64_data)
