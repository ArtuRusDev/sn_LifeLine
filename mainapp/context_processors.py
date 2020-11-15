def new_messages_processor(request):
    user = request.user
    unread_dialogs = user.chat_set.unreaded(user=user).count()
    return {'unread_dialogs': unread_dialogs}
