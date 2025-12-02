from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.post.models import Post

User = get_user_model()


class PostAPITestCase(TestCase):
    def setUp(self):
        """Set up test users and posts"""
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        self.post1 = Post.objects.create(
            author=self.user1,
            content='First test post'
        )
        self.post2 = Post.objects.create(
            author=self.user2,
            content='Second test post with Django'
        )
    
    def get_jwt_token(self, username, password):
        """Helper to get JWT token"""
        response = self.client.post('/api/token/pair', {
            'username': username,
            'password': password
        }, content_type='application/json')
        return response.json().get('access')
    
    def test_list_posts_200(self):
        """Test listing posts returns 200"""
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('total', data)
        self.assertIn('items', data)
        self.assertEqual(data['total'], 2)
    
    def test_list_posts_pagination(self):
        """Test pagination parameters"""
        response = self.client.get('/api/posts/?page=1&size=1')
        data = response.json()
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['size'], 1)
        self.assertEqual(len(data['items']), 1)
    
    def test_list_posts_search(self):
        """Test search filter"""
        response = self.client.get('/api/posts/?search=Django')
        data = response.json()
        self.assertEqual(data['total'], 1)
        self.assertIn('Django', data['items'][0]['content'])
    
    def test_list_posts_ordering(self):
        """Test ordering parameter"""
        response = self.client.get('/api/posts/?ordering=created_at')
        data = response.json()
        self.assertEqual(len(data['items']), 2)
    
    def test_get_post_200(self):
        """Test get single post returns 200"""
        response = self.client.get(f'/api/posts/{self.post1.id}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['id'], self.post1.id)
        self.assertEqual(data['content'], 'First test post')
        self.assertIn('author', data)
        self.assertEqual(data['author']['username'], 'testuser1')
    
    def test_get_post_404(self):
        """Test get non-existent post returns 404"""
        response = self.client.get('/api/posts/99999')
        self.assertEqual(response.status_code, 404)
    
    def test_create_post_401_without_auth(self):
        """Test create post without auth returns 401"""
        response = self.client.post('/api/posts/', {
            'content': 'Unauthorized post'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 401)
    
    def test_create_post_200_with_auth(self):
        """Test create post with JWT returns 200"""
        token = self.get_jwt_token('testuser1', 'testpass123')
        response = self.client.post('/api/posts/', {
            'content': 'New authenticated post'
        }, content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['content'], 'New authenticated post')
        self.assertEqual(data['author_username'], 'testuser1')
    
    def test_update_post_401_without_auth(self):
        """Test update post without auth returns 401"""
        response = self.client.put(f'/api/posts/{self.post1.id}', {
            'content': 'Updated content'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 401)
    
    def test_update_post_404_not_owner(self):
        """Test update post by non-owner returns 404"""
        token = self.get_jwt_token('testuser2', 'testpass123')
        response = self.client.put(f'/api/posts/{self.post1.id}', {
            'content': 'Trying to update'
        }, content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 404)
    
    def test_update_post_200_owner(self):
        """Test update post by owner returns 200"""
        token = self.get_jwt_token('testuser1', 'testpass123')
        response = self.client.put(f'/api/posts/{self.post1.id}', {
            'content': 'Updated by owner'
        }, content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['content'], 'Updated by owner')
    
    def test_delete_post_401_without_auth(self):
        """Test delete post without auth returns 401"""
        response = self.client.delete(f'/api/posts/{self.post1.id}')
        self.assertEqual(response.status_code, 401)
    
    def test_delete_post_200_owner(self):
        """Test delete post by owner returns 200"""
        token = self.get_jwt_token('testuser1', 'testpass123')
        response = self.client.delete(f'/api/posts/{self.post1.id}', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        # Verify post is deleted
        self.assertFalse(Post.objects.filter(id=self.post1.id).exists())
    
    def test_like_toggle_401_without_auth(self):
        """Test toggle like without auth returns 401"""
        response = self.client.post(f'/api/posts/{self.post1.id}/like')
        self.assertEqual(response.status_code, 401)
    
    def test_like_toggle_200_with_auth(self):
        """Test toggle like with auth returns 200"""
        token = self.get_jwt_token('testuser1', 'testpass123')
        # First like
        response = self.client.post(f'/api/posts/{self.post1.id}/like', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertTrue(data['liked'])
        self.assertEqual(data['like_count'], 1)
        
        # Unlike (toggle)
        response = self.client.post(f'/api/posts/{self.post1.id}/like', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertFalse(data['liked'])
        self.assertEqual(data['like_count'], 0)
    
    def test_nested_schema_author_details(self):
        """Test that post includes nested author details"""
        response = self.client.get(f'/api/posts/{self.post1.id}')
        data = response.json()
        self.assertIn('author', data)
        author = data['author']
        self.assertEqual(author['username'], 'testuser1')
        self.assertIn('level', author)
        self.assertIn('total_points', author)
        self.assertIn('is_verified', author)
    
    def test_nested_schema_counts(self):
        """Test that post includes like_count and comment_count"""
        response = self.client.get(f'/api/posts/{self.post1.id}')
        data = response.json()
        self.assertIn('like_count', data)
        self.assertIn('comment_count', data)
        self.assertEqual(data['like_count'], 0)
        self.assertEqual(data['comment_count'], 0)
