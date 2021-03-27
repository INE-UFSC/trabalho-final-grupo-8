import PySimpleGUI as sg
# Very basic window. Return values as a list
layout = [
 [sg.Text('Bem vindo ao JOGO DA ORDENAÇÃO!!!', background_color='black', )],

 [sg.Text('Name: ', size=(15, 1), background_color='black'), sg.InputText(background_color='gray')],

 [sg.Text('Selecione a dificuldade:', background_color='black'),
  sg.InputCombo(("1", "2", "3", "4"), background_color='gray', default_value="1")],

 [sg.Text('Selecione o modo de jogo:', background_color='black'),
  sg.Radio("tempo", "tempo", background_color='black'), sg.Radio("movimentos", "movimentos", background_color='black')],

 [sg.ReadFormButton("", button_color='black', image_filename="images.png", image_size=(55, 80))]
 ]
window = sg.Window('JOGO DA ORDENAÇÃO', background_color='black').Layout(layout)
button, values = window.Read()
sg.Popup(button, values)