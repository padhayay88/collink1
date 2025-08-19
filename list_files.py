import os

def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

if __name__ == '__main__':
    print("Project directory structure:")
    list_files('.')
    
    # Check if data directory exists
    print("\nChecking data directory:")
    if os.path.exists('data'):
        print("Data directory exists.")
        print("\nContents of data directory:")
        try:
            for item in os.listdir('data'):
                print(f"- {item}")
        except Exception as e:
            print(f"Error listing data directory: {e}")
    else:
        print("Data directory does not exist!")
