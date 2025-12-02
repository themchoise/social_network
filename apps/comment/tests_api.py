from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.post.models import Post
from apps.comment.models import Comment

User = get_user_model()


class CommentAPITestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.user1 = User.objects.create_user(
            username='commenter1',
            email='comm1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='commenter2',
            email='comm2@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            author=self.user1,
            content='Post for comments'
        )
        self.comment1 = Comment.objects.create(
            author=self.user1,
            post=self.post,
            content='First comment'
        )
    
    def get_jwt_token(self, username, password):
        """Helper to get JWT token"""
        response = self.client.post('/api/token/pair', {
            'username': username,
            'password': password
        }, content_type='application/json')
        return response.json().get('access')
    
    def test_list_comments_200(self):
        """Test listing comments returns 200"""
        response = self.client.get('/api/comments/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('total', data)
        self.assertGreaterEqual(data['total'], 1)
    
    def test_list_comments_filter_by_post(self):
        """Test filtering comments by post_id"""
        response = self.client.get(f'/api/comments/?post_id={self.post.id}')
        data = response.json()
        self.assertEqual(data['total'], 1)
        self.assertEqual(data['items'][0]['post_id'], self.post.id)
    
    def test_get_comment_200(self):
        """Test get single comment returns 200"""
        response = self.client.get(f'/api/comments/{self.comment1.id}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['content'], 'First comment')
        self.assertEqual(data['author_username'], 'commenter1')
    
    def test_create_comment_401_without_auth(self):
        """Test create comment without auth returns 401"""
        response = self.client.post('/api/comments/', {
            'post_id': self.post.id,
            'content': 'Unauthorized comment'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 401)
    
    def test_create_comment_200_with_auth(self):
        """Test create comment with auth returns 200"""
        token = self.get_jwt_token('commenter1', 'testpass123')
        response = self.client.post('/api/comments/', {
            'post_id': self.post.id,
            'content': 'New authenticated comment'
        }, content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['content'], 'New authenticated comment')
        self.assertEqual(data['post_id'], self.post.id)
    
    def test_create_reply_comment(self):
        """Test creating a reply to existing comment"""
        token = self.get_jwt_token('commenter2', 'testpass123')
        response = self.client.post('/api/comments/', {
            'post_id': self.post.id,
            'content': 'Reply to first comment',
            'parent_id': self.comment1.id
        }, content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['parent_id'], self.comment1.id)
    
    def test_update_comment_200_owner(self):
        """Test update comment by owner returns 200"""
        token = self.get_jwt_token('commenter1', 'testpass123')
        response = self.client.put(f'/api/comments/{self.comment1.id}', {
            'content': 'Updated comment content'
        }, content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['content'], 'Updated comment content')
        self.assertTrue(data['is_edited'])
    
    def test_delete_comment_200_owner(self):
        """Test delete comment by owner returns 200"""
        token = self.get_jwt_token('commenter1', 'testpass123')
        response = self.client.delete(f'/api/comments/{self.comment1.id}', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
