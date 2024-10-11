from django.contrib import admin
from .models import Article, Tag, Comment, MyLink, AboutMe, Technology, View, CommentLike, ArticleLike

admin.site.register(Article)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(MyLink)
admin.site.register(AboutMe)
admin.site.register(Technology)
admin.site.register(View)
admin.site.register(ArticleLike)
admin.site.register(CommentLike)

