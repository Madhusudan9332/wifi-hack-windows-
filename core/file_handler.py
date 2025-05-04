
class FileHandler:
    def validate_file(self, file_path):
        return file_path.endswith('.txt') or file_path.endswith('.xml')
