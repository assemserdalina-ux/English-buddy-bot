user_stats = {}

def update_stats(user_id, module_num, score, total):
    stats_for_user = user_stats.setdefault(user_id, {})
    m = stats_for_user.setdefault(
        module_num,
        {"attempts": 0, "best": 0, "last": 0, "total": total},
    )
    m["attempts"] += 1
    m["last"] = score
    m["total"] = total
    if score > m["best"]:
        m["best"] = score


def format_progress(user_id):
    if user_id not in user_stats or not user_stats[user_id]:
        return "📊 You haven't completed any quizzes yet."

    lines = ["📊 Your Progress:"]
    for module, data in user_stats[user_id].items():
        lines.append(
            f"• Module {module}: "
            f"attempts: {data['attempts']}, "
            f"best: {data['best']}/{data['total']}, "
            f"last: {data['last']}/{data['total']}"
        )

    return "\n".join(lines)

