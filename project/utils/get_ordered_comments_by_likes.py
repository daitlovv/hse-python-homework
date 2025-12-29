def get_ordered_comments_by_likes(comments):
    result = list(comments)

    for i in range(len(result)):
        for j in range(0, len(result) - i - 1):
            if result[j].like_count < result[j + 1].like_count:
                result[j], result[j + 1] = result[j + 1], result[j]

    return result
