import json
from ast import literal_eval as make_tuple
from PIL import Image, ImageDraw, ImageFont

# positions of the items (the drawings of the water use sectors) as pixel value in reference to the background diagram
posit = {
    "manufacturing": (1730, 1380),
    "agriculture": (2160, 1490),
    "livestock": (2480, 1535),
    "domestic": (2910, 1570)
}

# positions of the textual items for the water use sectors
postxt = {
    "manufacturing sector": (3990, 1330),
    "agriculture sector": (4950, 1370),
    "livestock sector": (5600, 1420),
    "domestic sector": (6200, 1460)
}

# define if text should be wrapped or not
textwrp = {
    "manufacturing sector": True,
    "agriculture sector": True,
    "livestock sector": True,
    "domestic sector": True
}


def paste_images(moddict, txtdict, positdict, postxtdict, postxtdictwrap, modname):
    """
    adds the single items to the background image
    :param moddict: model definition(s)
    :param txtdict: corresponding texts
    :param positdict: predefined positions of items
    :param postxtdict: predefined positions of text
    :param postxtdictwrap: predefined wrap allowance
    :param modname: name of the model(s)
    :return: a stored png of the model with modname as file name
    """
    background = Image.open('./fig_background/background.png', 'r')
    for key in moddict:
        img = Image.open('./fig_wateruse/' + key + '_' + moddict[key] + '.png', 'r')
        offset = positdict[key]
        background.paste(img, offset, img)
    imgtxt = ImageDraw.Draw(background)
    #font is not provided in repository due to avoid licensing issues.
    myFont = ImageFont.truetype('segoeui.ttf', size=50)
    for key, value in txtdict.items():
        txtpos = postxtdict[key]
        txtwrp = postxtdictwrap[key]
        if txtwrp:
            lines = key.rsplit(' ')
            y_text = txtpos[1]
            for line in lines:
                x0, y0, x1, y1 = myFont.getbbox(line)
                imgtxt.text(((txtpos[0] - (x1 - x0)) / 2, y_text), line, font=myFont, size=50, fill=make_tuple(value))
                y_text += (y1 - y0)
        else:
            imgtxt.text(txtpos, key, font=myFont, fill=(255, 0, 0))

    background.save(modname + '.png')


# read in the setup for the model(s)
#mod = open('modelsetup.json', 'r')
mod = open('modelsetup.json', 'r')
data = json.load(mod)
# iterate over the models and call the function to create the diagram
for model in data["Model"]:
    mod = model['items']
    txt = model['text']
    modname = model['model']['name']
    paste_images(mod, txt, posit, postxt, textwrp, modname)