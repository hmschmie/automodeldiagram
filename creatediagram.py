# tool to create diagrams for global water cycle based on information of the file modelsetup.json
# on top of a background image, specific content is displayed
# first, the positions of the items is defined. Then, and based on the information of the json file for the
# particular model (true or false), the item from the item folder is drawn. Then, the text is displayed
# in the corresponding font. In case a component is not represented in the model, this component is displayed
# in grey and highlighted with an "x".
# Author: Hannes Müller Schmied, 2024; last updated 2025-01-12

import json
from PIL import Image, ImageDraw, ImageFont

# positions of the items for the Main diagram as pixel value in reference to the background image
posit = {
    "electricity": (1410, 1390),
    "manufacturing": (1730, 1350),
    "irrigation": (2160, 1465),
    "livestock": (2480, 1510),
    "domestic": (2910, 1570),
    "ar_wateruse": (1690, 390),
    "groundwater_background": (-7, 1629),
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

# positions of the "x" (grey out for colourdisabled people) for the items of the Main diagram as pixel value in reference to the background diagram
positx = {
    "electricity": (1490, 1480),
    "manufacturing": (1850, 1490),
    "irrigation": (2330, 1550),
    "livestock": (2600, 1560),
    "domestic": (3000, 1570),
    "ar_wateruse": (2390, 400),
    "groundwater_background": (3000, 2450),
    "reservoir": (1810, 1000),
    "lake": (2350, 1020),
    "river": (2850, 1050),
    "wetland": (3480, 1160),
    "discharge": (3800, 1190),
    "ar_discharge": (3800, 1190),
    "canopy": (500, 1250),
    "glacier": (1000, 490),
    "shortwave": (75, 150),
    "longwave": (190, 150),
    "temperature": (290, 150),
    "wind": (60, 400),
    "humidity": (180, 400),
    "pressure": (300, 400),
    "precipitation": (200, 520),
    "ar_gw_abstraction": (2000, 1850),
    "ar_soil_retflow": (2070, 1850),
    "ar_gw_retflow": (2125, 1850),
    "ar_abs_reservoir": (1600, 1160),
    "ar_retflow_reservoir": (1655, 1185),
    "ar_abs_lake": (2120, 1180),
    "ar_retflow_lake": (2175, 1210),
    "ar_abs_river": (2810, 1155),
    "ar_retflow_river": (2880, 1175),
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
    "ar_glacierrunoff": (1190, 530),
    "ar_snowmelt": (700, 730)
}

# positions of the textual items for the Main diagrams
postxt = {
    "Electricity sector": (3150, 1290),
    "Manufacturing sector": (4000, 1330),
    "Irrigation sector": (4950, 1380),
    "Livestock sector": (5600, 1420),
    "Domestic sector": (6200, 1460),
    "Water consumption": (2200, 300),
    "Reservoir storage": (3660, 1000),
    "Reservoir evaporation": (4500, 700),
    "Lake evaporation": (5150, 850),
    "River evaporation": (5880, 770),
    "Wetland evaporation": (7100, 1000),
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
    "A_groundwater_background": (1, 2265),
    "Throughfall": (80, 1330),
    "Infiltration": (105, 1580),
    "Glacier runoff": (1350, 600),
    "Snow melt": (670, 690),
    "Snow storage": (1700, 560),
    "CO2 effect": (25, 1000)
}

# define if text display should be wrapped or not, for the Main diagram
textwrp = {
    "Electricity sector": True,
    "Manufacturing sector": True,
    "Irrigation sector": True,
    "Livestock sector": True,
    "Domestic sector": True,
    "Water consumption": False,
    "Reservoir storage": True,
    "Reservoir evaporation": True,
    "Lake evaporation": True,
    "River evaporation": True,
    "Wetland evaporation": True,
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
    "Snow melt": False,
    "Snow storage": True,
    "CO2 effect": False
}

# similar information as for posit but for A diagram
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
    "A_ar_surf_runoff": (1580, 1660),
    "A_ar_glacierrunoff": (1580, 1560),
    "A_ar_snowmelt": (1580, 1460),
    "A_ar_snow_sublim": (1420, 1050),
    "A_ar_glacier_sublim": (1560, 1070),
    "A_glacier": (1020, 1475),
    "A_glacier_background": (850, 1220),
    "A_groundwater": (700, 2550),
    "A_groundwater_background": (-5, 2271),
    "A_snow": (1020, 1280),
    "A_soil": (700, 2090)
}

# similar information as for positx but for A diagram
positax = {
    "shortwave": (75, 290),
    "longwave": (190, 290),
    "temperature": (290, 290),
    "wind": (70, 510),
    "humidity": (190, 510),
    "pressure": (300, 510),
    "precipitation": (190, 660),
    "A_canopy": (600, 1130),
    "A_ar_canopy_evapo": (360, 920),
    "A_ar_transpiration": (900, 920),
    "A_ar_soil_evapo": (100, 1400),
    "A_ar_throughfall": (300, 1500),
    "A_ar_infiltration": (300, 1800),
    "A_ar_interflow": (1650, 1950),
    "A_ar_gwr": (300, 2170),
    "A_ar_caprise": (500, 2170),
    "A_ar_gw_runoff": (1500, 2380),
    "A_ar_surf_runoff": (1680, 1630),
    "A_ar_glacierrunoff": (1680, 1530),
    "A_ar_snowmelt": (1680, 1430),
    "A_ar_snow_sublim": (1420, 1050),
    "A_ar_glacier_sublim": (1560, 1070),
    "A_glacier": (1250, 1475),
    "A_glacier_background": (850, 1220),
    "A_groundwater": (860, 2600),
    "A_groundwater_background": (860, 2600),
    "A_snow": (1170, 1290),
    "A_soil": (870, 2120)
}
# similar information as for positxt but for A diagram
postxta = {
    "Glacier storage": (1380, 1420),
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
    "Glacier runoff": (1560, 1610),
    "Groundwater runoff": (3300, 2360),
    "Interflow": (1600, 1970),
    "Snow melt": (1560, 1510),
    "Snow storage": (1060, 1220),
    "Surface runoff": (1560, 1710),
    "CO2 effect": (550, 880),
    "Canopy storage": (500, 1150),
    "Soil layers:": (800, 2150),
    "Groundwater layers:": (1800, 2610),
    "Glacier layers:": (1080, 1510),
    "Snow layers:": (1060, 1320)
}

# similar information as for textwrp but for A diagram
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
    "Groundwater runoff": True,
    "Interflow": False,
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

# position of the information where the number of represented layers should be displayed for A diagram
layatxtpos = {
    "Soil layers": (1060, 2150),
    "Groundwater layers": (1060, 2630),
    "Glacier layers": (1400, 1510),
    "Snow layers": (1350, 1320)
}

def paste_images(moddict, txtdict, modadict, positdict, postxtdict, postxtdictwrap, txtadict, layadict, layatxtpos, positadict, postxtadict, postxtadictwrap, modname):
    """
    adds the single items to the background image
    :param moddict: information for Main diagram
    :param txtdict: corresponding texts for Main diagram
    :param modadict: information for A diagram
    :param positdict: predefined positions of items for Main diagram
    :param postxtdict: predefined positions of text for Main diagram
    :param postxtdictwrap: predefined wrap allowance for Main diagram
    :param txtadict: corresponding texts for A diagram
    :param layadict: number of layers for A diagram
    :param layatxtpos: predifined position of number of layers for A diagram
    :param positadict: predefined positions of items for A diagram
    :param postxtadict: predefined positions of text for A diagram
    :param postxtadictwrap: predefined wrap allowance for A diagram
    :param modname: name of the model

    :return: a stored png of the model with modname as file name for the Main diagram and *_A for the A diagram
    """
    # definition of font sizes. Please see the license for the font.
    myFont = ImageFont.truetype('Roboto-Medium.ttf', 50)
    myFonts = ImageFont.truetype('Roboto-Medium.ttf', 35)
    myFontl = ImageFont.truetype('Roboto-Medium.ttf', 80)
    myFonth = ImageFont.truetype('Roboto-Medium.ttf', 100)

    # define the background and open it
    background = Image.open('fig_background/background_main.png', 'r')
    background.paste(Image.open('./fig_items/input_background.png'), (20, 20),
                     Image.open('./fig_items/input_background.png'))
    # loop for model by model as defined in the modelsetup.json
    print(modname)
    for key in moddict:
        # in case groundwater is represented, use certain items
        if key == "groundwater_background" and str(moddict[key]) == "True":
            background.paste(Image.open('./fig_items/all_line.png'), (970, 775), Image.open('./fig_items/all_line.png'))
            continue
        img = Image.open('./fig_items/' + key + '_' + str(moddict[key]) + '.png', 'r')
        offset = positdict[key]
        background.paste(img, offset, img)
        # in case groundwater is not represented
        if key == "groundwater_background":
            background.paste(Image.open('./fig_items/all_line.png'), (970, 775), Image.open('./fig_items/all_line.png'))
        background.paste(Image.open('./fig_items/legend_upd.png'),  (50, 2620), Image.open('./fig_items/legend_upd.png'))
        imgtxt = ImageDraw.Draw(background)
        # add specific text if model is the "standard model"
        if modname == "ISIMIP2b-complete":
            imgtxt.text((2700, 100), modname, font=myFonth, fill="black")
            imgtxt.text((2700, 220), "a hypothetical global water model representing \nall of the fluxes and storages that are included \nin at least one global water model participating \nin ISIMIP phase 2b", font=myFont, fill="black")
        # add specific text if model is MATSIRO (renamed during the whole process)
        elif modname == "MATSIRO":
            imgtxt.text((2000, 100), "MIROC-INTEG-LAND (formerly MATSIRO)", font=myFonth, fill="black")
        # in other cases, display the model name
        else:
            imgtxt.text((3400, 100), modname, font=myFonth, fill="black")
        # add specific text for JULES-W1
        if modname == "JULES-W1":
            imgtxt.text((3750, 1300), "CaMa Flood", font=myFont, fill="black")
        # in case a item is not represented in the model, add a "x"
        if str(moddict[key]) == "False":
            imgtxt.text(positx[key], "x", font=myFonth, fill="black")

    # now, add the corresponding text
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
                if value == "#929497":
                    imgtxt.text((90, 1000), "x", font=myFonth, fill="black")
            elif key == "Soil storage" or key == "Groundwater storage":
                imgtxt.text(txtpos, key, font=myFontl, fill=value)
            else:
                imgtxt.text(txtpos, key, font=myFont, fill=value)
    # save the image for this model
    background.save(modname + '.png')

    # use a similar process as for Main diagram but for the A diagram
    background = Image.open('fig_background/background_a.png', 'r')
    background.paste(Image.open('./fig_items/input_background.png'), (20, 150),
                     Image.open('./fig_items/input_background.png'))
    for key in modadict:
        if key == "A_groundwater_background" and str(modadict[key]) == "True":
            continue
        img = Image.open('./fig_items/' + key + '_' + str(modadict[key]) + '.png', 'r')
        offset = positadict[key]
        background.paste(img, offset, img)
        imgtxt = ImageDraw.Draw(background)
        if modname == "ISIMIP2b-complete":
            imgtxt.text((600, 50), "ISIMIP2b-complete", font=myFontl, fill="black")
            imgtxt.text((600, 170), "a hypothetical global water model representing \nall of the fluxes and storages that are included \nin at least one global water model participating \nin ISIMIP phase 2b", font=myFonts, fill="black")
        elif modname == "MATSIRO":
            imgtxt.text((300, 50), "MIROC-INTEG-LAND (formerly MATSIRO)", font=myFontl, fill="black")
        else:
            imgtxt.text((1200, 50), modname, font=myFonth, fill="black")
        if str(modadict[key]) == "False":
            imgtxt.text(positax[key], "x", font=myFonth, fill="black")
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
                if value == "#929497":
                    imgtxt.text((610, 860), "x", font=myFonth, fill="black")
            elif key == "Soil storage" or key == "Groundwater storage":
                imgtxt.text(txtpos, key, font=myFontl, fill=value)
            else:
                imgtxt.text(txtpos, key, font=myFont, fill=value)
    for key, value in layadict.items():
        txtpos = layatxtpos[key]
        if value == "1+n":
            imgtxt.text(txtpos, value, font=myFont, fill='#0445A2')
        elif int(value) > 0:
            imgtxt.text(txtpos, value, font=myFont, fill='#0445A2')
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
