"""Check saved files independently against control properties read from the live browser."""
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit, unquote


class InspectPage(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.controls, self.links, self.text, self.ignore = [], [], [], 0
        self.select = None
        self.scripts = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('style', 'title', 'script'):
            self.ignore += 1
        if tag == 'script':
            self.scripts += 1
        if tag == 'a':
            self.links.append(attrs.get('href', ''))
        if tag == 'select':
            self.select = {'tag': tag, 'attrs': attrs, 'options': []}
            self.controls.append(self.select)
        elif tag == 'option' and self.select is not None:
            self.select['options'].append(attrs)
        elif tag in ('input', 'textarea', 'button'):
            self.controls.append({'tag': tag, 'attrs': attrs})

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag in ('style', 'title', 'script'):
            self.ignore -= 1
        if tag == 'select':
            self.select = None

    def handle_data(self, text):
        if not self.ignore:
            self.text.append(text)


def normalized(parts):
    return re.sub(r'\s+', ' ', ' '.join(parts)).strip()


def main():
    output = Path(__file__).resolve().parents[1] / 'rendered'
    captures = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    note = 'Saved view · controls show captured values and are read-only. KB links open other saved pages.'
    all_controls, all_links = 0, 0
    for capture in captures:
        saved = (output / capture['file']).read_text(encoding='utf-8')
        parsed, original = InspectPage(), InspectPage()
        parsed.feed(saved)
        original.feed(capture['body'])
        assert parsed.scripts == 0
        assert normalized(parsed.text) == normalized([note, *original.text]), capture['route'] + ': visible text changed'
        assert len(parsed.controls) == len(capture['fields'])
        for actual, expected in zip(parsed.controls, capture['fields']):
            assert actual['tag'] == expected['tag']
            if actual['tag'] == 'select':
                assert 'disabled' in actual['attrs']
                selected = [o.get('value') for o in actual['options'] if 'selected' in o]
                assert selected == [o['value'] for o in expected['options'] if o['selected']], (capture['route'], selected)
                assert selected == [expected['value']]
            elif actual['tag'] == 'input':
                assert actual['attrs'].get('value') == expected['value']
                assert 'readonly' in actual['attrs'] or 'disabled' in actual['attrs']
            else:
                assert 'disabled' in actual['attrs']
            all_controls += 1
        for href in parsed.links:
            parts = urlsplit(href)
            if not parts.scheme and not parts.netloc and parts.path:
                assert not parts.path.startswith('/'), href
                target = (output / unquote(parts.path)).resolve()
                assert target.parent == output.resolve(), href
                assert target.is_file(), href
                all_links += 1
        assert re.findall(r'<svg\b[\s\S]*?</svg>', saved) == re.findall(r'<svg\b[\s\S]*?</svg>', capture['body']), 'SVG markup changed'
    print(f'PASS: {len(captures)} pages, {all_controls} captured controls and {all_links} local links; all captured values, visible text and SVG preserved; controls read-only.')


if __name__ == '__main__':
    main()
