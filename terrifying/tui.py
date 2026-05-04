"""TUI for terrifying add — requires textual (pip install terrifying[tui])."""

from __future__ import annotations

from terrifying.policies.library import PolicyEntry


def run_tui(entries: list[PolicyEntry], engine: str) -> list[PolicyEntry]:
    """Launch the policy browser TUI and return selected entries."""
    from textual.app import App, ComposeResult
    from textual.binding import Binding
    from textual.widgets import (
        Checkbox,
        Footer,
        Header,
        Label,
        ListItem,
        ListView,
        RadioButton,
        RadioSet,
        Static,
    )
    from textual.containers import Horizontal, Vertical

    class PolicyBrowserApp(App):
        BINDINGS = [
            Binding("a", "select_all", "Select all"),
            Binding("enter", "confirm", "Add"),
            Binding("q", "quit_no_select", "Quit"),
        ]
        CSS = """
        #left { width: 30%; border-right: solid $primary; }
        #right { width: 70%; }
        #detail { height: 8; border-top: solid $primary; padding: 1; }
        RadioSet { margin: 1; }
        ListView { height: 1fr; }
        """

        def __init__(self, all_entries: list[PolicyEntry], initial_engine: str):
            super().__init__()
            self._all = all_entries
            self._engine = initial_engine
            self._selected_ids: set[tuple[str, str]] = set()
            self._selected_entries: list[PolicyEntry] = []

        def compose(self) -> ComposeResult:
            yield Header()
            with RadioSet(id="engine-select"):
                yield RadioButton("Rego", value=self._engine == "rego", id="rb-rego")
                yield RadioButton("c7n", value=self._engine == "c7n", id="rb-c7n")
                yield RadioButton("Both", value=self._engine == "both", id="rb-both")
            with Horizontal():
                with Vertical(id="left"):
                    yield Label("Tags")
                    yield ListView(id="tag-list")
                with Vertical(id="right"):
                    yield ListView(id="policy-list")
                    yield Static("", id="detail")
            yield Footer()

        def on_mount(self) -> None:
            self._refresh_tags()

        def _visible_entries(self) -> list[PolicyEntry]:
            if self._engine == "both":
                return self._all
            return [e for e in self._all if e.engine == self._engine]

        def _selected_tag(self) -> str | None:
            tag_list = self.query_one("#tag-list", ListView)
            if tag_list.index is not None and tag_list.index >= 0:
                items = list(tag_list.children)
                if tag_list.index < len(items):
                    return items[tag_list.index].query_one(Label).renderable
            return None

        def _filtered_entries(self) -> list[PolicyEntry]:
            visible = self._visible_entries()
            tag = self._selected_tag()
            if tag and str(tag) != "(all)":
                return [e for e in visible if e.has_tag(str(tag))]
            return visible

        def _refresh_tags(self) -> None:
            visible = self._visible_entries()
            tag_counts: dict[str, int] = {}
            for e in visible:
                for t in e.tags:
                    tag_counts[t] = tag_counts.get(t, 0) + 1

            tag_list = self.query_one("#tag-list", ListView)
            tag_list.clear()
            tag_list.append(ListItem(Label("(all)")))
            for tag, count in sorted(tag_counts.items()):
                tag_list.append(ListItem(Label(f"{tag} ({count})")))

            self._refresh_policies()

        def _refresh_policies(self) -> None:
            filtered = self._filtered_entries()
            policy_list = self.query_one("#policy-list", ListView)
            policy_list.clear()
            for e in filtered:
                badge = "[R]" if e.engine == "rego" else "[C]"
                checked = (e.id, e.engine) in self._selected_ids
                item = ListItem(Label(f"{'[x]' if checked else '[ ]'} {badge} {e.id}"))
                policy_list.append(item)

        def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
            label = str(event.pressed.label)
            self._engine = label.lower() if label != "Both" else "both"
            self._refresh_tags()

        def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
            if event.list_view.id == "policy-list":
                filtered = self._filtered_entries()
                idx = event.list_view.index
                if idx is not None and 0 <= idx < len(filtered):
                    e = filtered[idx]
                    detail = self.query_one("#detail", Static)
                    detail.update(
                        f"[bold]{e.id}[/bold] [{e.engine}] [{e.severity}]\n"
                        f"{e.description}\n"
                        f"Resources: {', '.join(e.terraform_resources)}\n"
                        f"Tags: {', '.join(e.tags)}"
                    )
            elif event.list_view.id == "tag-list":
                self._refresh_policies()

        def on_list_view_selected(self, event: ListView.Selected) -> None:
            if event.list_view.id != "policy-list":
                return
            filtered = self._filtered_entries()
            idx = event.list_view.index
            if idx is None or idx >= len(filtered):
                return
            e = filtered[idx]
            key = (e.id, e.engine)
            if key in self._selected_ids:
                self._selected_ids.discard(key)
            else:
                self._selected_ids.add(key)
            self._refresh_policies()

        def action_select_all(self) -> None:
            for e in self._filtered_entries():
                self._selected_ids.add((e.id, e.engine))
            self._refresh_policies()

        def action_confirm(self) -> None:
            self._selected_entries = [
                e for e in self._all if (e.id, e.engine) in self._selected_ids
            ]
            self.exit(self._selected_entries)

        def action_quit_no_select(self) -> None:
            self.exit([])

    app = PolicyBrowserApp(entries, engine)
    result = app.run()
    return result if isinstance(result, list) else []
