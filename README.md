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
```sh
python -m venv /path/to/new/virtual/environment
```
More info on python virtual environment at developer's site [venv](https://docs.python.org/3.14/library/venv.html).