from O365 import FileSystemTokenBackend
token_backend = FileSystemTokenBackend(token_path='token', token_filename='my_token.txt')