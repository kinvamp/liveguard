from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, RichLog, Input, Label
from ..backend.engine import trigger_manual_backup
import os

class LiveGuardApp(App):
    TITLE = "LiveGuard"
    
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Label("Target Project Folder Path:")
        yield Input(value=os.getcwd(), id="input_path")
        yield Button("Run Manual Backup", id="btn_manual", variant="success")
        yield RichLog(id="console_log", highlight=True, markup=True)
        yield Footer()

    def on_mount(self) -> None:
        log = self.query_one("#console_log", RichLog)
        log.write("System Ready. Enter or paste your project path above.")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_manual":
            log = self.query_one("#console_log", RichLog)
            
            target_dir = self.query_one("#input_path", Input).value
            target_dir = os.path.abspath(target_dir.strip())
            
            if not os.path.exists(target_dir):
                log.write(f"[bold red]❌ Error: That folder path does not exist![/bold red]")
                return

            log.write(f"[bold yellow]Locating: {target_dir}[/bold yellow]")
            
            parent_dir = os.path.dirname(target_dir)
            
            success, message = trigger_manual_backup(target_dir, parent_dir)
            
            if success:
                log.write(f"[bold green]✅ {message}[/bold green]")
            else:
                log.write(f"[bold red]❌ {message}[/bold red]")