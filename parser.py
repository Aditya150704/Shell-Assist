def parse_input(nl_input):
    command_map = {
        "list files": "ls -l",
        "check disk": "df -h",
        "show processes": "ps aux",
        "show memory": "free -h"
    }
    return command_map.get(nl_input.lower(), "echo 'Command not recognized'")
