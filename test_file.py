print("Testing file operations...")

# Try to create a test file
try:
    with open('test_file.txt', 'w') as f:
        f.write("This is a test file.")
    print("Successfully created test_file.txt")
except Exception as e:
    print(f"Error creating file: {e}")

# List current directory
print("\nCurrent directory contents:")
try:
    import os
    for item in os.listdir('.'):
        print(f"- {item}")
except Exception as e:
    print(f"Error listing directory: {e}")
