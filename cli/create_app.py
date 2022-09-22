import os
import errno
import shutil
from cli.utils import in_path, empty_directory


def _copy_project_template(
	project_path: str, template_name: str = "default"
) -> None:
	cli_path = os.path.dirname(__file__)
	
	with in_path(cli_path) as path:
		template_source = os.path.join(path, "project_templates", template_name)
		
		for f in os.listdir(template_source):
			p = os.path.join(template_source, f)
			
			try:
				shutil.copytree(p, os.path.join(project_path, f))
			except OSError as exc:
				if exc.errno in (errno.ENOTDIR, errno.EINVAL):
					shutil.copy(p, os.path.join(project_path, f))
				else:
					raise
	
	with in_path(os.path.join(cli_path, "..")) as path:
		shutil.copytree(
			"pyfyre",
			os.path.join(project_path, "public", "pyfyre")
		)
		shutil.copytree("pyfyre", os.path.join(project_path, "src", "pyfyre"))


def create_app(app_name: str, app_dir: str) -> None:
	print(f"Creating your PyFyre project '{app_name}'...")
	
	project_path = os.path.join(app_dir, app_name)
	
	if os.path.isdir(project_path):
		prompt = input(
			f"Project '{app_name}' already exists. Want to overwrite "
			f"the directory? (y or n): "
		).lower()
		
		if prompt == "y":
			empty_directory(project_path)
		else:
			print("Aborting...")
			return
	
	_copy_project_template(project_path)
	print("Project created successfully.")