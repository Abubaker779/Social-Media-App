from django.test import TestCase
from .models import User, Post, Comment
# Create your tests here.


# Server side Testing 
class TestCases(TestCase):
    def setUp(self):
        u1=User.objects.create(username="Abubaker0@",password="Abubaker0@")
        u2=User.objects.create(username="Abubaker1@",password="Abubaker1@")
        u3=User.objects.create(username="Abubaker2@",password="Abubaker2@")
        c1=Comment.objects.create(user=u1,comment='my first comment')
        c2=Comment.objects.create(user=u2,comment='my second comment')
        c3=Comment.objects.create(user=u3,comment='my third comment')     
        p1=Post.objects.create(user=u1,body="My first Post")
        p2=Post.objects.create(user=u2,body="My Second Post")
        p3=Post.objects.create(user=u3,body="My third Post")
        p1.comment.add(c1)
        p2.comment.add(c2)
        p3.comment.add(c3)

           
        


    def test_user_is_valid(self):
        u1=User.objects.get(pk=1)
        u2=User.objects.get(pk=2)
        u3=User.objects.get(pk=3)
        self.assertFalse(u1.is_staff)
        self.assertFalse(u2.is_staff)
        self.assertFalse(u3.is_staff)


    def test_username_uniqueness(self):
        u1=User.objects.get(pk=1)
        u2=User.objects.get(pk=2)
        u3=User.objects.get(pk=3)
        self.assertFalse(u1==u2)
        self.assertFalse(u2==u3)

    def test_add_comment(self):
        u1=User.objects.get(pk=1)
        u2=User.objects.get(pk=2)
        u3=User.objects.get(pk=3)
        c1=Comment.objects.get(pk=1)
        c2=Comment.objects.get(pk=2)
        c3=Comment.objects.get(pk=3)
        p1=Post.objects.create(user=u3,body="My test Post")
        p2=Post.objects.create(user=u2,body="My test Post")
        p3=Post.objects.create(user=u1,body="My test Post")
        p1.comment.add(c1)
        p2.comment.add(c2)
        p3.comment.add(c3)
        p=Post.objects.filter(body="My test Post").all().count()
        self.assertEqual(p,3)

    def test_delete_comment(self):
        c1=Comment.objects.get(pk=1)
        c2=Comment.objects.get(pk=2)
        c3=Comment.objects.get(pk=3)
        c1.delete()
        c2.delete()
        c3.delete()
        self.assertTrue(c1)
        self.assertTrue(c2)
        self.assertTrue(c3)        

    def test_like_post(self):
        p1=Post.objects.get(pk=1)
        p2=Post.objects.get(pk=2)
        p3=Post.objects.get(pk=3)
        print(f"a=> {p1.serialize()}")
        print(f"b=> {p2.serialize()}")
        print(f"c=> {p3.serialize()}")
        for _ in range(5):
            p1.like()
            p2.like()
            p3.like()
        print(f"1=> {Post.objects.get(pk=1).likes}:{Post.objects.get(pk=2).likes}:{Post.objects.get(pk=3).likes}")
        self.assertEqual(Post.objects.get(pk=1).likes,5)
        self.assertEqual(Post.objects.get(pk=2).likes,5)
        self.assertEqual(Post.objects.get(pk=3).likes,5)    
        

    def test_unlike_count(self):
        p1=Post.objects.get(pk=1)
        p2=Post.objects.get(pk=2)
        p3=Post.objects.get(pk=3)
        print(f"2=> {p1.serialize()}")
        print(f"3=> {p2.serialize()}")
        print(f"4=> {p3.serialize()}")
        for _ in range(5):
            p1.unlike()
            p2.unlike()
            p3.unlike()
        print(f"2=> {p1.likes}:{p2.likes}:{p3.likes}")    
        self.assertEqual(p1.likes,0)
        self.assertEqual(p2.likes,0)
        self.assertEqual(p3.likes,0)
        

    def test_delete_post(self):
        p1=Post.objects.get(pk=1)
        p2=Post.objects.get(pk=2)
        p3=Post.objects.get(pk=3)
        p1=p1.delete()
        p2=p2.delete()
        p3=p3.delete()
        self.assertTrue(p1)
        self.assertTrue(p2)
        self.assertTrue(p3)

           


          


        

        


