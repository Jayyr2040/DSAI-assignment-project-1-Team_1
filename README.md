# DSAI-assignment-project-1-Team_1

## Project deliverables
- **Brief written report** (Markdown/PDF) following Sections 1–4 above.
- **Working dashboard/app** (provide a deployed link or clear local run instructions).
- **Code repository** containing:
    + Data handling notebook(s) / scripts,
    + Dashboard/app code,
    + README with setup steps.

## Hardware Requirements
- Use existing hardware qualified for the course.
- **Minimum:** 8 GB RAM.
- **Recommended:** > 16 GB RAM for optimal performance.


> <span style="color:red">**[WARNING]**
> 
> <span style="color:red">**No discrimination between Intel or Mac; use at your own discretion**

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

## Folder Setup & Workflow

### 1. Repository Setup
- **GitHub:** Create a new repository on GitHub (include a `README.md`).
- **Local Folder:** Create your project directory and clone the repo:
  ```bash
  mkdir DSAI-assignment-project-1-Team_1
  cd DSAI-assignment-project-1-Team_1
  git clone https://github.com/Jayyr2040/DSAI-assignment-project-1-Team_1.git .
  ```
- **Directory Structure:**
  ```bash
  mkdir notebooks app
  touch Written_Report.md
  ```
### 2. Environment Setup
- **If an `environment.yml` exists:**
  ```bash
  conda env create -f environment.yml
  ```
- **To export your environment (Initiator only):**
  ```bash
  conda env export --no-builds > environment.yml

### 3. Git Workflow
```bash
git status               # Check changes
git add .                # Stage all changes
git commit -m "message"  # Commit snapshot
git push                 # Upload to GitHub
```
## Tools & Deployment

### DuckDB (Database)
- Install within your active conda environment:
  ```bash
  conda install duckdb
  ```

### Streamlit (App)
#### Local Deployment
1. **Create and Activate Environment:**
   ```bash
   conda create -n job_analytics python=3.10 -y
   conda activate job_analytics
   ```
2. **Launch App:**
   Ensure your `.csv` data is in the same folder as your script (`app/SGjob_data.py`).
   ```bash
   streamlit run app/SGjob_data.py
   ```
   *Note: Use `Ctrl + C` in the terminal to stop the app.*

#### Cloud Deployment (Streamlit Community Cloud)
1. **Ensure the following are pushed to GitHub:**
   - `notebook.ipynb` (Main logic)
   - `original_data.csv` (Raw source)
   - `app.py` (Streamlit script)
   - `database.csv` (Referenced data)
   - `requirements.txt` (List of dependencies, e.g., `pandas`, `streamlit`, `plotly`)
2. **Deploy:**
   - Log in to [Streamlit.io](https://streamlit.io/) and link your GitHub.
   - Select "Create App" and point to your `app.py` file.
 
