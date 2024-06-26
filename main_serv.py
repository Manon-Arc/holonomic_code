import network
import socket
from move import Move
from motor import Motor


def display_ap_info(ap):
    print("\nLocal IP: {}\nSubnet mask: {}\nIP Gateway: {}\nDNS:{}".format(*ap.ifconfig()))
    print("SSID: {}\nChannel: {}".format(ap.config("essid"), ap.config("channel")))
    print("BSSID: {:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(*ap.config("mac")))


def web_page():
    return """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<style>
    html {
        font-family: Helvetica;
    }

    body {
        width: auto;
        height: 100svh;
        overflow: hidden;
    }

    .head {
        color: black;
        padding: 2vh;
        margin-bottom: 5%;
    }

    .page {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .joystick {
        position: relative;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: repeat(3, 1fr);
        border-radius: 50%;
        background-color: rgb(212, 212, 212);
        box-shadow: none;
    }

    .button {
        width: calc(30vh/3);
        height: calc(30vh/3);
        display: flex;
        color: black;
        text-decoration: none;
        font-size: 30px;
        cursor: pointer;
        border: none;
        z-index: 10;
        user-select: none;
    }

    .av {
        grid-area: 1 / 2 / 2 / 3;
    }

    .avg {
        grid-area: 1 / 1 / 2 / 2;
    }

    .g {
        grid-area: 2 / 1 / 3 / 2;
    }

    .arg {
        grid-area: 3 / 1 / 4 / 2;
    }

    .ar {
        grid-area: 3 / 2 / 4 / 3;
    }

    .ard {
        grid-area: 3 / 3 / 4 / 4;
    }

    .d {
        grid-area: 2 / 3 / 3 / 4;
    }

    .avd {
        grid-area: 1 / 3 / 2 / 4;
    }

    .center {
        grid-area: 2 / 2 / 3 / 3;
    }

    .cursor {
        position: absolute;
        background-color: rgb(72, 72, 72);
        width: calc(30vh/2.3);
        height: calc(30vh/2.3);
        border-radius: 50%;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
    }

    .slidecontent {
        height: 20px;
        width: 250px;
        padding: 10px;
        margin-bottom: 10%;
        border-radius: 20px;
        box-shadow: -3px 4px 15px 1px #ffffff inset, 3px -1px 15px 1px #8d8d8d inset;
    }

    .slider {
        -webkit-appearance: none;
        width: 250px;
        height: 5px;
        border-radius: 5px;
        background: #d3d3d3;
        outline: none;
        opacity: 0.7;
        -webkit-transition: .2s;
        transition: opacity .2s;
    }

    .slider::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width: 15px;
        height: 15px;
        border-radius: 50%;
        cursor: pointer;
        border-radius: 40%;
        background: #939393;
        border: 2px solid #d4d4d4;
        box-shadow: -4px 4px 3px 2px #ffffff, 2px -1px 4px 3px #8d8d8d;

    }

    .slider::-moz-range-thumb {
        width: 200px;
        height: 15px;
        border-radius: 50%;
        position: absolute;
        cursor: pointer;
        border-radius: 40%;
        background: #efefef;
        border: 2px solid #d4d4d4;
        box-shadow: -4px 4px 3px 2px #ffffff, 2px -1px 4px 3px #8d8d8d;

    }

    .slidecontainer {
        display: flex;
        flex-direction: row;
        height: 150px;
        justify-content: space-between;
        align-items: center;
        position: relative;
    }

    .affichage_vitesse {
        margin-bottom: 50%;
    }

    .rota {
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: space-around;
        align-items: center;
        position: relative;
        margin-top: 5vh;
    }
    .rotationD {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 8vh;
        height: 8vh;
        border: solid;
        border-width: 2px;
        border-color: rgb(69, 69, 69);
        border-radius: 30%;
    }

    .rotationD img {
        width: 6vh;
    }

    .rotationG {
        display: flex;
        justify-content: center;
        align-items: center;
        width:8vh;
        height: 8vh;
        border: solid;
        border-width: 2px;
        border-color: rgb(69, 69, 69);
        border-radius: 30%;
    }
    .rotationG img {
        width: 6vh;
    }

</style>

<body>
    <div class="page">
        <div class="head">
            <h1 id="direc">Motor control :</h1>
        </div>
        <div class="vitesse">
            <div class="affichage_vitesse">
                <label for="sliderValue">Speed :</label>
                <span id="sliderValue"></span>
                <div class="slidecontent">
                    <input type="range" min="0" max="100" value="0" step="1" class="slider" id="myRange" name="slider"
                    onchange='sendRequest("POST", "/manette", "speed", "value")'>
                    <input type="hidden" name="speed" class="slider_speed" value="">
                </div>
            </div>
        </div>
        <div class="joystick">
            <div class="button av" id="av"></div>
            <div class="button avg" id="avg"></div>
            <div class="button g" id="g"></div>
            <div class="button arg" id="arg"></div>
            <div class="button ar" id="ar"></div>
            <div class="button ard" id="ard"></div>
            <div class="button d" id="d"></div>
            <div class="button avd" id="avd"></div>
            <div class="button center" id="center"></div>
            <div class="cursor"></div>
        </div>
        <div class="rota">
            <div class="rotationG" value=rota onclick="sendRequest('POST', '/manette', 'joystick', 'rotag' )">
                <img src="/static/img/rotating-arrow-to-the-left .png" alt="">
            </div>
            <div class="rotationD" value=rota onclick="sendRequest('POST', '/manette', 'joystick', 'rotad' )">
                <img src="/static/img/rotating-arrow-to-the-right.png" alt="">
            </div>
        </div>
    </div>
</body>
<script>
    let lastDir = "st";
    let pre = document.getElementById("direc");
    let av = document.getElementById("av").getBoundingClientRect();
    let avg = document.getElementById("avg").getBoundingClientRect();
    let g = document.getElementById("g").getBoundingClientRect();
    let arg = document.getElementById("arg").getBoundingClientRect();
    let ar = document.getElementById("ar").getBoundingClientRect();
    let ard = document.getElementById("ard").getBoundingClientRect();
    let d = document.getElementById("d").getBoundingClientRect();
    let avd = document.getElementById("avd").getBoundingClientRect();
    let center = document.getElementById("center").getBoundingClientRect();

    function InDiv(div,x,y){
        return x > div.left && x < div.right && y > div.top && y < div.bottom;
    }

    const lache_clique = (e) => {
        e.style.left = "50%";
        e.style.top = "50%";
    }

    const joystick = document.querySelector(".joystick")
    const necessaire = joystick.scrollWidth;

    document.body.addEventListener('touchmove', (e) => {
        let xP = e.touches[0].clientX
        let yP = e.touches[0].clientY
        let cursor = document.querySelector(".cursor");
        const joystick_pos = document.querySelector(".joystick").getBoundingClientRect();
        cursor.style.left = `${xP - joystick_pos.left}px`;
        cursor.style.top = `${yP - joystick_pos.top}px`;
        const cursor_pos = cursor.getBoundingClientRect();

        if (cursor_pos.top < joystick_pos.top) {
            cursor.style.top = `${cursor.scrollWidth / 2}px`;
        }
        if (cursor_pos.bottom > joystick_pos.bottom) {
            cursor.style.top = `${necessaire - cursor.scrollWidth / 2}px`;
        }
        if (cursor_pos.right > joystick_pos.right) {
            cursor.style.left = `${necessaire - cursor.scrollWidth / 2}px`;
        }
        if (cursor_pos.left < joystick_pos.left) {
            cursor.style.left = `${cursor.scrollWidth / 2}px`;
        }

        let centreY = cursor_pos.top + cursor.scrollHeight/2;
        let centreX = cursor_pos.left + cursor.scrollWidth/2;

        if(InDiv(av,centreX,centreY) && lastDir != "av"){
            lastDir = "av";
            sendRequest('GET', '/manette', 'joystick', 'av' )
        } else if(InDiv(avg,centreX,centreY) && lastDir != "davg"){
            lastDir = "davg";
            sendRequest('GET', '/manette', 'joystick', 'davg' )
        } else if(InDiv(g,centreX,centreY) && lastDir != "g"){
            lastDir = "g";
            sendRequest('GET', '/manette', 'joystick', 'g' )
        } else if(InDiv(arg,centreX,centreY) && lastDir != "darg"){
            lastDir = "darg";
            sendRequest('GET', '/manette', 'joystick', 'darg' )
        } else if(InDiv(ar,centreX,centreY) && lastDir != "ar"){
            lastDir = "ar";
            sendRequest('GET', '/manette', 'joystick', 'ar' )
        } else if(InDiv(ard,centreX,centreY) && lastDir != "dard"){
            lastDir = "dard";
            sendRequest('GET', '/manette', 'joystick', 'dard' )
        } else if(InDiv(d,centreX,centreY) && lastDir != "d"){
            lastDir = "d";
            sendRequest('GET', '/manette', 'joystick', 'd' )
        }  else if(InDiv(avd,centreX,centreY) && lastDir != "davd"){
            lastDir = "davd";
            sendRequest('GET', '/manette', 'joystick', 'davd' )
        }  else if(InDiv(center,centreX,centreY) && lastDir != "st"){
            lastDir = "st";
            sendRequest('GET', '/manette', 'joystick', 'st' )
        }
    });

    document.body.addEventListener('touchend', (e) => {
        let cursor = document.querySelector(".cursor");
        cursor.style.left = `50%`;
        cursor.style.top = `50%`;
        lastDir = "st";
        pre.innerHTML = lastDir;
        sendRequest('GET', '/manette', 'joystick', 'st' )
    });

</script>
<script>
    const slider = document.getElementById("myRange");
    const output = document.getElementById("sliderValue");
    slider.addEventListener("input", function () {
        const value = slider.value;
        output.innerHTML = value;
    });
</script>
<script>
     function sendRequest(method, type, name, dir) {
        console.log("send")
        // Init un variable de requête
        let xhttp = new XMLHttpRequest();
        let url = "/";
        // Donne les paramètres de la requête   ("methode", "action", true|false(Async))
        xhttp.open(method, url + `?${name}=${dir}`, true);
        // Informe que l'envoie correspond à un envoie de form (des données sont envoyées)
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        // Donne les informations "name"="value"&"name2"="value2"   pour récuperer la value c'est comme avec un input from("name")
        xhttp.send(`${name}=${dir}`);
        pre.innerHTML = dir;
        console.log("send dir" + dir)
    }
</script>

</html>"""


moteur_1 = Motor(16, 17)
moteur_2 = Motor(18, 5)
moteur_3 = Motor(27, 14)
moteur_4 = Motor(26, 25)
movement = Move(16, 17, 18, 5, 14, 27, 26, 25)


def main():
    my_ap = network.WLAN(network.AP_IF)
    my_ap.active(True)
    my_ap.config(essid='ESP-AP', authmode=network.AUTH_WPA_WPA2_PSK, password='123456789')
    display_ap_info(my_ap)

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.bind(('', 80))
    my_socket.listen(5)

    while True:

        conn, addr = my_socket.accept()
        print('Got a connection from %s' % str(addr))
        try:
            request = conn.recv(1024)
            request_str = str(request)
            print('request = ' + request_str + 'end request')
        except:
            print("err request")
            request_str = "error"

        if "joystick=davg" in request_str:
            print("davg")
            movement.mov("davg")

        elif "joystick=davd" in request_str:
            print("davd")
            movement.mov("davd")

        elif "joystick=av" in request_str:
            print("av")
            movement.mov("av")

        elif "joystick=ar" in request_str:
            print("ar")
            movement.mov("ar")

        elif "joystick=g" in request_str:
            print("g")
            movement.mov("g")

        elif "joystick=darg" in request_str:
            print("darg")
            movement.mov("darg")

        elif "joystick=dard" in request_str:
            print("dard")
            movement.mov("dard")

        elif "joystick=d" in request_str:
            print("d")
            movement.mov("d")

        elif "joystick=st" in request_str:
            print("stop")
            movement.mov("stop")

        elif "joystick=rotad" in request_str:
            print("rotad")
            movement.mov("rotad")

        elif "joystick=rotag" in request_str:
            print("rotag")
            movement.mov("rotag")
        else:
            print('No action')

        try:
            response = web_page()
            conn.write("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
            conn.send(response)
        except:
            print("erreur response")
        conn.close()


if __name__ == "__main__":
    main()


