## Configuration options for the application.

# Secret Key for github verification, do not share this
SECRET_KEY = b'12345'

LOG_FILE_LOCATION = '/app/log.txt'

# Dictionary mapping of repo names and github repo urls.
# The names are used to pull the initial repos to the defined LOCAL_REPOS directory
REPOS = {
    'test-repo': {
        'url': r'https://github.com/alexgQQ/test-repo.git',
        'default-branch': 'test-branch',
    }
}
