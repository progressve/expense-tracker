# Expense Tracker

A simple desktop Expense Tracker built with **Python, Tkinter, and MySQL**. It provides a graphical interface for recording, viewing, filtering, and deleting personal expenses.

## Features

* Add expenses with:

  * Amount
  * Category
  * Description
  * Date
* Store expenses in a MySQL database
* View all recorded expenses
* Filter expenses by category
* Delete selected expenses
* Automatically create the required database and table
* Save custom categories for future use
* Maintain an expense activity log

## Technologies Used

* **Python**
* **Tkinter** — Graphical User Interface
* **MySQL** — Database management
* **mysql-connector-python** — Python-MySQL connection

## Database Structure

The application automatically creates a database named `expense_db` and an `expenses` table containing:

| Field         | Description         |
| ------------- | ------------------- |
| `id`          | Unique expense ID   |
| `amount`      | Expense amount      |
| `category`    | Expense category    |
| `description` | Expense description |
| `date`        | Date of the expense |

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/expense-tracker.git
cd expense-tracker
```

### 2. Install the required Python package

```bash
pip install mysql-connector-python
```

### 3. Set up MySQL

Make sure MySQL is installed and running on your computer.

The application automatically creates the `expense_db` database and required table when it starts.

### 4. Configure your MySQL password

Open the Python file and update the MySQL password variable:

```python
pwd = ""
```

Set it to your local MySQL password.

### 5. Run the application

```bash
python project.py
```

## Project Structure

```text
expense-tracker/
│
├── project.py
├── cats.txt
├── expense_log.txt
└── README.md
```

`cats.txt` stores custom expense categories, while `expense_log.txt` records expense activity.

## What I Learned

This project helped me practice:

* Python GUI development with Tkinter
* Connecting Python applications to MySQL
* CRUD-style database operations
* SQL queries and database management
* File handling
* Exception handling
* Working with functions and event-driven programming

## Future Improvements

Some features I would like to add:

* Monthly spending summaries
* Expense charts and visualizations
* Edit existing expenses
* Date-range filtering
* Export expenses to CSV
* Improved input validation
* Better UI design

---

**Built with Python, Tkinter, and MySQL.**
