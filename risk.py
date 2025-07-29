def assess_risk(command):
    high_risk = ["rm", "dd", "mkfs", ":(){ :|:& };:", "shutdown", "reboot"]
    score = 1

    for risky in high_risk:
        if risky in command:
            score = 9
            break
    if "sudo" in command:
        score = max(score, 7)
    elif "mv" in command or "cp" in command:
        score = max(score, 5)

    level = risk_label(score)
    return score, level

def risk_label(score):
    if score <= 2:
        return "Safe"
    elif score <= 4:
        return "Low Risk"
    elif score <= 6:
        return "Medium Risk"
    elif score <= 8:
        return "High Risk"
    else:
        return "Extreme Risk"
