import os
import re
import subprocess
import sys
import venv

# -------------------- You can customize the settings bellow --------------------

# You can customize the 'dependencies' dict:
# the key is the dependency to be installed, value is the label that will be added in 'INSTALLED_APPS'
dependencies = {
    'django': None,
    # 'django_managepy_anywhere': None,
    # 'requests': None,
    # 'pipreqs': None,
    # 'python-dotenv': None,
    # 'django_extensions': 'django_extensions',
    # 'django_crispy_forms': 'crispy_forms',
    # 'django_debug_toolbar': 'debug_toolbar',
    # 'django_rosetta': 'rosetta',
    # 'django_taggit': 'taggit',
    # 'markdown': 'markdown',
    # 'psycopg2': 'django.contrib.postgres'
}

# You can customize the 'project_folders' tuple:
project_folders = (
    'media',  # A single folder
    ('templates', 'static'),  # A parent directory, a child directory, so on and so forth
)

# You can customize the 'app_folders' tuple as described above.
app_folders = (
    ('management', 'commands'),
    ('static', 'css'),
)

# -------------------- You can customize the settings above --------------------


current_dir = os.path.basename(os.getcwd())
project_question = f"\n\tName your Django project to be created in '{current_dir}' folder ('exit' to quit): "
app_question = f"\n\tName your app ('exit' to quit): "


def get_folder_name(parameter):  # Used twice to get project and app names
    while True:
        try:
            new_folder = input(f"{parameter}").strip().replace(' ', '_')
            if new_folder.lower() == 'exit':
                print('\n\tPython interpreter terminated.')
                break
            elif not new_folder:
                raise ValueError('\n\tYou must type a name,')
            elif os.path.isdir(new_folder):
                raise ValueError(f"\n\tA folder called '{new_folder}' already exists,")
            else:
                return new_folder
        except ValueError as e:
            print(f'{e} please try again.')


def run_django_cmd(cmd, step):
    try:
        print(step)
        subprocess.run(cmd, shell=True, check=True, cwd=project) # setting current dir where cmds will be run
    except subprocess.CalledProcessError as e:
        print(f"\n\tsubprocess.CalledProcessError returned this error: \n\t{e}")
    except ValueError as e:
        print(f'{e} please try again.')


# paths for subprocess cmds
project = get_folder_name(parameter=project_question)
venv_path = os.path.join(project, '.venv')
python = '.venv/bin/python'
django_admin = '.venv/bin/django-admin'


# Creating venv
def create_venv():
    builder = venv.EnvBuilder(system_site_packages=False, symlinks=True, with_pip=True)
    builder.create(venv_path)


# upgrading pip
def upgrade_pip():
    whats_happening = f'\n\tUpgrading pip to the latest version...'
    cmd = f'{python} -m pip install --upgrade pip --quiet'
    run_django_cmd(cmd, step=whats_happening)


def install_dependencies():
    try:
        if not dependencies:
            raise Exception('There are no dependencies to be installed,')
        elif len(dependencies) > 1:
            which_dependencies = list(dependencies.keys())
            first_dependency = which_dependencies[0]
            whats_happening = f'\n\tCollecting {first_dependency}...'
            line_start = len(whats_happening) - len(first_dependency)
            all_others = which_dependencies[1:]
            print(whats_happening)
            for _ in all_others:
                whats_happening = f"{''.ljust(line_start)}{_}..."
                cmd = f'{python} -m pip install {_} --quiet'
                run_django_cmd(cmd, step=whats_happening)
        else:
            for _ in dependencies:
                whats_happening = f'\n\tCollecting {_}...'
                cmd = f'{python} -m pip install {_} --quiet'
                run_django_cmd(cmd, step=whats_happening)
    except Exception as e:
        print(f'\t{e}')
        sys.exit()


def create_project():
    whats_happening = f"\n\tCreating your Django project '{project}' structure..."
    cmd = f'{django_admin} startproject core .'
    run_django_cmd(cmd, step=whats_happening)


app = get_folder_name(parameter=app_question)


def create_app():
    whats_happening = f"\n\tCreating your app '{app}' structure..."
    cmd = f'{python} manage.py startapp {app}'
    run_django_cmd(cmd, step=whats_happening)


def create_extra_folders():
    project_str = f"\n\tFolders created in project '{project}':"
    print(project_str)
    project_str_start = len(project_str)
    for _ in project_folders:
        if isinstance(_, tuple):
            folder = os.path.join(project, '/'.join(_), app)
            os.makedirs(folder)
            print(f"{''.ljust(project_str_start)}'{'/'.join(_)}/{app}'")
        else:
            folder = os.path.join(project, _, app)
            os.makedirs(folder)
            print(f"{''.ljust(project_str_start)}'{_}/{app}'")

    app_str = f"\n\tFolders created in app '{app}':"
    print(app_str)
    app_str_start = len(app_str)
    for _ in app_folders:
        if isinstance(_, tuple):
            folder = os.path.join(project, app, '/'.join(_))
            os.makedirs(folder)
            print(f"{''.ljust(app_str_start)}'{'/'.join(_)}'")
        else:
            folder = os.path.join(project, app, '/'.join(_))
            os.makedirs(folder)
            print(f"{''.ljust(app_str_start)}'{_}'")


def django_migrate():
    whats_happening = f"\n\tApplying initial database migrations to '{project}' database..."
    cmd = f'{python} manage.py migrate -v 0' # 0 means 'No output at all'
    run_django_cmd(cmd, step=whats_happening)


def update_settings():
    try:
        settings_path = os.path.join(project, 'core', 'settings.py')

        with open(settings_path) as file:
            content = file.read()

            # remove initial multiline string about settings.py
            pattern = re.compile(r'\"\"\".*?\"\"\"\n{1,5}', re.DOTALL)
            content = pattern.sub('', content)

            # insert an import to the 'os' module
            pattern = re.compile('from pathlib import Path\n', re.DOTALL)
            content = pattern.sub('from pathlib import Path\nimport os\n\n', content)

            # insert django_extensions in INSTALLED_APPS
            pattern = re.compile("'django.contrib.staticfiles',\n", re.DOTALL)
            new_string = ("'django.contrib.staticfiles',\n\n"
                          '    # apps:\n')
            new_string += f"    '{app}',\n\n"
            new_string += '    # 3rd party:\n'

            # insert the app(s) name(s) in INSTALLED_APPS
            for _ in dependencies.values():
                if _ is not None:
                    new_string += f"    '{_}',\n"

            content = pattern.sub(new_string, content)

            # insert templates DIR info
            pattern = re.compile(r"'DIRS': \[\],\n", re.DOTALL)
            new = r"'DIRS': [os.path.join(BASE_DIR, 'templates')],\n"
            content = pattern.sub(new, content)

            # change static info and add media info
            new = ("STATIC_URL = '/static/'\n"
                   "STATICFILES_DIRS = (os.path.join(BASE_DIR, 'templates', 'static'),)\n"
                   "STATIC_ROOT = os.path.join('static')\n\n"
                   "MEDIA_ROOT = os.path.join(BASE_DIR, 'media')\n"
                   "MEDIA_URL = '/media/'\n"
                   )
            pattern = re.compile("STATIC_URL = 'static/'\n", re.DOTALL)
            content = pattern.sub(new, content)

        # save the new settings.py file
        with open(settings_path, 'w') as file:
            file.write(content)
        print(f"\n{''.ljust(50)}Your Django project {project} is all set!".upper())

    except Exception as e:
        print(f'{e}')


def create_django_project():
    create_venv()
    upgrade_pip()
    install_dependencies()
    create_project()


def create_django_app():
    create_app()
    create_extra_folders()
    django_migrate()
    update_settings()


if __name__ == '__main__':
    create_django_project()
    create_django_app()

