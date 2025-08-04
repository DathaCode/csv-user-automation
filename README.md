User Account Creation Script
==================================================
A Python script that creates user accounts from a CSV file by sending requests to an API endpoint. This is my solution to fix the bugs in the original script and add better error handling.
What Was Wrong With The Original Script
The original script had several problems:

No error logging - when something failed, there was no way to know what went wrong
Missing field handling - if a row had empty email, it would still try to create the user
Poor error handling - network errors would crash the script
No validation - didn't check if email format was valid or if roles were correct

What I Fixed
1. Added Proper Error Logging

Now writes detailed errors to error_log.txt
Shows which row failed and why
Includes timestamps for all log entries

2. Data Validation

Skips rows with missing required fields (name, email, role)
Basic email validation (checks for @ and . symbols)
Validates roles against allowed values: admin, user, moderator

3. Better Error Handling

Handles network timeouts and connection errors
Doesn't crash when API returns error codes
Shows clear error messages

4. Summary Statistics

Shows how many users were created successfully
Counts how many rows were skipped
Reports any failures

How to Use
1. Install Requirements
bashpip install requests
2. Prepare Your CSV File
Create a file called users.csv with these columns:
csvname,email,role
James Brown,james.brown@example.com,admin
Harsha Wijeratne,harsha.wijeratne@example.com,moderator
Lucía Torres,lucia.torres@example,moderator
3. Run the Script
bashpython user_creator.py
4. Check Results

Look at the console output for a summary
Check error_log.txt for detailed error information

CSV File Format
Your CSV file must have these columns:

name: User's full name (required)
email: Valid email address (required)
role: Must be one of: admin, user, moderator (required)

Example Output
When you run the script, you'll see something like this:
2024-08-03 10:30:15 - INFO - Starting to process file: users.csv
2024-08-03 10:30:15 - WARNING - Row 3 skipped: Missing email - Data: {'name': 'Bob', 'email': '', 'role': 'user'}
2024-08-03 10:30:16 - INFO - User created successfully: alice@example.com
2024-08-03 10:30:16 - ERROR - Row 5 failed: Invalid email format: not-an-email - User: not-an-email


PROCESSING COMPLETE
Total rows: 4
Successfully created: 2
Skipped (validation failed): 1
Failed (API errors): 1
Configuration
You can change these settings in the script:
python# At the bottom of the script
CSV_FILE = "users.csv"          # Change this to your CSV file name
API_ENDPOINT = "https://example.com/api/create_user"  # Change to your API URL
Files Created

error_log.txt - Detailed log of all operations and errors
Console output - Summary of what happened

Testing
I've included a sample users.csv file with various test cases:

Valid users that should be created
Users with missing emails (should be skipped)
Users with invalid email formats (should be skipped)
Users with invalid roles (should be skipped)

Limitations and Future Improvements
This is a working solution but could be improved:
Current limitations:

Basic email validation (just checks for @ and .)
No retry logic if API is temporarily down
Processes one user at a time (could be slow for large files)

Possible improvements:

Add command line arguments for file paths
More robust email validation using regex
Retry failed requests automatically
Progress bar for large files
Support for different CSV formats
Better configuration file instead of hardcoded values

Troubleshooting

"File not found" error:
Make sure your CSV file is in the same folder as the script
Check the filename is spelled correctly

"CSV missing required columns" error:
Make sure your CSV has columns named exactly: name, email, role
Check that the first row contains the column headers

Network errors:
Verify the API endpoint URL is correct
The API server might be down

Code Structure
The script is organized into these main functions:

setup_logging() - Sets up logging to file and console
validate_user_data() - Checks if a row has valid data
create_single_user() - Makes the API request for one user
create_users() - Main function that processes the entire CSV file