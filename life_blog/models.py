from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
import markdown

class Post(models.Model):
    title = models.CharField(max_length=200)
    # change to markdown field here
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def markdown2html(self):
    	self.text = markdown.markdown(self.text)
    	return self.text

    def __str__(self):
        return self.title

class Visiter(models.Model):
	ip = models.CharField(max_length=20)
	visit_date = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return self.ip

class Comment(models.Model):
	visiter = models.ForeignKey('Visiter')
	text = models.TextField()
	comment_date = models.DateTimeField(
		default=timezone.now)
