from core.esg_engine import ESGEngine
from core.terminal_ui import TerminalUI
from core.data_export import DataExporter
import sys

class ESGApp:
    def __init__(self):
        self.engine = ESGEngine()
        self.ui = TerminalUI()
        self.exporter = DataExporter()
        
    def run(self):
        while True:
            choice = self.ui.display_menu([
                ("View ESG Data", "1"),
                ("Export Report", "2"),
                ("Cross-Market Analysis", "3"),
                ("Exit", "4")
            ])
            
            if choice == '1':
                self.view_data_flow()
            elif choice == '2':
                self.export_flow()
            elif choice == '3':
                self.cross_analysis()
            elif choice == '4':
                sys.exit()
            else:
                self.ui.console.print("[red]Invalid choice![/]")

    def view_data_flow(self):
        country = input("Enter country code (e.g., MY, US): ").upper()
        ticker = input("Enter ticker (e.g., MAYBANK.KL, AAPL.US): ")
        
        self.ui.show_loading("Fetching ESG Data")
        data = self.engine.get_esg_data(country, ticker)
        
        if 'error' in data:
            self.ui.console.print("[red]Failed to fetch data[/]")
        else:
            self.ui.display_esg(data)

if __name__ == "__main__":
    ESGApp().run()