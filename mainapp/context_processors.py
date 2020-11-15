def new_messages_processor(request):
    user = request.user
    unread_chats = user.chat_set.unreaded(user=user)

    return {
        'unread_chats': unread_chats
    }
