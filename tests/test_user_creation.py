import pytest
import responses
import os
import tempfile
import csv
from unittest.mock import patch, MagicMock
import sys

# Add parent directory to path to import the main module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import after path modification
from user_creation_script import validate_user_data, create_single_user, create_users


class TestValidateUserData:
    """Tests for user data validation"""
    
    def test_valid_user_data(self):
        """Test validation with valid user data"""
        valid_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'role': 'admin'
        }
        is_valid, error = validate_user_data(valid_data)
        assert is_valid is True
        assert error is None
    
    def test_missing_name(self):
        """Test validation fails when name is missing"""
        invalid_data = {
            'name': '',
            'email': 'john@example.com',
            'role': 'admin'
        }
        is_valid, error = validate_user_data(invalid_data)
        assert is_valid is False
        assert 'Missing name' in error
    
    def test_missing_email(self):
        """Test validation fails when email is missing"""
        invalid_data = {
            'name': 'John Doe',
            'email': '',
            'role': 'admin'
        }
        is_valid, error = validate_user_data(invalid_data)
        assert is_valid is False
        assert 'Missing email' in error
    
    def test_invalid_email_format(self):
        """Test validation fails with invalid email format"""
        invalid_data = {
            'name': 'John Doe',
            'email': 'invalid-email',
            'role': 'admin'
        }
        is_valid, error = validate_user_data(invalid_data)
        assert is_valid is False
        assert 'Invalid email format' in error
    
    def test_invalid_role(self):
        """Test validation fails with invalid role"""
        invalid_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'role': 'superadmin'
        }
        is_valid, error = validate_user_data(invalid_data)
        assert is_valid is False
        assert 'Invalid role' in error
    
    def test_valid_roles(self):
        """Test all valid roles are accepted"""
        valid_roles = ['admin', 'user', 'moderator']
        for role in valid_roles:
            data = {
                'name': 'John Doe',
                'email': 'john@example.com',
                'role': role
            }
            is_valid, error = validate_user_data(data)
            assert is_valid is True
            assert error is None


class TestCreateSingleUser:
    """Tests for single user creation"""
    
    @responses.activate
    def test_successful_user_creation(self):
        """Test successful API call for user creation"""
        api_url = "https://example.com/api/create_user"
        responses.add(
            responses.POST,
            api_url,
            json={'message': 'User created'},
            status=201
        )
        
        user_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'role': 'admin'
        }
        
        success, error = create_single_user(user_data, api_url)
        assert success is True
        assert error is None
    
    @responses.activate
    def test_api_error_response(self):
        """Test handling of API error responses"""
        api_url = "https://example.com/api/create_user"
        responses.add(
            responses.POST,
            api_url,
            json={'error': 'User already exists'},
            status=400
        )
        
        user_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'role': 'admin'
        }
        
        success, error = create_single_user(user_data, api_url)
        assert success is False
        assert 'API error' in error
        assert '400' in error
    
    @responses.activate
    def test_connection_error(self):
        """Test handling of connection errors"""
        api_url = "https://example.com/api/create_user"
        responses.add(
            responses.POST,
            api_url,
            body=Exception('Connection failed')
        )
        
        user_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'role': 'admin'
        }
        
        success, error = create_single_user(user_data, api_url)
        assert success is False
        assert error is not None
    
    def test_data_trimming(self):
        """Test that whitespace is properly trimmed from user data"""
        api_url = "https://example.com/api/create_user"
        
        with responses.RequestsMock() as rsps:
            rsps.add(responses.POST, api_url, status=201)
            
            user_data = {
                'name': '  John Doe  ',
                'email': '  john@example.com  ',
                'role': '  admin  '
            }
            
            create_single_user(user_data, api_url)
            
            # Check that the request was made with trimmed data
            assert len(rsps.calls) == 1
            request_data = rsps.calls[0].request.body
            assert b'John Doe' in request_data
            assert b'  John Doe  ' not in request_data


class TestCreateUsers:
    """Tests for batch user creation from CSV"""
    
    def test_file_not_found(self, caplog):
        """Test handling of missing CSV file"""
        create_users('nonexistent.csv')
        assert 'File not found' in caplog.text
    
    def test_missing_csv_columns(self, caplog):
        """Test handling of CSV with missing required columns"""
        # Create temporary CSV with wrong columns
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'email'])
            writer.writeheader()
            f.flush()
            temp_file = f.name
        
        try:
            create_users(temp_file)
            assert 'CSV missing required columns' in caplog.text
        finally:
            os.unlink(temp_file)
    
    @responses.activate
    def test_successful_batch_creation(self, caplog):
        """Test successful batch user creation"""
        api_url = "https://example.com/api/create_user"
        responses.add(responses.POST, api_url, status=201)
        
        # Create temporary CSV with valid data
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'email', 'role'])
            writer.writeheader()
            writer.writerow({'name': 'John Doe', 'email': 'john@example.com', 'role': 'admin'})
            writer.writerow({'name': 'Jane Smith', 'email': 'jane@example.com', 'role': 'user'})
            f.flush()
            temp_file = f.name
        
        try:
            create_users(temp_file, api_url)
            assert 'Successfully created: 2' in caplog.text
        finally:
            os.unlink(temp_file)
    
    @responses.activate
    def test_mixed_results(self, caplog):
        """Test batch processing with mixed success/failure results"""
        api_url = "https://example.com/api/create_user"
        responses.add(responses.POST, api_url, status=201)
        
        # Create temporary CSV with mixed valid/invalid data
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'email', 'role'])
            writer.writeheader()
            writer.writerow({'name': 'John Doe', 'email': 'john@example.com', 'role': 'admin'})
            writer.writerow({'name': '', 'email': 'invalid@example.com', 'role': 'user'})  # Invalid: missing name
            writer.writerow({'name': 'Jane', 'email': 'bademail', 'role': 'user'})  # Invalid: bad email
            f.flush()
            temp_file = f.name
        
        try:
            create_users(temp_file, api_url)
            assert 'Successfully created: 1' in caplog.text
            assert 'Skipped (validation failed): 2' in caplog.text
        finally:
            os.unlink(temp_file)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])