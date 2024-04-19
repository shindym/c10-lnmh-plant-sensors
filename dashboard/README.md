# Dashboard

This folder contains all code and resources required for the dashboard.

## Requirements

**Modules**

 ```sh
   pip3 install -r requirements.txt
   ```

**Secrets/Authentication**
> [!IMPORTANT]  
> To be able to run these scripts the following details must be provided in the `.env` file.

| KEY                   | FILE REQUIRED |
|-----------------------|---------------|
| DB_HOST               | `app.py`      |
| DB_USER               | `app.py`      |
| DB_PASSWORD           | `app.py`      |
| DB_PORT               | `app.py`      |
| DB_NAME               | `app.py`      |
| AWS_ACCESS_KEY_ID     | `app.py`      |
| AWS_SECRET_ACCESS_KEY | `app.py`      |
| storage_folder        | `app.py`      |

## Files and Folders

- root folder: Contains code related to the pipeline.
    - `app.py` : python script responsible for running the dashboard.
    - `Dockerfile` - Contains the Dockerfile for the dashboard.
    - `README.md` - Contains the documentation for the dashboard.
    - `requirements.txt` - Contains the required packages for the dashboard.

- `.streamlit` folder: holds dashboard theme configuration details
    - `config.toml` - Contains the configuration details for the dashboard.

- `images` folder: Contains the images for the documentation.

#### Database reset script

```sh
   streamlit run app.py
   ```

This command runs and opens dashboard in your browser.

### Wireframe

In order to structure this dashboard effectively, a wireframe has been created to help identify what information we will
be displaying as well as where it will be displayed.

![Dashboard Wireframe](https://github.com/shindym/c10-lnmh-plant-sensors/blob/dashboard-readme/dashboard/images/plant-wireframe.png)

### Dashboard

This is the final look of the dashboard.

![Final Dashboard](https://github.com/shindym/c10-lnmh-plant-sensors/blob/dashboard-readme/dashboard/images/plant-dashboard.png)


