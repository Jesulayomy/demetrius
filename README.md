# Demetrius

The backend web api for NUESA-Funaab Resources

---

## Requirements
This project requires Python 3.10, a virtual environment manager,  MySQL
and a Linux server.

---

## Installation 
- First, clone the repository and navigate to the project directory

```bash
git clone https://github.com/Jesulayomy/demetrius.git
cd demetrius
```

- Next, create a virtual environment and activate it

```bash
python3 -m venv venv
source venv/bin/activate
```

- Install the project dependencies

```bash
pip install -r docs/requirements.txt
```

- Create a `.env` file in the root of the project and add the following environment variables

```env
# .env
DB_DEMETRIUS_USER=USER
DB_DEMETRIUS_PASSWORD=PASSWD
DB_DEMETRIUS_NAME=demetrius
DB_DEMETRIUS_HOST=HOST
DEMETRIUS_SECRET_KEY=KEY
DEMETRIUS_DEBUG=TEST
DEMETRIUS_ALLOWED_HOSTS=HOSTS
```

- Drive Folders
  - Create a credential for your application on the [Google Cloud Platform] and download the json file as `credentials.json` to the root of the project.
  - Create the base Drive folders as necessary, using the directory structure [^1]

- Create the database and run the migrations (It is recommended to delete the migrations folder and run the migrations again)

```bash
rm -rf library/migrations/
mysql -u USER -p
# Password
```

```SQL
# Use your own database name, user and password
>> CREATE DATABASE IF NOT EXISTS demetrius;
>> GRANT ALL PRIVILEGES ON demetrius.* TO USER@'localhost' IDENTIFIED BY 'PASSWD';
>> FLUSH PRIVILEGES;
```

```bash
python manage.py makemigrations library
python manage.py migrate

```

- Import data from Drive folder
First authenticate your application with the Google Drive API by running the command: `python manage.py shell` , then import the drive data to mysql database

```python
>> from library.manager import Manager
>> manager = Manager()
https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=
. . .
>> manager.build_db_tree_from_drive()
COLENG:
 DEPT: ELE
  LEVEL: 100
   SEM: 1ST
     . . .
Done!
```

- Create the superuser account with `python manage.py createsuperuser`

- Finally, run the server with `python manage.py runserver`

- The server will start running at `http://127.0.0.1:8000/`

### Project Maintainers

<table>
  <tr>
  <td align="center"><a href="https://github.com/Jesulayomy"><img src="https://avatars.githubusercontent.com/u/113533393?s=96&v=4" width="80px;" alt=""/><br /><sub><b>Jesulayomy</b></sub></a></td>

  <td align="center"><a href="https://github.com/DevEmmy"><img src="https://avatars.githubusercontent.com/u/62223314?v=4" width="80px;" alt=""/><br /><sub><b>DevEmmy</b></sub></a></td>
  </tr>
</table>


[^1]: Directory Structure
    ```
    COLLEGE
    --|ABE
    --|--|100
    --|--|--|1ST
    --|--|--|--|2023
    --|--|--|--|--|COURSES
    |__FILEA
    |__FILEB
    |__. . .
    --|--|--|2ND
    . . .
    --|--|200
    . . .
    --|CVE
    --|--|100
    --|--|--|1ST
    . . .
    --|ELE
    --|--|100
    . . .
    ```

[Google Cloud Platform]: https://console.cloud.google.com/
