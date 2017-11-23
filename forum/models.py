from django.db import models
from mainapp.models import RootProfile
from django.contrib.auth.models import User


class Forum(models.Model):
    owner = models.ForeignKey(RootProfile, related_name='forums')
    name = models.CharField(max_length=30)
    url = models.CharField(max_length=40, unique=True)
    punchline = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=300, default='')
    created_on = models.DateTimeField()
    thumb = models.ImageField()
    bg = models.ImageField(null=True)
    bg_thread = models.ImageField(null=True)

    def __str__(self):
        return self.name + '; owner: ' + self.owner.user.username

    def get_thread_count(self):
        cats = self.category_set.all()
        boards = [cat.board_set.all() for cat in cats]
        threads = [board.thread_set.all() for board in boards]
        return len(threads)

    def get_post_count(self):
        posts = Post.objects.filter(
            thread__board__category__forum=self).count()
        return posts

    def get_members_count(self):
        members = Post.objects.filter(
            thread__board__category__forum=self).values(
                'author').distinct().count()
        return members


class Profile(models.Model):
    user = models.OneToOneField(User)
    joined_on = models.DateTimeField()
    screen_name = models.CharField(max_length=30, null=True, blank=True)
    dp = models.ImageField(upload_to='user_dp')
    quote = models.CharField(max_length=300, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    karma = models.IntegerField(default=0)

    def __str__(self):
        return self.username

    def quote_present(self):
        if self.quote:
            return True
        return False


class Category(models.Model):
    forum = models.ForeignKey(Forum)
    name = models.CharField(max_length=60)
    created_on = models.DateTimeField()
    dp = models.ImageField(upload_to='forum_dps', null=True)
    description = models.CharField(max_length=200, null=True)
    detail = models.TextField(null=True)

    def __str__(self):
        return self.name


class Board(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=60)
    created_on = models.DateTimeField()
    dp = models.ImageField(upload_to='forum_dps', null=True)
    description = models.CharField(max_length=200, null=True)
    detail = models.TextField(null=True)
    last_thread_on = models.DateTimeField(null=True)

    def __str__(self):
        return self.name


class Thread(models.Model):
    NORMAL = 'NM'
    PINNED = 'PN'
    ANNOUNCEMENT = 'AM'
    THREAD_TYPE_CHOICES = (
        (NORMAL, 'Normal'),
        (PINNED, 'Pinned'),
        (ANNOUNCEMENT, 'Announcement')
    )
    board = models.ForeignKey(Board)
    started_on = models.DateTimeField()
    title = models.CharField(max_length=170)
    creator = models.ForeignKey(User, related_name='created_threads')
    thread_type = models.CharField(
        max_length=2,
        choices=THREAD_TYPE_CHOICES,
        default=NORMAL
    )
    views = models.IntegerField(default=0)
    last_post_on = models.DateTimeField()
    last_post_by = models.ForeignKey(User)
    post_count = models.IntegerField(default=1)

    def __str__(self):
        return self.title


class Post(models.Model):
    thread = models.ForeignKey(Thread)
    author = models.ForeignKey(User)
    content = models.TextField()
    post_time = models.DateTimeField()

    def __str__(self):
        return self.content[:50]

    def save(self):
        self.clean_content()
        super().save()

    def clean_content(self):
        words = self.content.split(' ')
        newcont = []
        for word in words:
            if len(word) > 80:
                new_words = [word[x:x+40] for x in range(0, len(word), 40)]
                newcont.extend(new_words)
            else:
                newcont.append(word)
        words = list(' '.join(newcont))
        newcont = []
        for word in words:
            # if word == '\n':
                # newcont.append('<br />')
            # elif word == ' ':
                # newcont.append('&nbsp')
            # else:
            newcont.append(word)
        self.content = ''.join(newcont) + '&nbsp '*300
        lines = self.content.split('\n')
        self.content = '<br>'.join(lines)

    def get_dp_url(self):
        profile = self.author.rootprofile
        return profile.avatar.url

    def get_karma(self):
        threads = Thread.objects.filter(creator=self.author)
        pts = 0
        for thread in threads:
            pts += thread.post_set.exclude(author=self.author).count()
        pts += Post.objects.filter(author=self.author).count()
        return pts


class PostFile(models.Model):
    post = models.ForeignKey(Post)
    name = models.CharField(max_length=20)
    content = models.FileField(upload_to='forum_post_files')

    def __str__(self):
        return self.name


class Rating(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]
    post = models.ForeignKey(Post)
    rater = models.ForeignKey(User)
    rating_point = models.SmallIntegerField(choices=RATING_CHOICES)
