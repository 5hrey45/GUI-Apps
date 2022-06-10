import PySimpleGUI as sg
from pathlib import Path

smileys = [
    'happy', [':)', 'xD', ':D', '<3'],
    'sad', [':(', 'T_T'],
    'other', [':3']
]

smiley_events = smileys[1] + smileys[3] + smileys[5]

theme_menu = ['menu', ['GrayGrayGray',
                       'LightGray1', 'DarkGrey8', 'dark', 'random']]

menu_layout = [
    ['File', ['Open', 'Save', '---', 'Exit']],
    ['Tools', ['Word Count']],
    ['Add', smileys],
    ['Themes', theme_menu[1]]
]


def create_window(theme):
    sg.theme(theme)
    layout = [
        [sg.Menu(menu_layout)],
        [sg.Text('Untitled', key='-DOCNAME-')],
        [sg.Multiline(no_scrollbar=True, size=(100, 30), key='-TEXTBOX-')]
    ]

    return sg.Window('Text Editor', layout)


window = create_window('GrayGrayGray')

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == 'Open':
        file_path = sg.popup_get_file('Open', no_window=True)
        if file_path:
            file = Path(file_path)
            window['-TEXTBOX-'].update(file.read_text())
            window['-DOCNAME-'].update(file_path.split('/')[-1])

    if event == 'Save':
        file_path = sg.popup_get_file(
            'Save as', no_window=True, save_as=True) + '.txt'
        file = Path(file_path)
        file.write_text(values['-TEXTBOX-'])
        window['-DOCNAME-'].update(file_path.split('/')[-1])

    if event == 'Exit':
        window.close()

    if event == 'Word Count':
        full_text = values['-TEXTBOX-']
        line_count = len(full_text.split('\n'))
        clean_text = full_text.replace('\n', ' ').split(' ')
        word_count = len(clean_text)
        char_count = len(''.join(clean_text))
        sg.popup(
            f'lines: {line_count}\nwords: {word_count}\ncharacters: {char_count}')

    if event in smiley_events:
        current_text = values['-TEXTBOX-']
        new_text = current_text + ' ' + event
        window['-TEXTBOX-'].update(new_text)

    if event in theme_menu[1]:
        window.close()
        window = create_window(event)

window.close()
