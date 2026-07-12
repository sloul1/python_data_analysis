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
>`user.email` to your own so you can push updates to remote repository.  
```sh
git config user.name "yourusername"
```
```sh
git config user.name "yourusername@email.tld"
```

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
Output:
```sh
✓ python3 is installed.
✓ pip3 is installed.
✓ python3 venv module is installed.
```  

## 3. Example of creating virtual environment for the project

The syntax for creating new Python virtual environment  `python3 -m venv /path/to/new/virtual/environment`. The command below creates virtual environment called `myenv`.   
```sh
python3 -m venv myenv
```  
>[!TIP] 
>With command above the `myenv` environment is created  
>in the current directory and this can be confirmed by  
>listing directories.    
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
This newly **created environment has to be activated to work in it**.  
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

## 4. Install requirements in venv using pip

To run included python srcipt in `venv` the requirements must be installed. There is a text file `requirements.txt` that contains information for the additional package installation. To run installation use the following command.  

```sh
pip install -r requirements.txt
```

Requirements can be uninstalled using command below.  
```sh
pip uninstall -r requirements.txt -y
```  

## 5. Running the python script

After installing dependecies mentioned in `requirements.txt` using `pip` the python script can be ran.  

```sh
python3 nordic_indicators.py
```  

The script fetches data of nordic countries (Finland, Sweden, Norway, Denmark and Iceland) from the [World Bank API](https://documents.worldbank.org/en/publication/documents-reports/api) and saves the data in `nordic_indicators.csv` file.  

>[!NOTE]  
>Note that EUR (€) has existed only from January 1, 1999 as  
>an accounting currency on and physical coins and banknotes  
>entered circulation on January 1, 2002 so the currency used in  
>this project is in USD ($).  

```sh
Downloading data from World Bank API...
Fetching Finland...
Fetching Sweden...
Fetching Norway...
Fetching Denmark...
Fetching Iceland...
Data saved to 'nordic_indicators.csv'
```

Dataset info will be printed:

```sh
Dataset info:
<class 'pandas.DataFrame'>
Index: 330 entries, 198 to 131
Data columns (total 6 columns):
 #   Column              Non-Null Count  Dtype  
---  ------              --------------  -----  
 0   date                330 non-null    int64  
 1   gdp_per_capita_usd  330 non-null    float64
 2   internet_users_pct  176 non-null    float64
 3   population          330 non-null    int64  
 4   country_code        330 non-null    str    
 5   country             330 non-null    str    
dtypes: float64(2), int64(2), str(2)
memory usage: 18.0 KB
None
``` 

Sample data print:  

```sh
Sample data:
     date  gdp_per_capita_usd  internet_users_pct  population country_code  country
198  1960         1389.021394                 NaN     4579603          DNK  Denmark
199  1961         1530.537790                 NaN     4611687          DNK  Denmark
200  1962         1711.218138                 NaN     4647727          DNK  Denmark
201  1963         1807.252792                 NaN     4684483          DNK  Denmark
202  1964         2049.397243                 NaN     4722072          DNK  Denmark
203  1965         2284.228505                 NaN     4759012          DNK  Denmark
204  1966         2487.136271                 NaN     4797381          DNK  Denmark
205  1967         2700.746379                 NaN     4835354          DNK  Denmark
206  1968         2776.135445                 NaN     4864883          DNK  Denmark
207  1969         3151.133243                 NaN     4891860          DNK  Denmark

```
Downloaded data includes the following fields:    
`date` `gdp_per_capita_usd` `internet_users_pct` `population` `country_code` `country`  

>[!NOTE]  
>Please note that the `internet_user_pct` data has been collected only since from year 1990.  

