from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import urllib.request
import time
import sys
import os

# THIS PROGRAM WILL SEARCH FOR IMAGES ON GOOGLE GIVEN A SEARCH QUERY AND THEN DOWNLOAD THE SPECIFIED NUMBER OF IMAGES.

search_queries = [

    'EVO, E-Sport Eye Combo, Light, Ensemble/Set', 'EVO, E-Tec Hero, Helmet, Black, L',
    'EVO, E-Tec Hero, Helmet, Black, M', 'EVO, E-Tec Hero, Helmet, Black, S', 'Abus, Pedelec, Helmet, Fashion Green, M',
    'Catlike, Tora, Helmet, Black, M', 'Catlike, Tiko, Helmet, Black/White, U', 'Catlike, Tiko, Helmet, Black/Blue, U',
    'Catlike, Kitten, Helmet, Tricolor Pink, XS',
    'Lezyne, LED Helmet mount, For Mini, Power, Super, Power and Mega Drive', 'Lezyne, LED, Helmet mount',
    'FLEA HELMET HEAD HAT MOUNT', 'Foldable Helmet M Size Black/Black', 'Helmet Stoker Bell Titanium L',
    'Helmet Stoker Bell White/Silver S', 'Abus, Yadd-I, Helmet, Velvet black, M',
    'Abus, Yadd-I, Helmet, Velvet black, S', 'Abus, Yun-I Ace, Helmet, Velvet black, L',
    'Abus, Yun-I Ace, Helmet, Velvet black, M', 'Lezyne, Femto Drive Duo, Helmet Light',
    'ZEFAL Z EYE MIRROR FOR HELMET', 'Abus, Smiley 2.0, Helmet, Royal/Black, S',
    'Abus, Smiley 2.0, Helmet, Royal/Blue, M', 'Abus, Smiley 2.0, Helmet, Royal/Blue, S',
    'Abus, In-Viz Ascent, Helmet, Velvet Black, M', 'Abus, Youn-I Ace, Helmet, Sparkling blue, L',
    'Hale Giro Youth Helmet Black', 'Vasona Giro Helmet Mat Glacier', 'Vasona Giro Helmet White',
    'Register Giro Helmet XL White', 'Vasona Giro Helmet Black', 'Vasona Giro Helmet Bright Pink',
    'Hale Giro Youth Helmet Red', 'Coast Joy Ride Bell Helmet Lead', 'Register Giro Helmet Red',
    'Saga Giro Helmet Glacier Med', 'Savant Giro Helmet REd Med', 'Register Giro Helmet White',
    'Abus, Smiley, Helmet, Sparkling Red, S', 'Abus, Smiley, Helmet, Sparkling Red, M',
    'Abus, Smiley, Helmet, Blue Sharky, M', 'Abus, Smiley, Helmet, Rse Princess, S',
    'Abus, Smiley, Helmet, Rse Princess, M', 'Abus, Smty, Helmet, cean, S', 'Abus, Smty, Helmet, cean, M',
    'Tremor Giro Helmet Black', 'Tremor Giro Helmet Bright Pink', 'Fixture Giro Helmet Grey',
    'Bern, Brentwd, Helmet, Matte Black, 3XL', 'Bern, Watts Mips, Helmet, Matte Black, 3XL',
    'Abus, Smiley 2.1 Helmet, Blue Mask, M', 'Abus, Scraper Kid, Helmet, Orange, M',
    'Abus, Scraper Kid, Helmet, Shiny Blue, S', 'Abus, Scraper Kid, Helmet, Shiny Blue, M',
    'Abus, Scraper 3.0 Helmet,Velvet Black L', 'Abus, Scraper 3.0 Helmet, Ultra Blue, L',
    'Abus, Pedelec 1.1, Helmet, Black, L', 'Abus, Pedelec 1.1, Helmet, Black, M', 'Abus, Pedelec 1.1, Helmet, White, M',
    'Giro Register Yellow helmet', 'helmet Giro Register Mips Black', 'Abus Makator helmet black L',
    'Abus Makator helmet Black M', 'Abus Makator helmet M red', 'ABUS, Makator, Helmet, Blaze red, L, 58-62cm',
    'ABUS, Macator, Helmet, Blaze Red, S, 51-55cm', 'ABUS, Hyban 2.0, Helmet, Velvet Black, XL, 58-63cm',
    'ABUS, Hyban 2.0, 56-61cm, L, Helmet, Polar White,', 'Helmet Giro Caden Mips S Black',
    'helmet Giro Agilis MIPS M true spruce', 'helmet Giro Scamp S black', 'helmet Giro Agilis MIPS W S midnight',
    'helmet Giro Radix MIPS M spruce citron', 'helmet Giro Radix MIPS M midnight',
    'helmet Giro Radix MIPS W S black purple', 'Helmet Radix MIPS Large RED', 'helmet youth Scamp blue green Camo S',
    'Giro Helmet Vasona MIPS Mat Glacier', 'Giro Helmet Radix M W cool breeze', 'Giro Helmet Register Titanium',
    'Helmet Giro Vasona MIPS  Mat Black', 'Tube Damco 24*1.75 /2.125', 'Tube Damco 700C 35/38C Presta',
    'Tire Mount Graham 26 x 2.0', 'Wheel 700 c Damco cassette 7-8 sp', 'Vice Grios Velo locking',
    'Tire Continental Grand Prix 5000 700c x 25', 'Novelty Valve caps 8 ball', 'Novelty Valve Capd eyeball',
    '10mm axle and cone set', 'light tube Arisun 700 x 18/25', 'Kickstand EVO Center Mount',
    'Shimano Alivio Crankset FC-T4060 ( speed 26/36/48, hollow, 175mm', 'Wheel F Alexrims MD27',
    'TUBE KENDA 700X28-35C (27"X1-1/8"-1-1/4") P.V 48MM',
    'Michelin, Dynamic Sport, 700x28C, Wire, 30TPI, 58-87PSI, 340g, Black', 'Lezyne Strip Drive Rear Light',
    'Lezyne Mini Drive 400/KTV Pro Light Set', 'BBB Shimano Brake pads', 'SHIMANO  CHAIN CN-HG40 8 SP',
    'Abus Ultra Mini 402, U lock, yellow', 'Deity MTB Handlebar 35mm 800mm 25mm raise',
    'Fabric Mask (mom medical) Muck off black L', 'Fabric Mask (non medical) Muck off S',
    'Sram Shifter combo X5 2 x 10', 'Sram Apex Rear Derailleur 10 sp Medium Black',
    'Sram GX R Derailleur 10 sp Medium cage', 'Stan”s N Tubes, Rim Tape, Yellw, 33mm x 9.14m rll',
    'Stans rim tape 30mm', 'Kool Stop brake pads Avid BB7', 'Roswheel Gear Straps 550 mm',
    'Zefal Z Console iPhone XS Max', 'Evo Windup Comfort  Handlebar Tape White',
    'Supacaz Prizmatic Handlebar Tape Pink', 'Supacaz Prizmatik Handlebar Tape Blue', 'Sram  locking grips Red',
    'Wolf Tooth Razer grips Blue', 'Wolf Tooth Razer grips Red', 'Wolf Tooth Razer grips Black',
    'Zefal Phone mount for Iphone XR', 'Evo  CO2 cartridge threaded', 'Roswheel Gear Straps 850mm',
    'Zefal Console for Iphone X or XS', 'Sram X5 Shifter  3 x 9', 'Jagwire Inline Adjuster',
    'FSA Handlebars Omega Compact 31.8 x 380 mm', 'Shimano Hydraulic hose  1700 mm SM-BH90-SS',
    'Shimano BBUN300 D-EL 68mm 127.5 mm', 'Shimano Claris  Shift brake Levers ST-R2000 - L  2 x 8',
    'Eclypce Crankset Fixie 46T 165mm Silver Black', 'Eclypse Freehub body Shimano',
    'Trail-Gator Ball joint bolt with nut and Washer', 'Sram Powerlock, chain link, connector, 12 speed',
    'Eclypse SS dual, Bottle Cage Saddle  clamp', 'Roswheel Off Road Top Tube Bag 1 L',
    'Evo Handlebar Tape  Wind up Classic Royal Blue', 'BBB Handlebar tape raceribbon Light Blue',
    'Sram X5 Rear Derailleur 10 Sp Medium Cage', 'Shimano BB-UN300 LL123 73mm 122.5mm Square Taper',
    'Ros Wheel Off Road Handlebar Bag 15L', 'Roswheel Seat Bag 17L Blue',
    'Shimano Sora Crankset 9 sp 34/50 170mm FC-R3000', 'Rosswheel Road handlebar Bag 9L Black',
    'Roswheel Road Accessory poch Handlebar Bag', 'Roswheel Road Frame Bag 3.5L', 'Roswheel Road Frame Bag 2L',
    'Shimano Sora Crankset  9 sp, 175 mm 34/50 black', 'Shimano Hydraulic Brake Rear  BL-M4100',
    'Roswheel Tour Handlebar Bag 5L', 'Muc Off Face Mask Woodland Camo S', 'Muc Off Face Mask L Woodland Camo',
    'Bordo Lite 6055 folding Lock red', 'Abus U Lock 402, STD Yellow', 'Sram Chain PC 1071 10sp',
    'Roswheel Tour Rear Rack', 'Roswheel Tour Trunk Pack 8L', 'Roswheel Tour Front Rack', 'Delta Cargo Net',
    'Shimano Chain 10s CN- HG95 XTR', 'Giro Ambient 2.0 Gloves XL Yellow black (winter)',
    'Giro Gloves Candela Womans Yellow L Winter', 'Roswheel Panier Large 20 L',
    'Wheel MD19  Rear 29"disc, through axle', 'Wheel MD19 27.5" rear',
    'Shimano Claris Crankset FC-R2030 30/39/50T 170mm', 'Shimano Tiagra FC-4700 Crankset 10 sp 170mm',
    'Evo Handlebar tape Pink Wind p Classic', 'Evo Handlebar Tape Royal BlueWind up Classic', 'TacX Bottle Cage holder',
    'Shimano Brake shoes inserts R55C4', 'Alexrims Front Wheel disc ATD470',
    'Alexrims MD19  Front Through axle 29” disc', 'Shimano BB 68 mm 117.5 mm',
    'Sram X5 Rear Derailleur 9 Sp Long Cage Black', 'Sram X4 Rear Derailleur 7,8,9 Speed Long cage Black',
    'Shimano inserts Brake pads R55C3', 'Giro Gloves Ambient M Yellow (winter)',
    'Giro Gloves Candela M Yellow Womans (Winter)', 'Tire Metro Cruiser 700 x 32', 'Evo Tube 700 x 35-44',
    'Cram red 22 Chain 11 sp', 'Koolstop Shimano Brake pads sintered', 'BBB Waterflex Shoe Cover 47/48 Yellow',
    'BBB Shoe Cover Waterflex 45/46 Yellow', 'BBB Shoe Cover Waterflex 43/44', 'Tire Metro Runner 700 x 38',
    'Maxxis Minion DHR2 Tire 27.5 x 2.40 folding tanwall'
]

image_names = [
    770612310216, 770612309128, 770612309111, 770612309104, 4003318122132, 8435354136556, 8435354135993, 8435354136006,
    8435354130981, 4712805978700, 4712805985678, 768686820090, 831273623906, 768686970368, 768686970580, 4003318725883,
    4003318726064, 4003318726132, 4003318726125, 4712805986620, 643187007198, 4003318775420, 4003318775451,
    4003318775444, 4003318133756, 4003318726217, 768686070907, 768686071782, 768686071829, 768686072482, 768686071744,
    768686071768, 768686070969, 768686099298, 768686072147, 768686075698, 768686075117, 768686072185, 4003318725807,
    4003318725814, 4003318725753, 4003318725647, 4003318725654, 4003318479717, 4003318479724, 768686070723,
    768686070761, 768686072628, 843990058251, 843990081341, 4003318818035, 4003318817571, 4003318817502, 4003318817519,
    4003318817595, 4003318817632, 4003318819063, 4003318819056, 4003318819117, 768686072123, 768686072208,
    4003318872136, 4003318872129, 4003318872228, 4003318872235, 4003318872211, 4003318869013, 4003318869037,
    768686183362, 768686265204, 768686070570, 768686268687, 768686266621, 768686266560, 768686265990, 768686266454,
    768686267116, 768686071867, 768686266041, 768686072161, 768686071843, 621920540058, 621920540119, 6927116102425,
    621920265470, 621920380661, 4019238007824, 5013863050476, 5013863050490, 689228170537, 6927116101053, 770612273412,
    689228594289, 770612341654, 47853051186, 86699414458, 4712806002060, 4712806002152, 8716683106169, 689228441460,
    655043417218, 817180023664, 5037835207583, 5037835207576, 710845684807, 710845647086, 710845771828, 847746020448,
    847746020431, 760251075843, 6920636793562, 3420587073704, 770612338937, 660902393190, 660902393183, 710845727566,
    810006800937, 810006800999, 810006800920, 643187018026, 770612336902, 6920636793579, 643187017173, 710845684869,
    4715910031438, 400310034700, 689228721029, 192790619316, 689228321519, 2100000063925, 770612330214, 91001001,
    710845805912, 770612316300, 6920636793524, 770612339088, 8716683098815, 710845673801, 192790622194, 6920636793470,
    6920636793487, 689228678491, 6920636793364, 6920636793371, 6920636793401, 6920636793388, 689228678583, 192790621289,
    6920636793265, 5037835207613, 5037835207620, 704660269479, 655043417225, 710845644696, 6920636793340, 6920636793302,
    6920636793357, 799403103806, 689228984660, 768686057069, 768686640476, 6920636793289, 770612342507, 770612342484,
    689228386754, 689228925908, 770612338890, 770612338913, 8714895004877, 689228994560, 770612341166, 770612342491,
    192790619224, 710845673795, 710845609671, 689228284876, 768686640490, 768686640469, 6927116101862, 770612336186,
    710845727627, 760251081530, 8716683108019, 8716683108002, 8716683107937, 6927116100216, 4717784038506,
]

count = 0
for query in range(len(search_queries)):

    site = 'https://www.google.com/search?tbm=isch&q=' + str(search_queries[query])

    # providing driver path
    PATH = "E:\webdrivers\chromedriver.exe"
    driver = webdriver.Chrome(PATH)

    # passing site url
    driver.get(site)



    driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")

    # parsing
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # closing web browser
    driver.quit()

    # scraping image urls with the help of image tag and class used for images

    img_tags = soup.find_all("img", class_="rg_i")
    amountOfImagesDownloaded = 0
    amountOfImagesToDownload = 3
    for i in img_tags:
        try:
            # passing image urls one by one and downloading
            urllib.request.urlretrieve(i['src'], str(query) + "-" + str(amountOfImagesDownloaded) + "-" + str(image_names[query]) + ".jpg")

            count += 1
            amountOfImagesDownloaded += 1
            print("Number of images downloaded = " + str(count), end='\=r')
            if amountOfImagesDownloaded == amountOfImagesToDownload:
                break
        except Exception as e:
            pass
