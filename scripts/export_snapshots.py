"""Export DOM read from the live KB; preserve raw SVG/style markup and captured field state."""
import argparse
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re


def set_attr(tag, name, value=None):
    pattern = re.compile(r'\s+' + re.escape(name) + r'(?:\s*=\s*(?:"[^"]*"|\x27[^\x27]*\x27|[^\s>]+))?(?=\s|/?>)', re.I)
    tag = pattern.sub('', tag)
    addition = ' ' + name + ('' if value is None else '="' + html.escape(str(value), quote=True) + '"')
    at = tag.rfind('/>') if tag.endswith('/>') else tag.rfind('>')
    return tag[:at] + addition + tag[at:]


def remove_attr(tag, name):
    return re.sub(r'\s+' + re.escape(name) + r'(?:\s*=\s*(?:"[^"]*"|\x27[^\x27]*\x27|[^\s>]+))?(?=\s|/?>)', '', tag, flags=re.I)


class CaptureExporter(HTMLParser):
    def __init__(self, source, fields, routes):
        super().__init__(convert_charrefs=True)
        self.source, self.fields, self.routes = source, fields, routes
        self.offsets = [0]
        for line in source.splitlines(keepends=True):
            self.offsets.append(self.offsets[-1] + len(line))
        self.edits, self.field_index, self.active_select, self.option_index = [], 0, None, 0

    def absolute_offset(self):
        line, column = self.getpos()
        return self.offsets[line - 1] + column

    def handle_starttag(self, tag, attrs):
        raw = self.get_starttag_text()
        replacement = raw
        attrs = dict(attrs)
        if tag == 'a' and attrs.get('href', '').startswith('/kb'):
            target = attrs['href'].rstrip('/')
            if target not in self.routes:
                raise ValueError(f'No local snapshot for {target}')
            replacement = set_attr(replacement, 'href', self.routes[target])
        if tag in ('select', 'input', 'textarea', 'button'):
            field = self.fields[self.field_index]
            self.field_index += 1
            if field['tag'] != tag:
                raise ValueError('Captured control order differs from DOM markup')
            if tag == 'select':
                self.active_select, self.option_index = field, 0
                replacement = set_attr(replacement, 'disabled')
            elif tag == 'input':
                replacement = set_attr(replacement, 'value', field['value'])
                if field.get('type') in ('checkbox', 'radio'):
                    replacement = remove_attr(replacement, 'checked')
                    if field.get('checked'):
                        replacement = set_attr(replacement, 'checked')
                    replacement = set_attr(replacement, 'disabled')
                else:
                    replacement = set_attr(replacement, 'readonly')
            elif tag == 'button':
                replacement = set_attr(replacement, 'disabled')
            else:
                raise ValueError('Textarea export needs an explicit content-state implementation')
        if tag == 'option' and self.active_select:
            option = self.active_select['options'][self.option_index]
            self.option_index += 1
            replacement = set_attr(remove_attr(replacement, 'selected'), 'value', option['value'])
            if option['selected']:
                replacement = set_attr(replacement, 'selected')
        if replacement != raw:
            self.edits.append((self.absolute_offset(), self.absolute_offset() + len(raw), replacement))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag == 'select':
            if self.option_index != len(self.active_select['options']):
                raise ValueError('Captured option count differs from DOM markup')
            self.active_select = None

    def export(self):
        self.feed(self.source)
        self.close()
        if self.field_index != len(self.fields):
            raise ValueError('Not all captured controls were serialized')
        result = self.source
        for start, end, replacement in sorted(self.edits, reverse=True):
            result = result[:start] + replacement + result[end:]
        return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('captures', type=Path)
    args = parser.parse_args()
    captures = json.loads(args.captures.read_text(encoding='utf-8'))
    output = Path(__file__).resolve().parents[1] / 'rendered'
    output.mkdir(exist_ok=True)
    routes = {page['route']: page['file'] for page in captures}
    state = []
    note = '<aside class="saved-view">Saved view · controls show captured values and are read-only. KB links open other saved pages.</aside>'
    note_css = '.saved-view{max-width:760px;margin:1rem auto 0;padding:.5rem 16px;color:var(--muted);font:13px/1.5 system-ui;}'
    for page in captures:
        body = CaptureExporter(page['body'], page['fields'], routes).export()
        result = '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + html.escape(page['title']) + '</title><style>' + page['css'] + '\n' + note_css + '</style></head><body>' + note + body + '</body></html>'
        (output / page['file']).write_text(result, encoding='utf-8', newline='\n')
        state.append({key: page[key] for key in ('route', 'file', 'title', 'fields')})
        state[-1]['capturedBodySha256'] = hashlib.sha256(page['body'].encode()).hexdigest()
    (output / 'snapshot-state.json').write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(f'Exported {len(captures)} saved pages, captured controls and local KB navigation.')


if __name__ == '__main__':
    main()
