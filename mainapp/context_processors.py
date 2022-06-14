def new_messages_processor(request):
    user = request.user

    if not user.is_authenticated:
        return {}
    unread_chats = user.chat_set.unreaded(user=user)
    requests = user.friendrequests_set.requests(user=user)

    return {
        'unread_chats': unread_chats,
        'requests': requests
    }
