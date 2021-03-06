#/**
 #* @file   rss_feed.py
 #* @author Akshay Katre <akshay.k@cern.ch>
 #* @date   Wed Feb 17, 2016
 #*
 #* @brief  A simple shell interface to browse through daily news
 #*
 #*/


import urwid
import feedparser
import pdb 
#from readability.readability import Document
from urllib import urlopen
from goose import Goose 

class MenuButton(urwid.Button):
    def __init__(self, caption, callback):
        super(MenuButton, self).__init__("")
        urwid.connect_signal(self, 'click', callback)
        self._w = urwid.AttrMap(urwid.SelectableIcon(
            [u'  \N{BULLET} ', caption], 2), None, 'selected')

class SubMenu(urwid.WidgetWrap):
    def __init__(self, caption, choices):
        super(SubMenu, self).__init__(MenuButton(
            [caption, u"\N{HORIZONTAL ELLIPSIS}"], self.open_menu))
        line = urwid.Divider(u'\N{LOWER ONE QUARTER BLOCK}')
        listbox = urwid.ListBox(urwid.SimpleFocusListWalker([
            urwid.AttrMap(urwid.Text([u"\n  ", caption]), 'heading'),
            urwid.AttrMap(line, 'line'),
            urwid.Divider()] + choices + [urwid.Divider()]))
        self.menu = urwid.AttrMap(listbox, 'options')

    def open_menu(self, button):
        top.open_box(self.menu, 40)


class Choice(urwid.WidgetWrap):
    def __init__(self, caption):
        super(Choice, self).__init__(
            MenuButton(caption.title, self.item_chosen))
        self.caption = caption.title

    def item_chosen(self, button):
        #pdb.set_trace()
#        response = urwid.Text([u'  You chose ', self.caption, u'\n'])
        response = urwid.Text([find_link(self.caption)])
        done = MenuButton(u'Ok', exit_program)
        response_box = urwid.Filler(response)
#        test= urwid.MainLoop(response_box).run()
#        top.open_box(urwid.AttrMap(response_box, 'options'), 110)
        top.open_box(urwid.WidgetWrap(response_box), 110)
 #       top.final_box((response), 110)
        #top.final_box(response, 110)
def exit_program(key):
    raise urwid.ExitMainLoop()

link = "http://newsrss.bbc.co.uk/rss/newsonline_world_edition/front_page/rss.xml"
feed = feedparser.parse(link)

def find_link(title):
    for entry in feed.entries:
        if entry.title == title:
            read = entry.link
#            html = urlopen(read).read()
#            pdb.set_trace()
#            return Document(html).summary()
            g = Goose()
            article = g.extract(url=read)
            return article.title, article.cleaned_text
    return 'nothing found'

 
menu_top = SubMenu(u'Main Menu', [
    SubMenu(u'BBC', [
        SubMenu(u'Front Page', [
            Choice(entry) for entry in feed.entries
               
#            Choice(u'Terminal'),
        ]),
    ]),
    SubMenu(u'Google', [
        SubMenu(u'Preferences', [
        #                Choice(u'Appearance'),
        ]),
       # Choice(u'Lock Screen'),
    ]),
])

palette = [
    (None,  'light gray', 'black'),
    ('heading', 'black', 'light gray'),
    ('line', 'black', 'light gray'),
    ('options', 'dark gray', 'black'),
    ('focus heading', 'white', 'dark red'),
    ('focus line', 'black', 'dark red'),
    ('focus options', 'black', 'light gray'),
    ('selected', 'white', 'dark blue')]
focus_map = {
    'heading': 'focus heading',
    'options': 'focus options',
    'line': 'focus line'}

class HorizontalBoxes(urwid.Columns):
    def __init__(self):
        super(HorizontalBoxes, self).__init__([], dividechars=1)

    def open_box(self, box, size):
        if self.contents:
            del self.contents[self.focus_position + 1:]
        self.contents.append((urwid.AttrMap(box, 'options', focus_map),
            self.options('given', size)))
        self.focus_position = len(self.contents) - 1

    def final_box(self, box, size):
        if self.contents:
            del self.contents[self.focus_position + 1:]
       # pdb.set_trace()
        self.contents.append((urwid.AttrMap(box, 'options', focus_map),
            self.options('given', size)))
        self.focus_position = len(self.contents) - 1


def show_or_exit(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()
#    txt.set_text(repr(key))

top = HorizontalBoxes()
top.open_box(menu_top.menu, 30)
urwid.MainLoop(urwid.Filler(top, 'top', 60), palette, unhandled_input=show_or_exit).run()
