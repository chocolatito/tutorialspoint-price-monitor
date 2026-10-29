# [tutorialspoint-price-monitor](https://github.com/chocolatito/tutorialspoint-price-monitor)
A simple bot to monitor the course offerings on the website `market.tutorialspoint.com` according to a defined frequency.

* [Install dependencies](#install-dependencies)
* [Project Structure](#project-structure)
* [Execution](#execution)
* [Data storage](#data-storage)
  * [Tables](#tables)

---

## Install dependencies

Python 3.10+ is required
```sh
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt.
```

---

## Project Structure
```sh
.
├── .flake8
├── .gitignore
├── LICENSE
├── main.py
├── MONITOR.db
├── README.md
├── requirements.txt
├── src
│   ├── constants.py
│   ├── db_manager.py
│   ├── env-example.template
│   ├── parser_mixin.py
│   ├── scraper.py
│   └── utils.py
```

---

## Execution
```sh
# Default execution
python main.py

# To create the database at runtime
python main.py --create_tables="true"
```

---

## Data storage
The data is stored in a database.  
> The database name is defined in the `DB_NAME` constant in the `src/constants.py` file.

### Tables

**`course`**
```json
{
    "course_id": "20722",
    "href": "https://market.tutorialspoint.com/course/bootstrap-mastery-build-responsive-websites-like-a-pro/index.asp",
    "title": "Bootstrap Mastery: Build Responsive Websites Like a Pro",
    "data_title": "bootstrap-mastery-build-responsive-websites-like-a-pro",
    "sale_price": 8.99,
    "list_price": 100.0,
    "profile": "Mehmood Khalil",
    "profile_url": "https://market.tutorialspoint.com/profile/mehmood-khalil",
    "available": 1,
    "hexdigest": "aa523c6b5eca474e355e70b7301cc23c",
    "created_at": "2026-05-20 00:11:23",
    "updated_at": "2026-05-20 23:23:27"
}
```

**`historical`**
```json
{
    "id": 6,
    "sale_price": 8.99,
    "list_price": 40.0,
    "course_id": "18772",
    "created_at": "2026-10-29 00:32:10"
}
```