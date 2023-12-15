import ffstats

def handle_response(message):
    p_message = message

    if p_message == "!help":
        return "`Enter a full NFL team name`"
    
    if p_message == "hello":
        return "Hey there!"
    
    return ffstats.get_player_info(p_message)

print(handle_response("Tyler Boyd"))                                               