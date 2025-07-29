def explain_command(cmd):
    explanations = {
        "ls -l": "Lists files in long format (permissions, size, date)",
        "df -h": "Shows disk space usage in human-readable format",
        "ps aux": "Shows running processes with details",
        "free -h": "Displays memory usage in human-readable format"
    }
    return explanations.get(cmd, "No explanation available.")
