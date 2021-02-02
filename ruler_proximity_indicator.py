from functools import reduce
import sublime
import sublime_plugin


def closest(a, b):
    return a if abs(a) <= abs(b) else b


def current_line(view):
    line_point = view.sel()[0].begin()
    line_length = view.line(line_point).size()
    line_number = view.rowcol(line_point)[0]
    return {'length': line_length, 'number': line_number}


def indicator(proximity):
    index = min(6, max(0, proximity + 3))
    cursor = '╬' if index == 3 else '═'
    return replace_char('───┼───', cursor, index)


def replace_char(text, char, index):
    return text[:index] + char + text[index+1:]


class RulerProximityIndicator(sublime_plugin.EventListener):
    rulers = [80]
    last_line = {'length': 0, 'number': 0}

    def _update_rulers(self):
        settings = sublime.load_settings('Preferences.sublime-settings')
        if settings.get('rulers') is None:
            return
        self.rulers = settings.get('rulers')

    def _update_status(self, view):
        line = current_line(view)
        if line == self.last_line:
            return
        self.last_line = line
        proximity_to_rulers = map(lambda r: (line['length'] - r), self.rulers)
        closest_one = reduce(closest, proximity_to_rulers, 1000)
        view.set_status('proximity_indicator', indicator(closest_one))

    def on_activated(self, view):
        self._update_rulers()
        self._update_status(view)

    def on_selection_modified_async(self, view):
        self._update_status(view)
