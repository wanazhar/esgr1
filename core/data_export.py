import pandas as pd
from rich.console import Console

class DataExporter:
    def __init__(self):
        self.console = Console()

    def to_excel(self, data: dict, filename: str):
        try:
            df = pd.DataFrame(data['metrics'])
            df.to_excel(filename, index=False)
            self.console.print(f"[green]Successfully exported to {filename}[/]")
        except Exception as e:
            self.console.print(f"[red]Export failed: {str(e)}[/]")