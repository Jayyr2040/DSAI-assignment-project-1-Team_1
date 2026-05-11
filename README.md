# DSAI-assignment-project-1-Team_1

## Project deliverables
- Brief written report (Markdown/PDF) following Sections 1–4 above.
- Working dashboard / app (deployed link or clear run instructions).
- Code repo with:
    + Data handling notebook(s) / scripts,
    + Dashboard/app code,
    + README with setup steps.

## Hardware Requirements
- Use existing hardware which has being qualified for the course. 
- Min 8 GB RAM. Recommend > 16 GB for optimal performance.

> <span style="color:red">**[WARNING]**
> 
> <span style="color:red">**No discrimination between Intel or Mac, use at your own discretion**

## Software Requirements

| Software | Description | Platform | Details |
|----------|-------------|----------|---------|
| WSL | Windows Subsystem for Linux | Windows only | [Installation Guide](#wsl-for-windows) |
| Visual Studio Code (VSCode) | Source code editor | All platforms | [Installation Guide](#visual-studio-code-vscode) |
| Git CLI | Command-Line Interface for version control | All platforms | [Installation Guide](#git-cli) |
| Conda/Miniconda | Package and environment manager | All platforms | [Installation Guide](#condaminiconda) |
| DBGate/DBeaver | Database viewer | All platforms | [Installation Guide](#duckdb-browser-dbgate) | 
| DuckDB | Lightweight, in-process analytical database (no server needed) | All platforms | [Installation Guide](#https://duckdb.org/) |
| Test Installation | Confirm if everything is working fine | All platforms | [Verification Guide](#verification-of-installation-mac-and-windows-users) |

## Folder Setup
- Project Repo: 
    + Users should create a new repo using your desired github account.
    + Include a README.md file during creation
- Local Project Folder: 
    + Similarly set up a project folder in local drive. In your local root folder, type: `mkdir DSAI-assignment-project-1-Team_1 `
    + Navigate into the project folder that was created and create a local clone of the repo, type: `git clone 'https://github.com/Jayyr2040/DSAI-assignment-project-1-Team_1.git'`.
    + Report file creation: type `touch Written_Report.md`
    + Notebooks folder creation: type `mkdir notebooks`
    + App folder creation: type `mkdir app` 
    + README.md creation: cloned from repo
    + Conda env: Type `conda env create -f environment.yml` to install all necessary libraries (Pandas, Plotly, Streamlit, DuckDB) in an isolated environment. (Note: this step is for when a environment.yml was created for you by initiator) 
        * If you are initiating from scratch, type `conda env export --no-builds > environment.yml` at the end when you are about to wrap this project so that others can use your replicate your work later on.
    + Updating of git repo: 
        * type `git status` to check changes
        * type `git add .` to stage all files in the project folder
        * type `git commit -m "message"` to finalize the snapshot and commit all files
        * type `git push` to upload GitHub

- Jupyter Notebook (Main Engine):
    + Create a new notebook. One way would be via VS Code. Press `Ctrl + Shift + P` and search and select Creat new Juypter Notebook.
- Duckdb (Database):
    + Should have installed based software requirements above
    + At WSL terminal, type `conda install duckdb`
- Streamlit (App):
    + In the project folder, type `conda create -n job_analytics python=3.10 -y`.
    + To activate the environment, type `conda activate job_analytics`. Similar to ddb or pds activation at WSL terminal.
    + Create SGjob_data.py in the app folder that was created earlier.
    + To run SGjob_data.py, type `streamlit run app/SGjob_data.py` at the root project folder. 
        * .csv has to be the same folder as SGjob_data.py as it is referenced by app.py
    + To type `conda list` to check if Streamlit, Pandas and Plotly libraries are in the list in case unsure.
    + Links to browser will be shared if successful to launch app.
    + `Ctrl + c` to abort at terminal.

