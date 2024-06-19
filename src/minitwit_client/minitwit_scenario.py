import requests
import socket
from time import sleep
from flask import Flask

# py39-requests-2.31.0
# SERVER_URL = "http://192.168.1.88:5000"
# SERVER_URL = "http://0.0.0.0:5000"
# SERVER_URL = "http://192.168.2.101:5000"
SERVER_URL = "http://10.0.0.4:5000"


app = Flask(__name__)


# helper functions
def register(username, password, email):
    """Helper function to register a user"""
    return requests.post(
        SERVER_URL + "/register",
        data={
            "username": username,
            "password": password,
            "password2": password,
            "email": email,
        },
        allow_redirects=True,
    )


def login(username, password):
    """Helper function to login"""
    s = requests.Session()
    s.post(
        SERVER_URL + "/login",
        data={"username": username, "password": password},
        allow_redirects=True,
    )
    return s


def register_and_login(username, email, password):
    """Registers and logs in in one go"""
    register(username, password, email)
    return login(username, password)


def logout(session):
    """Helper function to logout"""
    return session.get(SERVER_URL + "/logout", allow_redirects=True)


def add_message(session, text):
    """Records a message"""
    r = session.post(
        SERVER_URL + "/add_message", data={"text": text}, allow_redirects=True
    )
    if text:
        assert "Your message was recorded" in r.text
    return r


def get_public_timeline(session=None):
    if session:
        return session.get(SERVER_URL, allow_redirects=True)
    else:
        return requests.get(SERVER_URL, allow_redirects=True)


def get_private_timeline(username, session=None):
    if session:
        return session.get(SERVER_URL + f"/{username}", allow_redirects=True)
    else:
        return requests.get(SERVER_URL + f"/{username}", allow_redirects=True)


def follow(follows_username, username=None, password=None, session=None):
    if session:
        r = session.get(
            SERVER_URL + f"/{follows_username}/follow", allow_redirects=True
        )
    else:
        login(username, password)
        r = requests.get(
            SERVER_URL + f"/{follows_username}/follow", allow_redirects=True
        )

    assert f"You are now following &#34;{follows_username}&#34;" in r.text
    return r


def scenario_per_user(username, email, password):
    print("Requesting 10 times the public timeline...", flush=True)
    for idx in range(10):
        get_public_timeline()

    print(f"Registering user {username} with email {email} and password {password}...", flush=True)
    session = register_and_login(username, email, password)

    print("Sending 10 tweets...", flush=True)
    for idx in range(10):
        add_message(session, TWEETS[idx])

    for offset in range(0, 20, 10):
        print(f"Cycle {offset}:", flush=True)
        print("    Following 10 users...", flush=True)
        for idx in range(10):
            follow(USERS[offset + idx], session=session)
            # and see it on timeline
            get_private_timeline(session)
        print("    Requesting 10 times the private timeline...", flush=True)
        for idx in range(10):
            get_private_timeline(session)
        print("    Sending 10 tweets...", flush=True)
        for idx in range(10):
            add_message(session, TWEETS[idx])


def scenario():
    hostname = socket.gethostname()
    scenario_per_user(f"{hostname}", f"{hostname}@itu.dk", "1234567")


TWEETS = [
    "Consectetur reprehenderit aliqua laborum cupidatat est labore amet fugiat sunt minim ipsum exercitation irure mollit eiusmod.",
    "Nulla laboris aliquip et nisi mollit veniam consectetur id.",
    "Sunt nulla enim est ipsum velit anim eiusmod in duis cupidatat voluptate mollit sit.",
    "Nisi nulla consectetur eu voluptate deserunt veniam adipiscing minim exercitation incididunt.",
    "Fugiat nostrud ex dolor sit.",
    "Labore culpa anim pariatur.",
    "Officia nulla laboris duis elit ex pariatur, proident minim lorem consectetur ut nisi magna.",
    "Ex velit elit fugiat aliquip minim occaecat.",
    "Ad do est lorem nostrud elit reprehenderit aute, laboris enim fugiat exercitation anim nulla duis eiusmod.",
    "Id non ut nulla cupidatat mollit reprehenderit et anim amet minim ipsum est lorem ex pariatur esse elit ullamco enim.",
    "Irure nisi sed pariatur velit sunt occaecat amet culpa tempor consequat esse incididunt non ex nulla.",
    "Duis non sit tempor nulla aute aliquip eiusmod excepteur veniam nostrud laboris est commodo anim ea quis id qui culpa.",
    "Excepteur duis exercitation labore occaecat fugiat enim nostrud nisi consequat ea.",
    "Nostrud ex eiusmod quis fugiat adipiscing.",
    "Eiusmod est sint consectetur consequat tempor et lorem dolore ut cillum magna fugiat sed voluptate.",
    "Lorem irure duis dolore proident cillum sint consectetur id est pariatur sed adipiscing.",
    "Veniam est irure lorem cillum voluptate ea dolor minim sint tempor sed reprehenderit cupidatat et ex adipiscing labore.",
    "Consectetur nostrud anim laborum ad nisi magna ullamco cupidatat cillum ipsum.",
    "Exercitation mollit cillum ullamco officia nulla occaecat ad ut quis sed anim sunt nostrud cupidatat duis tempor aute excepteur.",
    "Consequat ullamco duis lorem eu officia cillum ad dolore adipiscing ut.",
    "Labore sed laboris ullamco nulla excepteur est velit in magna elit minim ut duis quis nisi.",
    "Fugiat tempor reprehenderit amet labore occaecat mollit sit.",
    "Laboris fugiat nisi duis dolore dolor proident eiusmod ad aliqua culpa sint labore id qui.",
    "Sit excepteur non in do aliquip amet adipiscing.",
    "Lorem minim exercitation dolor ut aute occaecat.",
    "Nostrud aliquip enim irure dolor occaecat nulla duis.",
    "Ut consectetur adipiscing consequat veniam irure eu elit qui esse minim est incididunt sed voluptate commodo nisi.",
    "Cillum id enim excepteur nulla consectetur eiusmod mollit irure do magna lorem.",
    "Nisi ad elit exercitation non irure consequat minim mollit id enim excepteur, laborum culpa deserunt amet officia aliqua ea dolore nulla sint duis tempor dolor incididunt aute et qui ex aliquip.",
    "Mollit voluptate eu et cillum cupidatat magna pariatur dolore ut tempor labore velit nulla.",
    "Sint consequat laboris nostrud.",
    "Ipsum quis ad lorem mollit eiusmod laborum irure aliquip cillum consectetur minim elit.",
    "Commodo mollit nostrud aliqua incididunt dolore sunt duis voluptate deserunt sint pariatur laboris.",
    "Tempor ea mollit exercitation voluptate, nostrud eiusmod quis aliquip consectetur lorem nisi.",
    "Ad nisi lorem labore est velit eu occaecat, adipiscing exercitation sunt minim commodo excepteur irure qui laborum magna sint, deserunt aliqua et dolore non.",
    "Quis lorem consequat laboris, qui veniam reprehenderit tempor cupidatat et amet aliquip ullamco.",
    "Quis enim aliquip officia culpa duis est irure pariatur nulla ad adipiscing nostrud ullamco voluptate fugiat, cupidatat qui sit nisi consectetur ut id velit laboris.",
    "Eu lorem irure cupidatat pariatur laborum sunt ex non aliquip sint in nisi eiusmod excepteur tempor occaecat veniam deserunt, voluptate dolore amet ullamco commodo dolor proident adipiscing duis quis cillum elit anim minim officia est nostrud.",
    "Ipsum consequat non deserunt pariatur elit aute lorem incididunt sint nulla, dolor labore excepteur aliqua commodo duis sed quis veniam ex voluptate ea dolore aliquip magna.",
    "Nulla sed tempor velit lorem aute labore sint incididunt laboris.",
    "Aute sunt duis id cillum sint sed esse cupidatat sit anim enim eu velit ullamco officia adipiscing, lorem dolor occaecat in quis laboris nostrud elit nisi.",
    "Consectetur nostrud elit sint nisi id officia aliqua, irure minim ipsum deserunt aute veniam velit exercitation sunt dolor laborum.",
    "Minim consequat aute duis voluptate.",
    "In voluptate dolor sint amet esse et reprehenderit enim magna mollit labore quis dolore commodo consequat culpa.",
    "Ullamco duis cillum esse reprehenderit officia velit dolore nulla id deserunt nisi quis occaecat adipiscing ex sint consectetur consequat.",
    "Ad magna velit ex ipsum duis laboris deserunt fugiat consequat commodo consectetur anim excepteur.",
    "Mollit excepteur anim laborum eu laboris pariatur non consectetur ut voluptate consequat, exercitation lorem ullamco aliquip ea tempor nisi deserunt et ad est amet cillum reprehenderit.",
    "Sit mollit consectetur et tempor nostrud elit sed non exercitation qui id.",
    "Duis anim enim consectetur tempor.",
    "Anim officia ipsum sed aliqua dolor incididunt elit commodo cillum est reprehenderit.",
    "Aliqua consectetur lorem fugiat ex mollit voluptate magna laborum est ut.",
    "Proident veniam anim et eu esse consectetur fugiat lorem nisi dolor sit magna, laboris tempor mollit id deserunt ea est do sint aliqua voluptate minim dolore labore quis.",
    "Cillum ex aute ad id dolor laboris mollit lorem ut ipsum est magna duis deserunt irure.",
    "Dolor qui consectetur nulla cupidatat dolore reprehenderit aliquip mollit sunt ullamco amet non nostrud incididunt, laboris proident excepteur adipiscing do in esse minim voluptate, enim consequat irure cillum magna labore.",
    "Mollit sit dolor officia deserunt proident id eu, consequat elit aute adipiscing nostrud consectetur occaecat laboris anim reprehenderit enim culpa ut veniam ullamco commodo fugiat, dolore lorem nulla non.",
    "Consequat nostrud nulla aute commodo dolor veniam duis in laborum ex reprehenderit ullamco et occaecat, sint proident enim ut fugiat aliquip elit magna deserunt irure amet officia esse labore culpa qui velit pariatur non.",
    "Irure eu cupidatat sed officia deserunt ea ut tempor fugiat do ipsum commodo nulla.",
    "Ut officia ex minim, fugiat magna cillum aliqua qui sint sed quis labore.",
    "Cupidatat qui aliqua proident, incididunt sed officia consequat tempor sint anim labore duis aliquip adipiscing laboris eu quis amet veniam.",
    "Magna consectetur irure cillum dolor occaecat aute.",
    "Eu cupidatat deserunt ea.",
    "Laboris et eiusmod fugiat nulla nostrud quis esse sint sunt consequat adipiscing mollit.",
    "Eiusmod tempor amet commodo excepteur et irure esse voluptate exercitation pariatur est deserunt mollit dolor, in dolore veniam ut cillum sit ipsum ex occaecat sunt anim aute minim.",
    "Et sed aute laboris ullamco sunt lorem in esse nisi, nulla reprehenderit dolor id commodo do exercitation, enim amet nostrud aliqua.",
    "Laborum qui ipsum incididunt cupidatat deserunt pariatur exercitation est.",
    "Fugiat amet reprehenderit eu labore nisi esse culpa velit.",
    "Reprehenderit consequat voluptate enim quis sint commodo consectetur deserunt ipsum sunt esse amet adipiscing, nostrud aute laboris do laborum sit labore aliqua non anim ut duis nulla culpa dolor elit exercitation dolore cillum mollit, tempor id eu ullamco cupidatat excepteur est et minim nisi fugiat ad velit veniam proident aliquip magna.",
    "Do sunt est in duis excepteur magna ut adipiscing minim velit ullamco, quis deserunt eu amet eiusmod irure et exercitation nulla consectetur laboris mollit ex fugiat aliquip enim commodo anim ad.",
    "Aute sint enim ad laborum irure eu qui id occaecat deserunt.",
    "Ut nostrud eiusmod officia irure sint esse laboris voluptate proident minim consectetur qui labore adipiscing.",
    "Ea mollit ipsum fugiat ut officia nulla consectetur minim irure magna ullamco id nisi, aute voluptate sunt velit culpa anim.",
    "Id aliqua deserunt adipiscing enim officia.",
    "Commodo adipiscing aliqua amet, esse consequat velit aute ullamco.",
    "Aliqua cillum proident tempor consequat aute lorem irure pariatur ex laborum nulla ea nisi id est.",
    "Ex irure occaecat ullamco est qui ad fugiat minim cupidatat sed amet non enim in velit ipsum culpa, nostrud proident officia lorem commodo ea mollit veniam exercitation quis incididunt cillum sint.",
    "Do id excepteur sit magna dolor ea nulla cupidatat non dolore qui enim elit ex.",
    "Sint est labore minim nulla consequat duis in ad veniam laboris, aliqua sit elit laborum quis officia dolore tempor ex sunt fugiat pariatur voluptate ea sed proident velit magna.",
    "Ut ullamco voluptate fugiat ex et in.",
    "Exercitation consectetur aliqua eiusmod id nulla amet culpa velit sed minim quis cillum enim occaecat dolor.",
    "Ut nulla voluptate officia qui proident et reprehenderit irure est enim cillum consectetur aliqua amet occaecat non fugiat, magna duis eiusmod dolor sunt culpa elit exercitation in ad tempor id laboris, ex deserunt aute anim nisi quis labore pariatur.",
    "Elit est aliquip sit irure officia dolore proident, esse incididunt non tempor cillum eu eiusmod consectetur sint in ipsum pariatur, qui reprehenderit culpa deserunt laborum et nostrud anim veniam voluptate commodo consequat do.",
    "Elit dolor nisi excepteur lorem id officia.",
    "Sit enim nostrud ipsum minim, culpa voluptate do amet laborum magna esse qui in officia exercitation nisi quis ullamco aute reprehenderit consequat elit.",
    "Cupidatat eiusmod in ipsum reprehenderit voluptate.",
    "Minim lorem consectetur cillum aute irure ipsum nisi ea laboris deserunt adipiscing sed duis aliquip veniam voluptate.",
    "Ipsum eiusmod magna do aliqua sint laborum.",
    "Officia irure laborum est nulla nisi ipsum et pariatur.",
    "Sint labore incididunt quis elit sit anim excepteur nostrud duis reprehenderit aliqua voluptate occaecat eiusmod, dolor lorem fugiat aute.",
    "Anim aliquip aliqua proident fugiat est nisi sed amet incididunt tempor magna laboris, ex reprehenderit non qui do irure id esse ea officia lorem commodo aute ad, velit dolor labore eu veniam exercitation in laborum ullamco nostrud dolore deserunt pariatur ut sunt.",
    "Voluptate reprehenderit laborum exercitation dolor incididunt duis deserunt sed.",
    "Aute et eu eiusmod cillum dolor occaecat id ex tempor minim in excepteur quis laborum ullamco sint.",
    "Sint laboris cillum sunt et cupidatat pariatur occaecat ut ex.",
    "In exercitation deserunt laboris cillum occaecat excepteur id officia nisi adipiscing ex elit esse tempor, ad qui ea ullamco amet quis irure aliquip nostrud et culpa laborum sit sed.",
    "Lorem sint sit culpa nostrud sed ex ut non voluptate cupidatat minim ea consectetur et nulla amet occaecat proident excepteur.",
    "Lorem aliquip irure ea esse culpa.",
    "Sed esse culpa qui aliquip sunt nulla adipiscing cupidatat nisi.",
    "Nisi est id ipsum tempor occaecat officia culpa aute aliqua deserunt laboris non.",
    "Laboris exercitation anim deserunt sunt sed reprehenderit ex aliqua enim cillum cupidatat velit eiusmod ad dolore.",
    "Magna enim et aliquip sed non nulla esse sit minim ex.",
    "Sit proident lorem in do consequat consectetur commodo quis nulla velit excepteur ipsum cupidatat ea eiusmod cillum elit duis.",
]


USERS = [
    "Roger Histand",
    "Geoffrey Stieff",
    "Wendell Ballan",
    "Nathan Sirmon",
    "Quintin Sitts",
    "Mellie Yost",
    "Malcolm Janski",
    "Octavio Wagganer",
    "Johnnie Calixto",
    "Jacqualine Gilcoine",
    "Luanna Muro",
    "Shaunda Loewe",
    "Lowell Caneer",
    "Roderick Tauscher",
    "Kym Yarnell",
    "Sherril Tazewell",
    "Blair Reasoner",
    "Rhea Pollan",
    "Ayako Yestramski",
    "Georgie Mathey",
    "Beverley Campanaro",
    "Leonora Alford",
    "Odessa Redepenning",
    "Quintin Reimann",
    "Johnnie Casasola",
    "Enoch Herdman",
    "Angeline Sasse",
    "Guadalupe Rumps",
    "Lien Pons",
    "Maria Aceto",
    "Caitlin Kenndy",
    "Carrol Hollopeter",
    "Logan Labarbera",
    "Buford Hunsperger",
    "Hildegard Rediske",
    "Bret Santrizos",
    "Rachal Hoke",
    "Cherelle Yeaton",
    "Maribeth Chenot",
    "Meridith Bemrich",
    "Shalon Schuyleman",
    "Shizue Linde",
    "Tyree Hotz",
    "Barney Allyn",
    "Otto Simcox",
    "Kris Berdine",
    "Diana Hoeschen",
    "Lynn Harnden",
    "Noelia Flot",
    "Carolina Wiatrak",
    "Brandon Appelgate",
    "Dion Metherell",
    "Andres Lebitski",
    "Lucille Cardinas",
    "Clair Mccoard",
    "Jess Betzig",
    "Candida Vimont",
    "Melissa Findlen",
    "Olen Hain",
    "Madonna Brown",
    "Jean Leasor",
    "Carroll Begnaud",
    "Dorian Tomory",
    "Hilario Bendlage",
    "Tamie Debeaumont",
    "Blake Kapp",
    "Sanjuana Garibay",
    "Hiram Lauchaire",
    "Eusebio Oestreich",
    "Sal Nases",
    "Valda Brokaw",
    "Numbers Shanley",
    "Sonya Hoffstetter",
    "Cameron Winge",
    "Donte Hua",
    "Kyla Gierut",
    "Thalia Averitte",
    "Sherwood Bonnel",
    "Tracy Mckim",
    "Eloisa Distel",
    "Jackson Callas",
    "Isaias Aspley",
    "Leigh Kahuhu",
    "Kathe Overson",
    "Lynwood Lomax",
    "Salley Twidwell",
    "Ruthanne Nusser",
    "Kasi Araki",
    "Ed Benker",
    "Marjory Cuccia",
    "Rebeca Witkus",
    "Toya Zesati",
    "Palmer Stroot",
    "Shauna Yamasaki",
    "Rick Digiulio",
    "Marisela Vincik",
    "Natividad Ballar",
    "Rob Mclamb",
    "Apryl Rowan",
    "Marquis Luque",
    "Darci Chiarella",
    "Gladis Massaglia",
    "Gayle Hayoz",
    "Charley Makepeace",
    "Lyndsay Corti",
    "Landon Zee",
    "Giuseppe Polek",
    "Jeromy Duclo",
    "Norine Mittman",
    "Cleveland Delage",
    "Karyn Chagolla",
    "Berry Steinhoff",
    "Louie Tugwell",
    "John Peressini",
    "Ruben Pizano",
    "Vennie Huddleson",
    "Maricela Mcnurlen",
    "Lyman Foxman",
    "Numbers Busey",
    "Nakia Vero",
    "Staci Guster",
    "Lynn Mckeague",
    "Abdul Smeathers",
    "Jeffry Baerman",
    "Jospeh Kilichowski",
    "Desmond Bennerman",
    "Elmo Liepins",
    "Elodia Rohlack",
    "Pattie Mellom",
    "Kerry Passer",
    "Janyce Freytas",
    "Claudia Giacchino",
    "Rudolph Sommons",
    "Lanora Kolinski",
    "Olen Boothroyd",
    "Breana Sissom",
    "Shanda Tande",
    "Shannon Casassa",
    "Aurelio Madena",
    "Josh Hiler",
    "Waneta Ungvarsky",
    "Stacy Consolo",
    "Margherita Topal",
    "Lenora Wenk",
    "Winter Spinoza",
    "Clint Mccardle",
    "Ferdinand Gonyo",
    "Paulene Mathers",
    "Lyndon Olide",
    "Chi Mccallister",
    "Alysha Turbeville",
    "Cristobal Hickonbottom",
    "Markus Goes",
    "Dana Hasper",
    "Katelyn Frankiewicz",
    "Cleo Grulke",
    "Dane Megeath",
    "Chin Radish",
    "Martha Demuzio",
    "Caren Swiler",
    "Federico Nowlen",
    "Bret Iuliucci",
    "Vania Nimick",
    "Johna Slaybaugh",
    "Katheleen Ekdahl",
    "Kelley Praytor",
    "Hyo Stricklen",
    "Latashia Moraites",
    "Jerrell Camilleri",
    "Dominga Barcenas",
    "Domenic Kriegshauser",
    "Margert Healy",
    "Eloy Phimsoutham",
    "Janella Bevevino",
    "Cheryll Ebbers",
    "Glenn Corn",
    "Dirk Zumpano",
    "Rick Hinton",
    "Delorse Tribble",
    "Francesco Kassam",
    "Xuan Kozera",
    "Homer Bettridge",
    "Edwin Luthe",
    "Kurtis Liakos",
    "Priscilla Mitton",
    "Wyatt Schnorbus",
    "Kesha Chestnut",
    "Isreal Reefer",
    "Johnette Joye",
    "Johnnie Lesso",
    "Prince Trbovich",
    "Irene Valcin",
    "Caitlyn Handly",
    "Tyler Hautan",
    "Kristina Mcpeek",
    "Kala Saner",
    "Darryl Bart",
    "Ward Colley",
    "Sharmaine Abdelrahman",
    "Francesco Tavira",
]



@app.route('/trigger')
def start_scenario():
    scenario()
    return f"Done running scenario on {socket.gethostname()}."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
