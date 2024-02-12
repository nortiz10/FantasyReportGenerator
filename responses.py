import ffstats

def handle_response(message):
    p_message = message

    if p_message == "!help":
        return "`Enter a full NFL team name`"
    
    return ffstats.get_player_info(p_message)