import ollama
import re
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt

console = Console()

# ----------------------------
# Risk Scoring System
# ----------------------------
def assess_risk(command):
    command = command.strip()

    if re.match(r'^\s*(ls|pwd|whoami|uptime|date|cal|cat|echo|ip a|ip addr|df -h|du -sh|free -h|top|ps)', command):
        return 0, "Safe: Read-only or informational command."
    elif re.match(r'^\s*(cd|touch|mkdir|mv|cp|nano|vim)', command):
        return 3, "Low Risk: File or directory operations in user space."
    elif re.match(r'^\s*(ping|wget|curl|netstat|ifconfig|ip|systemctl status)', command):
        return 5, "Medium Risk: Network or system query operations."
    elif re.match(r'^\s*(apt install|yum install|chmod|chown|systemctl start|systemctl stop|ufw)', command):
        return 7, "High Risk: System modifications or permission changes."
    elif re.match(r'^\s*(rm|mkfs|dd|reboot|shutdown|init|mount|umount|kill -9|userdel)', command):
        return 9, "Extreme Risk: Can delete files or affect system stability."

    return 6, "Moderate Risk: Command not explicitly categorized, review before running."

def color_risk_score(score):
    if score <= 2:
        return Text(str(score), style="bold green")
    elif score <= 4:
        return Text(str(score), style="bold yellow")
    elif score <= 6:
        return Text(str(score), style="bold orange3")
    elif score <= 8:
        return Text(str(score), style="bold red")
    else:
        return Text(str(score), style="bold red on white")

# ----------------------------
# Extract up to 3 commands
# ----------------------------
def extract_valid_commands(response_text):
    lines = response_text.strip().split('\n')
    commands = []
    for line in lines:
        if re.match(r'^\s*(ls|cd|df|du|echo|cat|grep|find|ps|top|pwd|mkdir|rm|touch|chmod|chown|mv|cp|ifconfig|ip|uptime|whoami|date|cal|ping|curl|wget)', line.strip()):
            commands.append(line.strip())
    return commands[:3]  # Limit to 3

# ----------------------------
# Shell Command Translator
# ----------------------------
def translate_to_shell(prompt):
    console.print("[bold green]Translating your request...[/bold green]")

    response = ollama.chat(
        model='phi',
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a Linux shell assistant. Convert vague or general natural language into up to 3 possible "
                    "single-line POSIX shell commands. Reply ONLY with the commands, each on a new line, no markdown or extra explanation."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    raw_output = response['message']['content']
    commands = extract_valid_commands(raw_output)

    if not commands:
        console.print("[bold red]Model Error:[/bold red] No valid shell command found.")
        return None

    # If one suggestion, return directly
    if len(commands) == 1:
        return commands[0]

    # Multiple options — show and prompt user
    console.print(Panel.fit("[bold magenta]I found multiple command suggestions:[/bold magenta]"))
    for i, cmd in enumerate(commands, 1):
        console.print(f"[{i}] {cmd}")

    while True:
        choice = Prompt.ask("Select command number to run (or 'c' to cancel)")
        if choice.lower() == 'c':
            return None
        elif choice.isdigit() and 1 <= int(choice) <= len(commands):
            return commands[int(choice)-1]
        else:
            console.print("[bold red]Invalid choice. Try again.[/bold red]")

# ----------------------------
# Command Execution
# ----------------------------
def run_shell_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.stdout:
            console.print(f"[bold green]Output:[/bold green]\n{result.stdout.strip()}")
        if result.stderr:
            console.print(f"[bold red]Errors:[/bold red]\n{result.stderr.strip()}")
    except Exception as e:
        console.print(f"[bold red]Execution Error:[/bold red] {e}")

# ----------------------------
# Main CLI Loop
# ----------------------------
def main():
    console.print(Panel.fit("[bold cyan]Shell-Assist CLI[/bold cyan]\nType your command in natural language"))

    while True:
        user_input = console.input("[bold yellow]You > [/bold yellow]").strip()
        
        if user_input.lower() in ['exit', 'quit']:
            console.print("[italic red]Exiting...[/italic red]")
            break

        command = translate_to_shell(user_input)
        if not command:
            continue

        # Risk analysis
        score, explanation = assess_risk(command)
        risk_text = color_risk_score(score)

        console.print(Panel.fit(
            f"[bold magenta]Suggested Shell Command:[/bold magenta]\n{command}\n\n"
            f"[bold white]Risk Score:[/bold white] {risk_text} / 10\n"
            f"[bold white]Explanation:[/bold white] {explanation}"
        ))

        confirm = console.input("Do you want to run this command? (y/n): ").strip().lower()

        if confirm == 'y':
            console.print("🟢 Executing command...\n")
            run_shell_command(command)
        else:
            console.print("⚪ Command skipped.")

if __name__ == "__main__":
    main()
