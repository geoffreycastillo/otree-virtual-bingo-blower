def find_human_colour(colour_css):
    colours = ['Red', 'Blue', 'Green', 'Yellow', 'Pink', 'Violet']
    for colour in colours:
        if colour_css.endswith(colour):
            human_colour = colour
        if colour_css == 'Gold':
            human_colour = 'Yellow'

    return human_colour