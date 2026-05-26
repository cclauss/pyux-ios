import ux

@ux.in_background
def show_value(sender):
    print(slide.value)
    
view = ux.View()
view.name = 'Slider'
view.frame = (0, 0, 580, 620)
view.background_color = 'cyan'

btn = ux.Button(title='show value')
btn.name = 'btnpopup'
btn.frame = (10, 10, 120, 40)
btn.background_color = 'lightgray'
btn.action = show_value
view.add_subview(btn)

slide = ux.Slider()
slide.frame = (10, 80, 320, 40)
slide.value = 0.5
slide.action = show_value
view.add_subview(slide)

#view.present('sheet', title_bar_color='white', title_color='black', hide_title_bar=False)
view.present('sheet', title_bar_color='black', title_color='white', right_close_button=True)


