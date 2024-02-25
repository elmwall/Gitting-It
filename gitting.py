# Import required modules
import subprocess
import sys
import os
print("\nDirectories:")
import branchDir as bDir

print("\n\n------------------ INITIATE GITTING ------------------\n")

# FUNCTIONS

# Define function for running git commands.
def runGit(command):
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {e}")
        return None

# Check current branches for selection
def branches():
    git_branch = runGit(["git", "branch"])  # Run git command
    git_branchList = git_branch.splitlines()    # Creates a list of the branches by splitting at linebreak
    git_branchList.reverse()    # Reverses the list to get main first
    return git_branchList   # Return value for future reference, other variables are discarded

# Check and return information from 'git_status'
def status():
    git_status = runGit(["git", "status"])  # Run git command
    return git_status   # Return value for future reference, other variables are discarded

# Analyze status of current branches. Has information sometimes not included in 'git status' needed to check if commit is pending push.
def upstream(branch):
    currentAhead = str()
    git_branchList.clear()  # Empty previous entries in list to avoid errors
    git_upstream = runGit(["git", "branch", "-vv"]) # Run git command
    git_upstreamList = git_upstream.splitlines()    # Creates a list of the branches by splitting at linebreak
    git_upstreamList.reverse()  # Reverses the list to get main first

    branchOverview = dict() # Create dictionary, where values can be easily collected
    branchOverview.clear()
    for x in git_upstreamList:
        if branch in x:
            branchOverview.update({"Current": x})
            if "ahead" in x:
                currentAhead = "Yes"
            else:
                currentAhead = "No"
        else:
            branchOverview.update({"Non-active": x})
    
    print("\nMESSAGE\n" + "From command 'git upstream':")
    for x, y in branchOverview.items():
        print(x, y)

    return currentAhead

# Pulling command. Process + output message included. No output required.
def pull(branch):
    print("\n- PULLING")
    git_pull = runGit(["git", "pull", "origin", branch])
    print("\nMESSAGE\n" + "From command 'git pull':\n" + git_pull)

# Adding command. Process message included. No output required.
def add(target):
    print("\n- ADDING CHANGES")
    if os.path.exists(toAdd):
        runGit(["git", "add", target])
    else:
        print("Invalid path or file. Git add not executed. \nExiting program.")
        sys.exit()

# Commit command. Process message included. 
def commit(name):
    print("\n- COMMITTING CHANGES")
    git_commit = runGit(["git", "commit", "-m", name])
    try:    # Sometimes 'git_commit' gives no output, despite there being a commit pending. Output message kept under "try" to avoid error.
        print("\nMESSAGE\n" + "From command 'git commit':\n" + git_commit)
    except:
        print("No output from 'git commit'. Verify that there are changes to commit or other issues.")


def push(branch):
    git_push = runGit(["git", "push", "origin", branch])
    try:    # Sometimes 'git_push' gives no output. Output message kept under "try" to avoid error.
        print("\nMESSAGE\n" + "From command 'git push':\n" + git_push)
    except:
        print("Push not performed. Verify that there are changes to push or other issues.")


# Print a line of dashes for structuring of output
def line():
    print("------------------------------------------------------")

# Call to exit the program
def exitGitting():
    print("\n------------------ GITTING EXITED ------------------\n\n")
    sys.exit()



# ANALYSIS OF EXISTING BRANCHES and SELECTION OF BRANCH TO WORK WITH
print("Current branches in repository:")
git_branchList = branches()
# print(len(git_branchList))
for x in git_branchList:    # Listing branches in terminal
    a = git_branchList.index(x)
    if "*" in x:
        print(str(a) + ":", git_branchList[a], "CURRENT")   # Label active branch
    else:
        print(str(a) + ":", git_branchList[a])

try:
    branchCue = git_branchList[int(input("Select branch index: "))]     # Select branch to work with 
except:
    print("Error collecting list of branches.")
    exitGitting()   # Call exit function to end program

if branchCue in git_branchList:     # Affirmative message
    print(branchCue, "selected")
else:
    exitGitting()

try:
    git_branchSwitch = runGit(["git", "checkout", branchCue])   # Perform switch
    print("\nMESSAGE\n" + "From command 'git checkout' " + branchCue + ":\n" + git_branchSwitch + "\n\n")
except:
    print("Switch not performed. There could be changes to commit in current branch before switch can be performed.")
line()



# INPUT SECTION: Selection of program, for whether to perform step-by-step or automated cycles.
print('INFORMATION:\n- Gitting can perform pre-set programs for \n  synchronizing with your Git repository.\n- Git messages are checked and printed for every step \n  and after completion if verification or \n  troubleshooting is needed.\n- If you want to select the precise actions and \n  verify git status, select the stepwise program ("1").\n- If you are confident about the changes \n  you can use an automated cycle.\n- Program "2" performs steps: add, commit, and push. \n  Program "3" also does a pull beforehand. \n  These require manual naming of the commit.\n- In a hurry? Use "4" for a quick program, \n  it will be named "Quick commit". \n  Automated cycles runs through add, commit, and push \n  of the branch without checking for errors, \n  but final status is returned. \n\nThe git commands run by this script include: \n- status\n- branch -vv\n- pull\n- add.\n- commit -m "[name]"\n- push\n\n')

actionCue = input("Select procedure for synchronizing Git:\n\n   PROGRAM                  NAMING\n  ---------------------------------------------------------\n   1) Stepwise procedure    manual selections step-by-step\n   2) Add-to-push           manual naming\n   3) Full pull'n'push      manual naming\n   4) QUICK PROGRAM         fully automatic\n   Exit: any other key\n   Selection:")
print()


if "*" in branchCue:
    branchCue = branchCue[2:]
if "main" in branchCue or "master" in branchCue:
    toAdd = "."
else:
    toAdd = bDir.branchDict[branchCue]



# Response for Full pull'n'push (3): initial push.
if actionCue == "3":
    pull(branchCue)     # Call pull function for specified branch


# Response program for automated cycles (2, 3, and 4).
automatedAction = ("2", "3", "4")  # List of accepted selection input for program.
if actionCue in automatedAction:
    add(toAdd)  # Call add function for specified directory
    if actionCue == "4":
        commitName = "Quick commit"         # Automated naming of commit for quick program (4).
    else:
        commitName = input("Name commit: ")     # INPUT SECTION: Manual naming (1-3).
    commit(commitName)
    push(branchCue)     # Call push function for specified branch
    print("\n- SYSTEM STATUS")
    git_status = status()   # Call status function, collect info
    print("\nMESSAGE\n" + "From command 'git status':\n" + git_status)
    upstream(branchCue)  # Call upstream function for specified branch, prints info
    print("\nDONE")
    exitGitting()
elif actionCue == "1":  # Response for stepwise procedure (1), i.e. skip cycle.
    pass
else:   # Response for invalid entry.
    exitGitting()
line()


# Response steps for stepwise procedure (1).
# Pull
pullCue = input("Execute pull?\n   1) Yes\n   2) No\n   Else) Exit\n   Selection:")     # INPUT SECTION: do or don't perform "pull".
if pullCue == "1":      # Affirmative input for pull
    pull(branchCue)     # Call pull function for specified branch
    git_status = status()   # Call status function, collect info
elif pullCue == "2":    # Negative input for pull
    print("Pull not performed.")
else:
    exitGitting()
line()
git_status = status()


# Add
if "Untracked files" in git_status or "Changes not staged for commit" in git_status:
    print("Untracked or changed files: Yes\n")
    print("FILE DETAILS:")
    print("\nMESSAGE\n" + "From command 'git status':\n" + git_status + "\n")
    addCue = input("Add changes?\n   1) Yes\n   2) No\n   Else) Exit\n   Selection:")   # INPUT SECTION: do or don't perform "add".
    if addCue == "1":
        pathCue = input("\nDirectory or file selection:\n   1) Add all in main or branch directory\n   2) Manual input of directory, file, or file path\n   Else) Exit\n   Selection:")
        if pathCue == "2":
            toAdd = input("\nSpecify path in either of specified formats: \n   file.extension               (for file in main folder of git repository) \n   subfolder\\                   (for complete folder under main folder) \n   subfolder\\file.extension     (for file within folder under main folder) \nPath:")
            toAdd = toAdd.replace("\\", "/")
            print("Path confirmed:", toAdd)
        elif pathCue == "1":
            pass
        else:
            exitGitting()
        print("check3")
        add(toAdd)
        print("check4")
        line()
    elif addCue == "2":
        print("Changes not added.")
    else:
        exitGitting()
else:
    print("Untracked or changed files: No")
git_status = status()


# Commit
if "Changes to be committed" in git_status:
    print("Non-committed changes: Yes\n")
    print("ADDED CHANGES:")
    print("\nMESSAGE\n" + "From command 'git status':\n" + git_status, "\n")
    commitCue = input("Commit changes?\n   1) Yes\n   2) No\n   Else) Exit\n   Selection:")     # INPUT SECTION: do or don't perform "commit".
    if commitCue == "1":
        commitName = input("Name commit: ")                                                     # INPUT SECTION: Manual naming.
        commit(commitName)
        line()
    elif commitCue == "2":
        print("Changes not committed.")
    else:
        exitGitting()
else:
    print("Non-committed changes: No")
git_status = status()


# Push
currentAhead = upstream(branchCue)
if currentAhead == "Yes":
    print("Files to push: Yes\n")
    print("COMMITTED CHANGES:")
    print("\nMESSAGE\n" + "From command 'git status':\n" + git_status, "\n")
    pushCue = input("Push files?\n   1) Yes\n   2) No\n   Else) Exit\n   Selection:")       # INPUT SECTION: do or don't perform "push".
    if pushCue == "1":
        push(branchCue)
        line()
    elif pushCue == "2":
        print("Files not pushed.")
    else:
        exitGitting()
else:
    print("Files to push: No\n")


# Final status check
git_status = status()   # Call status function, collect info
print("\nMESSAGE\n" + "From command 'git status':\n" + git_status + "\n")
upstream(branchCue)     # Call upstream function for specified branch, prints info
print("DONE")
print("\n------------------ END GITTING ------------------\n\n")
