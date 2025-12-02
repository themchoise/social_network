from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAPITestCase(TestCase):
    def setUp(self):
        """Set up test users"""
        self.user1 = User.objects.create_user(
            username='apiuser1',
            email='api1@example.com',
            password='testpass123',
            bio='Test bio'
        )
        self.user2 = User.objects.create_user(
            username='apiuser2',
            email='api2@example.com',
            password='testpass123'
        )
    
    def get_jwt_token(self, username, password):
        """Helper to get JWT token"""
        response = self.client.post('/api/token/pair', {
            'username': username,
            'password': password
        }, content_type='application/json')
        return response.json().get('access')
    
    def test_list_users_200(self):
        """Test listing users returns 200"""
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('total', data)
        self.assertIn('items', data)
        self.assertGreaterEqual(data['total'], 2)
    
    def test_list_users_search(self):
        """Test user search filter"""
        response = self.client.get('/api/users/?search=apiuser1')
        data = response.json()
        self.assertGreaterEqual(data['total'], 1)
        self.assertEqual(data['items'][0]['username'], 'apiuser1')
    
    def test_get_user_200(self):
        """Test get single user returns 200"""
        response = self.client.get(f'/api/users/{self.user1.id}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['username'], 'apiuser1')
        self.assertEqual(data['bio'], 'Test bio')
        self.assertIn('achievements', data)
    
    def test_get_user_404(self):
        """Test get non-existent user returns 404"""
        response = self.client.get('/api/users/99999')
        self.assertEqual(response.status_code, 404)
    
    def test_create_user_200(self):
        """Test create user returns 200"""
        response = self.client.post('/api/users/', {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['username'], 'newuser')
        self.assertEqual(data['first_name'], 'New')
    
    def test_update_user_401_without_auth(self):
        """Test update user without auth returns 401"""
        response = self.client.put(f'/api/users/{self.user1.id}', {
            'bio': 'Updated bio'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 401)
    
    def test_update_user_404_not_owner(self):
        """Test update user by different user returns 404"""
        token = self.get_jwt_token('apiuser2', 'testpass123')
        response = self.client.put(f'/api/users/{self.user1.id}', {
            'bio': 'Trying to update'
        }, content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 404)
    
    def test_update_user_200_owner(self):
        """Test update user by owner returns 200"""
        token = self.get_jwt_token('apiuser1', 'testpass123')
        response = self.client.put(f'/api/users/{self.user1.id}', {
            'bio': 'Updated bio by owner',
            'first_name': 'Updated'
        }, content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['bio'], 'Updated bio by owner')
        self.assertEqual(data['first_name'], 'Updated')
    
    def test_delete_user_200_owner(self):
        """Test delete user by owner returns 200"""
        token = self.get_jwt_token('apiuser1', 'testpass123')
        response = self.client.delete(f'/api/users/{self.user1.id}', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertFalse(User.objects.filter(id=self.user1.id).exists())
    
    def test_user_nested_achievements(self):
        """Test that user includes nested achievements list"""
        response = self.client.get(f'/api/users/{self.user1.id}')
        data = response.json()
        self.assertIn('achievements', data)
        self.assertIsInstance(data['achievements'], list)
