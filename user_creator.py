import csv
import requests
import logging
import os
from datetime import datetime

# Configure logging
def setup_logging():
    """Setup logging to file and console"""
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler('error_log.txt'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

def validate_user_data(row):
    # Checking required fields
    required_fields = ['name', 'email', 'role']
    
    for field in required_fields:
        if not row.get(field) or row.get(field).strip() == '':
            return False, f"Missing {field}"
    
    # email validation
    email = row['email'].strip()
    if '@' not in email or '.' not in email:
        return False, f"Invalid email format: {email}"
    
    # Check if role is valid (only allow specific roles: admin, user, moderator)
    valid_roles = ['admin', 'user', 'moderator']
    role = row['role'].strip().lower()
    if role not in valid_roles:
        return False, f"Invalid role: {role}"
    
    return True, None

def create_single_user(user_data, api_url):
    """
    Create a single user account
    Returns: (success, error_message)
    """
    try:
        # Cleaning data
        clean_data = {}
        for key, value in user_data.items():
            if value:
                clean_data[key] = value.strip()
        
        response = requests.post(
            api_url, 
            json=clean_data,
            timeout=10  # Add timeout to prevent hanging
        )
        
        if response.status_code == 201:
            logger.info(f"User created successfully: {clean_data['email']}")
            return True, None
        else:
            error_msg = f"API error - Status: {response.status_code}"
            if response.text:
                error_msg += f", Response: {response.text[:100]}"
            return False, error_msg
            
    except requests.exceptions.Timeout:
        return False, "Request timed out"
    except requests.exceptions.ConnectionError:
        return False, "Could not connect to API"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

def create_users(file_path, api_url="https://example.com/api/create_user"):
    """
    Main function to create users from CSV file
    """
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return
    
    # Keep track of results
    total_rows = 0
    successful = 0
    skipped = 0
    failed = 0
    
    logger.info(f"Starting to process file: {file_path}")
    
    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            
            # Checking CSV columns
            expected_columns = ['name', 'email', 'role']
            if not all(col in reader.fieldnames for col in expected_columns):
                logger.error(f"CSV missing required columns. Expected: {expected_columns}")
                return
            
            for row_num, row in enumerate(reader, start=2):  # start=2 because row 1 is header
                total_rows += 1
                
                # Validate the row data
                is_valid, error_msg = validate_user_data(row)
                
                if not is_valid:
                    skipped += 1
                    logger.warning(f"Row {row_num} skipped: {error_msg} - Data: {row}")
                    continue
                
                # Creating user msg
                success, error_msg = create_single_user(row, api_url)
                
                if success:
                    successful += 1
                else:
                    failed += 1
                    logger.error(f"Row {row_num} failed: {error_msg} - User: {row.get('email', 'unknown')}")
    
    except Exception as e:
        logger.error(f"Error reading CSV file: {e}")
        return
    
    # Print summary
    logger.info("="*50)
    logger.info("PROCESSING COMPLETE")
    logger.info(f"Total rows: {total_rows}")
    logger.info(f"Successfully created: {successful}")
    logger.info(f"Skipped (validation failed): {skipped}")
    logger.info(f"Failed (API errors): {failed}")
    
    if failed > 0 or skipped > 0:
        logger.warning("Some users were not created. Check error_log.txt for details.")

# Main run
if __name__ == "__main__":
    ######### Change the CSV file path and API endpoint as needed #########
    CSV_FILE = "users.csv"
    API_ENDPOINT = "https://example.com/api/create_user"
    
    create_users(CSV_FILE, API_ENDPOINT)