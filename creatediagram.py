import json
from ast import literal_eval as make_tuple
from PIL import Image, ImageDraw, ImageFont

# positions of the items (the drawings of the water use sectors) as pixel value in reference to the background diagram
posit = {
    "electricity": (1410, 1390),
    "manufacturing": (1730, 1350),
    "irrigation": (2160, 1470),
    "livestock": (2480, 1515),
    "domestic": (2910, 1570),
    "wateruse_arrow": (1690, 390),
    "runoff": (974, 837),
    "reservoir": (1614, 779),
    "lake": (2097, 896),
    "river": (2650, 1070),
    "wetland": (3053, 1046),
    "discharge": (3664, 1175)
}

# positions of the textual items for the water use sectors
postxt = {
    "Electricity sector": (3150, 1290),
    "Manufacturing sector": (4000, 1330),
    "Irrigation sector": (4950, 1380),
    "Livestock sector": (5600, 1420),
    "Domestic sector": (6200, 1460),
    "Water consumption": (2200, 300),
    "Reservoir storage": (3660, 1000),
    "Dam": (2050, 1048),
    "Lake storage": (4800, 1020),
    "River storage": (5955, 980),
    "Wetland storage": (6990, 1180),
    "River discharge": (7770, 1115)
}

# define if text should be wrapped or not
textwrp = {
    "Electricity sector": True,
    "Manufacturing sector": True,
    "Irrigation sector": True,
    "Livestock sector": True,
    "Domestic sector": True,
    "Water consumption": False,
    "Reservoir storage": True,
    "Dam": False,
    "Lake storage": True,
    "River storage": True,
    "Wetland storage": True,
    "River discharge": True
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
    background = Image.open('fig_background/background_main_plain.png', 'r')
    for key in moddict:
        print(key)
        img = Image.open('./fig_items/' + key + '_' + str(moddict[key]) + '.png', 'r')
        offset = positdict[key]
        background.paste(img, offset, img)
    background.paste(Image.open('./fig_items/legend.png'),  (50, 2620), Image.open('./fig_items/legend.png'))
    imgtxt = ImageDraw.Draw(background)
    myFont = ImageFont.truetype('Roboto-Medium.ttf', size=50)
    for key, value in txtdict.items():
        txtpos = postxtdict[key]
        txtwrp = postxtdictwrap[key]
        if txtwrp:
            lines = key.rsplit(' ')
            y_text = txtpos[1]
            for line in lines:
                x0, y0, x1, y1 = myFont.getbbox(line)
                imgtxt.text(((txtpos[0] - (x1 - x0)) / 2, y_text), line, font=myFont, size=50, fill=value)
                y_text += (y1 - y0)
        else:
            imgtxt.text(txtpos, key, font=myFont, size=50, fill=value)

    background.save(modname + '.png')

# read in the setup for the model(s)
mod = open('modelsetup.json', 'r')
config = json.load(mod)
# iterate over the models and call the function to create the diagram
for model in config["Model"]:
    mod = model['items']
    txt = model['text']
    modname = model['model']['name']
    paste_images(mod, txt, posit, postxt, textwrp, modname)