from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from inspect_ai.log._condense import resolve_sample_attachments
from inspect_ai.log._file import list_eval_logs, read_eval_log, read_eval_log_sample

from ..core.group import group_events
from ..widgets import EventGroupsListView

# textual console
# textual run --dev inspect_ai._ui.logview.logview:LogviewApp


class LogviewApp(App[None]):
    def __init__(
        self, log_file: str | None = None, sample: str | None = None, epoch: int = 1
    ) -> None:
        # call super
        super().__init__()

        # enable resolution of default log file for dev/debug
        if not log_file:
            log_file = list_eval_logs()[0].name

        # resolve eval sample (specifc sample or first one if not specified)
        if sample:
            self.eval_sample = read_eval_log_sample(log_file, sample, epoch)
        else:
            eval_log = read_eval_log(log_file)
            if not eval_log.samples:
                raise ValueError(f"No samples in log file {log_file}")
            self.eval_sample = eval_log.samples[0]

        # resolve event groups
        self.event_groups = group_events(
            resolve_sample_attachments(self.eval_sample).events
        )

    CSS_PATH = "logview.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        yield Header(classes="header")
        yield Footer()
        yield EventGroupsListView(self.event_groups)

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark


if __name__ == "__main__":
    app = LogviewApp()
    app.run()
