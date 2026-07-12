# Python data analysis project in Linux environment

>[!NOTE]
>This project has been created and tested with **Fedora Linux 43 (Workstation Edition)**.  
>Requirements for this project are basic understanding of Linux operating systems,  
>Python programming and using Python virtual environment. 


## 1. Using this project repository
Create desired project directory from CLI. `~` uses current user's home folder and switch `-p` creates full path to the `[project_directory]` even if some of the directories within the path didn't yet exist.
```sh
mkdir -p ~/non-existing_directory/project_directory
```

Clone the repository. 
```sh
git clone git@github.com:sloul1/python_data_analysis.git
```
>[!WARNING]  
>CHECK BETWEEN THESE LINES!!
  
>[!CAUTION]    
>If you have multiple ssh keys configured in `~/.ssh/config` file with different `IdentityFile` options,  
>use the corresponding option by changing the default `Host` after `@` 

```sh
git clone git@sloul1:sloul1/python_data_analysis.git
```
>[!WARNING]  
>CHECK BETWEEN THESE LINES!!    

>[!TIP]  
>Remember to change your local `user.name` and  
>`user.email`so you can push updates to remote repository.  

## 2. Checking dependencies  
>[!TIP]  
>To run `check_dependencies.sh` script for verifying packages needed for running this project are installed  `chmod +x` command  
```sh
chmod +x check_dependencies.sh
```
might be needed to make script executable before running it below.
```sh
./check_dependencies
```

## 3. Example of creating virtual environment for the project

The syntax for creating new Python virtual environment  `python3 -m venv /path/to/new/virtual/environment`. The command below creates virtual environment called `myenv`.   
```sh
python3 -m venv myenv
```
With command above the `myenv` environment is created in the current directory and this can be confirmed by listing directories.  
```sh
ls -al
```  
Directory listing below contains `myenv` directory.
```sh
total 8
drwxr-xr-x. 1 pepper pepper   78 12. 7. 23:26 .
drwxr-xr-x. 1 pepper pepper   40 12. 7. 23:05 ..
-rw-r--r--. 1 pepper pepper  747 12. 7. 23:05 check_dependencies.sh
drwxr-xr-x. 1 pepper pepper  150 12. 7. 23:14 .git
drwxr-xr-x. 1 pepper pepper   76 12. 7. 23:26 myenv
-rw-r--r--. 1 pepper pepper 2091 12. 7. 23:25 README.md
```  
This newly created environment **has to be activated to work in it**.  
```sh 
source myenv/bin/activate   
```
`(myenv)` in front of your CLI's user and hostname indicates that the virtual environment is active   
```sh 
(myenv) pepper@fedora:~/python_data_analysis$   
```  
After you are finished with working in the virtual environment it can be deactivated using `deactivate` commmand.  
```sh
deactivate
```
More info on python virtual environment at developer's site [venv](https://docs.python.org/3.14/library/venv.html).