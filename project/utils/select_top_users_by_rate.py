def select_top_users_by_rate(users, top_size):
    if top_size <= 0:
        return []

    result = list(users)

    for i in range(len(result)):
        for j in range(0, len(result) - i - 1):
            if result[j].rate < result[j + 1].rate:
                result[j], result[j + 1] = result[j + 1], result[j]

    top_users = []
    for i in range(min(top_size, len(result))):
        top_users.append(result[i])

    return top_users
