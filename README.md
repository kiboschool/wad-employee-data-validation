# Employee data validation

This example application shows employee records. It's not a great application. For one, it's quite plain. The bigger issue - much of the data is invalid!

In this practice, you'll work on data validation and SQL by fixing bad data in the application.

## Starter Code

There is a Flask application in `app.py`, with a connection to a SQLite database with a table "employees".

The "employees" table has the following columns: id (integer), name (text), email (text), and salary (integer).

Run the application, click around, and explore the database and schema to get a sense for what you are working with.

## Your Task

In the database, there are some employees with invalid data. Their names are empty or contain numbers, they have duplicate emails, and their salaries are negative. 

That doesn't make sense! Your job is to fix these entries.

First, read the rules for what valid data should look like. Then, add validation to the application so that no more invalid data gets added. Then fix the data in the database so that it is valid. Finally, add database constraints for an extra layer of data protection.

### Validation Rules

Here are the rules the application must implement:

- The salary must be a positive integer
- The name must be a non-empty string with no numbers
- Emails must not be null
- Emails must be unique (there cannot be duplicates)
- Emails must have the `@` character in them

### Part 1: Add Validation

Implement validation to prevent any more bad data from being added to the database. 

In the `add_employee` route, use the `request.form` object to access the input and validate the data before inserting it into the database.

- If the data is valid, insert it into the database. The route should continue to redirect to the index.
- If it is not valid:
  - don't insert the data into the database.
  - return an error message to the user 

You can manually validate the input, or import and use a library.

### Part 2: Fix the data

Now that you've added validation, no more bad data will be added to the database. But, there's still a bunch of old, bad data in there! Now, you need to fix it.

1. Make a backup copy of the database. Copy the database file to a new file called `backup-employees.db`. 
2. Connect to the database (either using Python or the sqlite3 command line tool).
3. **Delete** any rows where the data is not valid.
  - any rows where the salary is zero or less
  - any rows with a NULL or blank name, or a name with a number in it
  - any rows with NULL emails
  - any rows where the email is missing the `@` character
  - any rows with duplicate emails (Hint: first find these using COUNT and GROUP BY, then delete them by their ids)

In many applications, you might make an attempt to figure out how the bad data was added, and try to correct it. In this case, since it's just for practice, go ahead and delete the bad data -- that's why you made a backup!

### Part 3: Add database validation

You've added server-side validation and you've fixed the data. Now it's time to add database constraints for another level of protection for the database.

1. Create a file called `schema_with_validations.sql` to create the `new_employees` table
2. In the file write a CREATE TABLE like in `schema.sql`, but with these constraints on the `new_employees` table:
  - make name NOT NULL
  - make email NOT NULL UNIQUE
3. Create the new table

```sh
sqlite3 employees.db < schema_with_validations.sql
```

SQLite does not support all of the ALTER TABLE statements, so in order to use the validations, we'll have to do a little copying.

4. Copy the current employees table (the one without the constraints) to the new table. Then drop the old table, and rename the new table, so there's only one _validated_ employees table:

```sql
INSERT INTO new_employees SELECT * FROM employees;
DROP TABLE employees;
ALTER TABLE new_employees RENAME TO employees;
```

> Note: in a live production database, it'd be wise to do all of this table-copying in a transaction, in case something goes wrong. In a database like Postgres or MySQL, there is also more support for adding constraints, so there's less cause to copy, drop, and re-add tables.

## Bonus: Updating data

Now that you have validations, you can add more features to the application. Add a route that allows users to edit existing employees' data.

Be sure to validate the data before updating the database.

## Bonus: Accessibility, Feedback, Styling

Right now, this app is not very user-friendly or accessible.

1. Add labels to the form fields
2. Change the types of the inputs to match the data types expected by the application
3. Add `required` and `min` attributes to the inputs to help show client-side validation
4. When there are validation errors, show them inline with the inputs, instead of below the form
5. Add instructions to the form that tell the user what they have to enter to create a valid employee

You can also improve the styling of the form. Right now, it's quite bad looking!

