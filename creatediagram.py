import json
from PIL import Image, ImageDraw, ImageFont

# positions of the items (the drawings of the water use sectors) as pixel value in reference to the background diagram
posit = {
    "electricity": (1410, 1390),
    "manufacturing": (1730, 1350),
    "irrigation": (2160, 1465),
    "livestock": (2480, 1510),
    "domestic": (2910, 1570),
    "ar_wateruse": (1690, 390),
    "reservoir": (1605, 785),
    "lake": (2085, 901),
    "river": (2637, 1074),
    "wetland": (3040, 1050),
    "discharge": (3651, 1179),
    "ar_discharge": (3740, 1235),
    "canopy": (210, 1050),
    "glacier": (975, 480),
    "shortwave": (75, 125),
    "longwave": (190, 125),
    "temperature": (290, 125),
    "wind": (50, 410),
    "humidity": (180, 390),
    "pressure": (280, 400),
    "precipitation": (70, 520),
    "ar_gw_abstraction": (2000, 1690),
    "ar_soil_retflow": (2070, 1700),
    "ar_gw_retflow": (2125, 1710),
    "ar_abs_reservoir": (1600, 1160),
    "ar_retflow_reservoir": (1655, 1185),
    "ar_abs_lake": (2120, 1180),
    "ar_retflow_lake": (2175, 1210),
    "ar_abs_river": (2715, 1135),
    "ar_retflow_river": (2770, 1155),
    "ar_canopy_evaporation": (420, 760),
    "ar_caprise": (500, 1960),
    "ar_glacier_sublim": (1060, 200),
    "ar_lake": (2380, 780),
    "ar_reservoir": (2080, 660),
    "ar_river": (2850, 880),
    "ar_wetland": (3360, 910),
    "ar_soil_evapo": (730, 1250),
    "ar_transpiration": (250, 900),
    "ar_snow_sublim": (720, 480),
    "ar_gwr": (600, 1960),
    "ar_throughfall": (330, 1280),
    "ar_infiltration": (330, 1560),
    "ar_glacierrunoff": (1150, 530),
    "ar_runoff": (1300, 410),
    "ar_snowmelt": (600, 750)
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
    "River discharge": (7770, 1115),
    "Canopy storage": (1100, 1170),
    "Glacier storage": (2130, 510),
    "Total precipitation": (540, 230),
    "Rainfall": (520, 340),
    "Snowfall": (730, 340),
    "Soil storage": (2630, 2100),
    "Groundwater storage": (2500, 2450),
    "Capillary rise": (800, 2020),
    "Soil evaporation": (1830, 1380),
    "Transpiration": (120, 840),
    "Canopy evaporation": (900, 650),
    "Snow sublimation": (1200, 530),
    "Glacier sublimation": (2500, 280),
    "Groundwater recharge": (1600, 2020),
    "Throughfall": (80, 1330),
    "Infiltration": (105, 1580),
    "Glacier runoff": (1350, 600),
    "Total runoff": (1350, 400),
    "Snow melt": (670, 690),
    "Snow storage": (1700, 560),
    "CO2 effect": (25, 1000)
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
    "River discharge": True,
    "Canopy storage": True,
    "Glacier storage": True,
    "Total precipitation": False,
    "Rainfall": False,
    "Snowfall": False,
    "Soil storage": False,
    "Groundwater storage": False,
    "Capillary rise": True,
    "Soil evaporation": True,
    "Transpiration": False,
    "Canopy evaporation": True,
    "Snow sublimation": True,
    "Glacier sublimation": True,
    "Groundwater recharge": True,
    "Infiltration": False,
    "Throughfall": False,
    "Glacier runoff": False,
    "Total runoff": False,
    "Snow melt": False,
    "Snow storage": True,
    "CO2 effect": False
}

#for A diagram
posita = {
    "shortwave": (75, 260),
    "longwave": (190, 260),
    "temperature": (290, 260),
    "wind": (50, 530),
    "humidity": (180, 510),
    "pressure": (280, 520),
    "precipitation": (70, 650),
    "A_canopy": (-50, 710),
    "A_ar_canopy_evapo": (360, 920),
    "A_ar_transpiration": (900, 920),
    "A_ar_soil_evapo": (100, 1400),
    "A_ar_throughfall": (300, 1500),
    "A_ar_infiltration": (300, 1800),
    "A_ar_interflow": (1500, 1950),
    "A_ar_gwr": (300, 2170),
    "A_ar_caprise": (500, 2170),
    "A_ar_gw_runoff": (1500, 2450),
    "A_ar_trunoff": (1900, 1720),
    "A_ar_surf_runoff": (1580, 1660),
    "A_ar_glacierrunoff": (1240, 1660),
    "A_ar_snowmelt": (900, 1660),
    "A_ar_snow_sublim": (1420, 1050),
    "A_ar_glacier_sublim": (1560, 1070),
    "A_glacier": (1020, 1475),
    "A_groundwater": (700, 2550),
    "A_snow": (1020, 1280),
    "A_soil": (700, 2090)
}

# positions of the textual items for the water use sectors
postxta = {
    "Glacier storage": (1400, 1420),
    "Total precipitation": (770, 630),
    "Rainfall": (720, 770),
    "Snowfall": (1120, 770),
    "Soil storage": (720, 2000),
    "Groundwater storage": (520, 2430),
    "Capillary rise": (560, 2300),
    "Soil evaporation": (290, 1280),
    "Transpiration": (950, 980),
    "Canopy evaporation": (470, 950),
    "Snow sublimation": (2580, 1070),
    "Glacier sublimation": (3500, 1070),
    "Groundwater recharge": (320, 2160),
    "Infiltration": (70, 1900),
    "Throughfall": (200, 1410),
    "Glacier runoff": (1230, 1710),
    "Total runoff": (4200, 2220),
    "Snow melt": (900, 1710),
    "Snow storage": (1090, 1220),
    "Surface runoff": (1560, 1710),
    "CO2 effect": (550, 880),
    "Canopy storage": (500, 1150),
    "Soil layers:": (800, 2150),
    "Groundwater layers:": (1800, 2610),
    "Glacier layers:": (1090, 1510),
    "Snow layers:": (1090, 1320)
}

# define if text should be wrapped or not
textwrpa = {
    "Glacier storage": False,
    "Total precipitation": False,
    "Rainfall": False,
    "Snowfall": False,
    "Soil storage": False,
    "Groundwater storage": False,
    "Capillary rise": False,
    "Soil evaporation": True,
    "Transpiration": False,
    "Canopy evaporation": True,
    "Snow sublimation": True,
    "Glacier sublimation": True,
    "Groundwater recharge": True,
    "Infiltration": False,
    "Throughfall": False,
    "Glacier runoff": False,
    "Total runoff": True,
    "Snow melt": False,
    "Snow storage": False,
    "Surface runoff": False,
    "CO2 effect": False,
    "Canopy storage": False,
    "Soil layers:": False,
    "Groundwater layers:": True,
    "Glacier layers:": False,
    "Snow layers:": False
}
layatxtpos = {
    "Soil layers": (1060, 2150),
    "Groundwater layers": (1060, 2630),
    "Glacier layers": (1420, 1510),
    "Snow layers": (1380, 1320)
}

def paste_images(moddict, txtdict, modadict, positdict, postxtdict, postxtdictwrap, txtadict, layadict, layatxtpos, positadict, postxtadict, postxtadictwrap, modname):
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
    myFont = ImageFont.truetype('Roboto-Medium.ttf', 50)
    myFonts = ImageFont.truetype('Roboto-Medium.ttf', 35)
    myFontl = ImageFont.truetype('Roboto-Medium.ttf', 80)
    myFonth = ImageFont.truetype('Roboto-Medium.ttf', 120)
    background = Image.open('fig_background/background_main.png', 'r')
    background.paste(Image.open('./fig_items/input_background.png'), (20, 20),
                     Image.open('./fig_items/input_background.png'))
    for key in moddict:
        print(key)
        img = Image.open('./fig_items/' + key + '_' + str(moddict[key]) + '.png', 'r')
        offset = positdict[key]
        background.paste(img, offset, img)
        background.paste(Image.open('./fig_items/legend.png'),  (50, 2620), Image.open('./fig_items/legend.png'))
        imgtxt = ImageDraw.Draw(background)
        imgtxt.text((3400, 100), modname, font=myFonth, fill="black")
    for key, value in txtdict.items():
        txtpos = postxtdict[key]
        txtwrp = postxtdictwrap[key]
        if txtwrp:
            lines = key.rsplit(' ')
            y_text = txtpos[1]
            for line in lines:
                x0, y0, x1, y1 = myFont.getbbox(line)
                if key == "Soil storage" or key == "Groundwater storage":
                    imgtxt.text(((txtpos[0] - (x1 - x0)) / 2, y_text), line, font=myFontl, fill=value)
                    y_text += (y1 - y0)
                else:
                    imgtxt.text(((txtpos[0] - (x1 - x0)) / 2, y_text), line, font=myFont, fill=value)
                    y_text += (y1 - y0)
        else:
            if key == "CO2 effect":
                imgtxt.text(txtpos, "CO", font=myFont, fill=value)
                imgtxt.text((90, 1025), "2", font=myFonts, fill=value)
                imgtxt.text((120, 1000), "effect", font=myFont, fill=value)
            elif key == "Soil storage" or key == "Groundwater storage":
                imgtxt.text(txtpos, key, font=myFontl, fill=value)
            else:
                imgtxt.text(txtpos, key, font=myFont, fill=value)

    background.save(modname + '.png')

    background = Image.open('fig_background/background_a.png', 'r')
    background.paste(Image.open('./fig_items/input_background.png'), (20, 150),
                     Image.open('./fig_items/input_background.png'))
    for key in modadict:
        print(key)
        img = Image.open('./fig_items/' + key + '_' + str(modadict[key]) + '.png', 'r')
        offset = positadict[key]
        background.paste(img, offset, img)
        imgtxt = ImageDraw.Draw(background)
        imgtxt.text((1530, 50), modname, font=myFonth, fill="black")
    for key, value in txtadict.items():
        txtpos = postxtadict[key]
        txtwrp = postxtadictwrap[key]
        if txtwrp:
            lines = key.rsplit(' ')
            y_text = txtpos[1]
            for line in lines:
                x0, y0, x1, y1 = myFont.getbbox(line)
                if key == "Soil storage" or key == "Groundwater storage":
                    imgtxt.text(((txtpos[0] - (x1 - x0)) / 2, y_text), line, font=myFontl, fill=value)
                    y_text += (y1 - y0)
                else:
                    imgtxt.text(((txtpos[0] - (x1 - x0)) / 2, y_text), line, font=myFont, fill=value)
                    y_text += (y1 - y0)
        else:
            if key == "CO2 effect":
                imgtxt.text(txtpos, "CO", font=myFont, fill=value)
                imgtxt.text((617, 905), "2", font=myFonts, fill=value)
                imgtxt.text((650, 880), "effect", font=myFont, fill=value)
            elif key == "Soil storage" or key == "Groundwater storage":
                imgtxt.text(txtpos, key, font=myFontl, fill=value)
            else:
                imgtxt.text(txtpos, key, font=myFont, fill=value)
    for key, value in layadict.items():
        txtpos = layatxtpos[key]
        if int(value) > 0:
            imgtxt.text(txtpos, value, font=myFont, fill='#0062FF')
        else:
            imgtxt.text(txtpos, value, font=myFont, fill='#929497')

    background.save(modname + '_A.png')

# read in the setup for the model(s)
mod = open('modelsetup.json', 'r')
config = json.load(mod)
# iterate over the models and call the function to create the diagram
for model in config["Model"]:
    mod = model['items_main']
    txt = model['text_main']
    moda = model['items_a']
    txta = model['text_a']
    laya = model['layers_a']
    modname = model['model']['name']
    paste_images(mod, txt, moda, posit, postxt, textwrp, txta, laya, layatxtpos, posita, postxta, textwrpa, modname)
