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

[^1]: Directory Structure
    ```
    COLLEGE
    --|ABE
    --|--|100
    --|--|--|1ST
    --|--|--|--|2023
    --|--|--|--|--|COURSES
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
