from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress

class TerminalUI:
    def __init__(self):
        self.console = Console()
        
    def display_menu(self, options: list) -> str:
        self.console.clear()
        self.console.print(Panel.fit("[bold cyan]Global ESG Intelligence Platform[/]", 
                                subtitle="[yellow]v3.0 • Multi-Market Support[/]"))
        
        table = Table(show_header=False, padding=(0, 4))
        for i, (text, _) in enumerate(options, 1):
            table.add_row(f"[bold green]{i}.[/]", text)
        self.console.print(table)
        
        return input("\nEnter your choice: ")

    def display_esg(self, data: dict):
        table = Table(title=f"ESG Data for {data['company']}", 
                    title_style="bold magenta")
        
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        table.add_column("Source", style="yellow")
        table.add_column("Last Updated", style="blue")

        for metric in data['metrics']:
            table.add_row(*metric.values())

        self.console.print(table)

    def show_loading(self, message: str):
        with Progress() as progress:
            task = progress.add_task(f"[cyan]{message}...", total=100)
            while not progress.finished:
                progress.update(task, advance=0.5)