def filter_comments_by_author(comments, author):
    return [comment for comment in comments if comment.author_id == author.id]
