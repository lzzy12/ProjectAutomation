import os
import subprocess
import getpass
from github import Github

# installs GitHub module
subprocess.run("pip install PyGithub", shell=True)


# common console colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# global project variables
localPath = "L:/Projects/"
projectName = input("Project name: ")
projectType = input("Project type: ")


# global GitHub credentials
repoName = ""
username = ""
password = ""


# switches the proccess to run based on the type of project
def GetProjectProcess(projectType):
    switcher = {
        'react': f"npx create-react-app {projectName}",
        'blank': f"mkdir {projectName}"
    }
    return switcher.get(projectType, "invalid")


# gets user input to update GitHub credentials
def GetCredentials():
    global repoName
    global username
    global password
    repoName = input("Enter new GitHub repository name: ")
    username = input("Enter your GitHub username: ")
    password = getpass.getpass("Enter your GitHub password: ")


# creates GitHub repo if credentials are valid
def CreateGitHubRepo():
    GetCredentials()
    try:
        user = Github(username, password).get_user()
        user.create_repo(repoName)
        return True
    except Exception as e:
        print(e)
        return False


# loops until project type is valid
while GetProjectProcess(projectType) == "invalid":
    print(bcolors.WARNING + "Invalid project type, please try again." + bcolors.ENDC)
    projectType = input("Project type: ")


# loops until GitHub repo has been created successfully
while CreateGitHubRepo() == False:
    print(bcolors.WARNING +
          "Something went wrong when creating the GitHub repo. See above for more details." + bcolors.ENDC)


# changes into correct directory and runs the project proccess for the declared project type
os.chdir(localPath)
subprocess.run(GetProjectProcess(projectType), shell=True)
os.chdir(projectName)


# git proccesses
subprocess.run("git init", shell=True)
subprocess.run("git add *", shell=True)
subprocess.run("git commit -m 'initial commit'", shell=True)
subprocess.run(
    f"git remote add origin https://github.com/{username}/{repoName}",
    shell=True)
subprocess.run("git push origin master", shell=True)


# opens project in VS code
subprocess.run("code .", shell=True)


# starts dev server for react projects
if projectType == 'react':
    subprocess.run("npm start", shell=True)
