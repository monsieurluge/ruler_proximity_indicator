from functools import reduce
import sublime
import sublime_plugin


def closest(a, b):
    return a if abs(a) <= abs(b) else b


def indicator(proximity):
    index  = min(6, max(0, proximity + 3))
    cursor = '╬' if index == 3 else '═'
    return replace_char('───┼───', cursor, index)


def replace_char(text, char, index):
    return text[:index] + char + text[index+1:]


class RulerProximityIndicator(sublime_plugin.EventListener):
    rulers = [80]

    def on_activated(self, view):
        settings = sublime.load_settings('Preferences.sublime-settings')
        if not settings.get('rulers') is None:
            self.rulers = settings.get('rulers')

    def on_selection_modified(self, view):
        current_line_point  = view.sel()[0].begin()
        line_length         = view.line(current_line_point).size()
        proximity_to_rulers = map(lambda r: (line_length - r), self.rulers)
        closest_one         = reduce(closest, proximity_to_rulers, 1000)
        view.set_status('proximity_indicator', indicator(closest_one))
