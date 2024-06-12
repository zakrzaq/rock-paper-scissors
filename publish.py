import os
import sys
import subprocess
from dotenv import load_dotenv
from ftplib import FTP
from typing import Literal

load_dotenv()

FTP_HOST = os.getenv("FTP_HOST", "")
FTP_PORT = os.getenv("FTP_PORT", "")
FTP_USER = os.getenv("FTP_USER", "")
FTP_PASSWORD = os.getenv("FTP_PASSWORD", "")
FE_FTP_DIR = "/public_html/games/rpc/"
BE_FTP_DIR = "/backed/rpc/"
SERVICE: Literal["frontend", "backend"] = "frontend"
DEPLOY_BRANCH = "main"

if len(sys.argv) > 1:
    if sys.argv[1] in ["frontend", "backend"]:
        SERVICE = sys.argv[1]


class Server:
    def __init__(self, deploy_branch=DEPLOY_BRANCH):
        self.deploy_branch = deploy_branch

    @staticmethod
    def get_current_branch():
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True,
                check=True,
            )
            branch_name = result.stdout.strip()
            return branch_name
        except subprocess.CalledProcessError as e:
            print(f"❌ An error occurred while getting the current branch: {e}")
            return None

    @staticmethod
    def list_files_omitting_gitignore(repo_path="."):
        try:
            if not os.path.exists(os.path.join(repo_path, ".git")):
                raise Exception(
                    f"❌ The directory '{repo_path}' is not a Git repository."
                )

            result = subprocess.run(
                [
                    "git",
                    "ls-files",
                    "--others",
                    "--exclude-standard",
                    "--cached",
                    "--full-name",
                ],
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=True,
            )

            file_paths = result.stdout.splitlines()
            return file_paths

        except subprocess.CalledProcessError as e:
            print(f"❌ An error occurred while listing files: {e}")
            return None
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            return None

    @staticmethod
    def create_upload_list(input: list[str], repo: Literal["frontend", "backend"]):
        if repo == "frontend":
            file_list = []
            for root, dirs, files in os.walk("./frontend/dist"):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_list.append(file_path)
            return [x for x in file_list]
        if repo == "backend":
            return [x for x in input if "frontend" not in x]

    def upload(self):
        file_list = self.list_files_omitting_gitignore()
        branch_name = self.get_current_branch()
        if self.get_current_branch() == DEPLOY_BRANCH and file_list:
            upload_list = self.create_upload_list(file_list, SERVICE)

            FTP_DIR = BE_FTP_DIR if SERVICE == "backend" else FE_FTP_DIR
            print(FTP_DIR)

            with FTP(FTP_HOST, FTP_USER, FTP_PASSWORD) as ftp:
                for f in upload_list:
                    # print(f"{FTP_DIR}{f.replace("./frontend/dist/", "")}")
                    with open(f, "rb") as file:
                        if file:
                            ftp.storbinary(
                                f"STOR {FTP_DIR}{f.replace("./frontend/dist/", "")}",
                                file,
                            )
                            print(f"UPLOADED: {f}")
                ftp.quit()
        else:
            print(f"❌ Current branch: {branch_name}\nIt should be {DEPLOY_BRANCH}")
            exit(1)


if __name__ == "__main__":
    server = Server()
    server.upload()
