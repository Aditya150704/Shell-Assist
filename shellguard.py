from rich.console import Console
from rich.prompt import Prompt
from parser import parse_input
from explainer import explain_command
from risk import assess_risk

console = Console()

def main():
    console.print("[bold cyan]ShellGuard CLI[/bold cyan] - Safe Shell Assistant 🔐")

    while True:
        user_input = Prompt.ask("\n💬 Enter natural language command (or type 'exit')")
        if user_input.lower() in ['exit', 'quit']:
            break

        shell_command = parse_input(user_input)
        explanation = explain_command(shell_command)
        risk_score, risk_level = assess_risk(shell_command)

        console.print(f"\n🧠 [bold]Command:[/bold] {shell_command}")
        console.print(f"📖 [bold]Explanation:[/bold] {explanation}")
        console.print(f"⚠️ [bold]Risk Score:[/bold] {risk_score}/10 - {risk_level}")

        if risk_score >= 7:
            console.print("[red bold]This command is dangerous![/red bold] Are you sure?")
        run = Prompt.ask("🚀 Run this command?", choices=["yes", "no"], default="no")

        if run == "yes":
            console.print("[green]Running command... (mock for now)[/green]")
            # subprocess.run(shell_command, shell=True)  ← add later
        else:
            console.print("[yellow]Command aborted.[/yellow]")

if __name__ == "__main__":
    main()
