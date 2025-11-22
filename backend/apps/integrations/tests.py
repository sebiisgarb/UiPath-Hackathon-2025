from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch, MagicMock
import asyncio


class ActivitiesAPITest(APITestCase):
    """
    Test cases for the Amadeus activities API endpoint.
    """
    
    def test_get_activities_missing_latitude(self):
        """Test that latitude parameter is required."""
        response = self.client.get('/api/integrations/activities/')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn('latitude', response.data['error'].lower())
    
    def test_get_activities_missing_longitude(self):
        """Test that longitude parameter is required."""
        response = self.client.get('/api/integrations/activities/?latitude=48.8566')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn('longitude', response.data['error'].lower())
    
    def test_get_activities_invalid_latitude(self):
        """Test that latitude must be a valid number."""
        response = self.client.get('/api/integrations/activities/?latitude=invalid&longitude=2.3522')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_get_activities_invalid_min_price(self):
        """Test that min_price must be a valid number."""
        response = self.client.get('/api/integrations/activities/?latitude=48.8566&longitude=2.3522&min_price=invalid')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn('min_price', response.data['error'].lower())
    
    def test_get_activities_invalid_max_price(self):
        """Test that max_price must be a valid number."""
        response = self.client.get('/api/integrations/activities/?latitude=48.8566&longitude=2.3522&max_price=invalid')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn('max_price', response.data['error'].lower())
    
    def test_get_activities_invalid_limit(self):
        """Test that limit must be a valid integer."""
        response = self.client.get('/api/integrations/activities/?latitude=48.8566&longitude=2.3522&limit=invalid')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn('limit', response.data['error'].lower())
    
    @patch.dict('os.environ', {}, clear=True)
    def test_get_activities_missing_credentials(self):
        """Test that API returns error when credentials are not configured."""
        response = self.client.get('/api/integrations/activities/?latitude=48.8566&longitude=2.3522')
        
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertIn('error', response.data)
        self.assertIn('credentials', response.data['error'].lower())
    
    @patch.dict('os.environ', {'AMADEUS_CLIENT_ID': 'test_id', 'AMADEUS_CLIENT_SECRET': 'test_secret'})
    @patch('apps.integrations.views.AmadeusClient')
    def test_get_activities_success(self, mock_amadeus_client):
        """Test successful activities retrieval."""
        # Mock the amadeus client response
        mock_instance = MagicMock()
        mock_amadeus_client.return_value = mock_instance
        
        # Create a mock async coroutine
        async def mock_get_activities(*args, **kwargs):
            return {
                'data': [
                    {
                        'id': '1',
                        'name': 'Eiffel Tower Visit',
                        'price': {'amount': '25.00', 'currencyCode': 'EUR'},
                        'rating': 4.5,
                        'pictures': ['url1', 'url2', 'url3']
                    }
                ]
            }
        
        mock_instance.get_activities.return_value = mock_get_activities()
        
        response = self.client.get('/api/integrations/activities/?latitude=48.8566&longitude=2.3522')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIsInstance(response.data['data'], list)
    
    @patch.dict('os.environ', {'AMADEUS_CLIENT_ID': 'test_id', 'AMADEUS_CLIENT_SECRET': 'test_secret'})
    @patch('apps.integrations.views.AmadeusClient')
    def test_get_activities_with_all_parameters(self, mock_amadeus_client):
        """Test activities retrieval with all optional parameters."""
        # Mock the amadeus client response
        mock_instance = MagicMock()
        mock_amadeus_client.return_value = mock_instance
        
        # Create a mock async coroutine
        async def mock_get_activities(*args, **kwargs):
            return {'data': []}
        
        mock_instance.get_activities.return_value = mock_get_activities()
        
        response = self.client.get(
            '/api/integrations/activities/?latitude=48.8566&longitude=2.3522&'
            'radius=5&min_price=10.0&max_price=100.0&limit=10&sort_by_rating=true'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify that get_activities was called with correct parameters
        mock_instance.get_activities.assert_called_once()
        call_kwargs = mock_instance.get_activities.call_args[1]
        self.assertEqual(call_kwargs['latitude'], 48.8566)
        self.assertEqual(call_kwargs['longitude'], 2.3522)
        self.assertEqual(call_kwargs['radius'], 5)
        self.assertEqual(call_kwargs['min_price'], 10.0)
        self.assertEqual(call_kwargs['max_price'], 100.0)
        self.assertEqual(call_kwargs['limit'], 10)
        self.assertTrue(call_kwargs['sort_by_rating'])
