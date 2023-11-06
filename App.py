from flask import Flask,session,render_template,request,redirect,g,url_for,flash 
from flask_sqlalchemy import SQLAlchemy  
from functools import wraps


import os 

#               <------------------------------------Vardnica---------------------------------------------------->
# Flask - mikro web-framework Python valoda 
# session - objekts, kas uzglaba lietotaja sesijas informaciju.
# render_template - funkcija, kas rendere HTML failus no servera. 
# request - objekts, kas uzglaba informaciju no HTTP pieprasijuma.
# redirect - funkcija, kas paradrese uz citu vietni. 
# g - globals objekts Flask lietotaja informacijas uzglabasanai. 
# url_for - funkcija, kas genere URL adresi Flask lietotnei. 
# flash - funkcija, kas sagatavo zinojumu, kas tiks attelots lietotajam. 
# Flask SQLAlchemy - SQLAlchemy paplasinajums Flask lietotnem. 
# SQLAlchemy - Python ORM (Object Relational Mapping) biblioteka, kas lauj savienoties ar datu bazem. 
# functools - Python standarta biblioteka ar dažadam utilitprogrammam. 
# wraps - dekorators, kas saglaba funkcijas metadatus (piemeram, funkcijas nosaukumu un dokumentaciju) pec tas dekoresanas.
# Komanda "import os" ievada "os" biblioteku Python programma un lauj pieklut operetajsistemas funkcijam, 
## kuras var izmantot Python programmas izpildes laika. "os" biblioteka nodrosina iespeju izveidot, dzest, parvietot, 
### kopet failus, stradat ar failu celiem, ka ari pieklut operetajsistemas vides mainigajiem un citam sistemas funkcijam.
# wraps - wraps ir dekoratora funkcija, kas lauj saglabat orginalas funkcijas nosaukumu, dokumentaciju un argumentu informaciju.
# args - args ir Python funkcijas parametrs, kas lauj definet mainamo argumentu sarakstu funkcijas izsaukumam. Tas atlauj funkcijai pienemt vairakus argumentus.
# kwargs - kwargs ir Python funkcijas parametrs, kas lauj definet atslegu-vertibu parus ka argumentus funkcijas izsaukumam. Tas atlauj funkcijai pienemt vairakus argumentus, kurus var identificet ar atslegu-vertibu pariem.
#               <--------------------------------------------------------------------------------------------------->

# Definejam Flask lietotni un nosakam slepto atslegu:
app = Flask(__name__)          
app.secret_key = "Secret Key"  

# Konfigurejam SQLALchemy datu bazi. Noradam savienojuma virzienu un atslegu, ka ari atspejojam modifikacijas izsekosanu:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 



# Izveidojam SQLAlchemy objektu, kam padodam Flask lietotnes instanci, lai veiktu darbibas ar datu bazi:
db = SQLAlchemy(app) 


# saja koda definetas tris datubazes klases, kas atbilst tris tabulam datubaze. 
## Klases tiek definetas, izmantojot SQLAlchemy, kas ir Flask iestatijums, kas lauj viegli darboties ar datubazem. 
### Klases tiek defineti atributi, kas atbilst tabulas kolonnam, un konstruktors, kas inicialize objektus ar siem atributiem. 
#### sis klases tiek izmantotas, lai veidotu tabulas datubaze un apstradatu datus, kas tajas glabajas:

class Zivs(db.Model): 
    id = db.Column(db.Integer, primary_key = True) 
    vards = db.Column(db.String(100))
    vecums = db.Column(db.String(100))
    suga = db.Column(db.String(100))
    bariba = db.Column(db.String(100)) 

    def __init__(self, vards, vecums, suga, bariba):
        self.vards = vards 
        self.vecums = vecums 
        self.suga = suga 
        self.bariba = bariba 

class Barosana(db.Model): 
    id = db.Column(db.Integer, primary_key = True) 
    barosanas_datums = db.Column(db.String(100))
    baribas_nosaukums = db.Column(db.String(100)) 
    daudzums_mg = db.Column(db.String(100))  

    def __init__(self, barosanas_datums, baribas_nosaukums, daudzums_mg): 
        self.barosanas_datums = barosanas_datums 
        self.baribas_nosaukums = baribas_nosaukums 
        self.daudzums_mg = daudzums_mg

class Akvarijs(db.Model): 
    id = db.Column(db.Integer, primary_key = True) 
    datums = db.Column(db.String(100))
    tilpums_l = db.Column(db.String(100))
    temperatura_celsija_grados = db.Column(db.String(100)) 
    pH_limenis = db.Column(db.String(100)) 
    gaismas_limenis_W = db.Column(db.String(100)) 
    dulkainuma_limenis_ppm = db.Column(db.String(100)) 
    barosanas_id = db.Column(db.String(100)) 
    zivs_id = db.Column(db.String(100)) 


    def __init__(self, datums, tilpums_l, temperatura_celsija_grados, pH_limenis, gaismas_limenis_W, dulkainuma_limenis_ppm, barosanas_id, zivs_id):
        self.datums = datums 
        self.tilpums_l = tilpums_l 
        self.temperatura_celsija_grados = temperatura_celsija_grados 
        self.pH_limenis = pH_limenis 
        self.gaismas_limenis_W = gaismas_limenis_W 
        self.dulkainuma_limenis_ppm = dulkainuma_limenis_ppm 
        self.barosanas_id = barosanas_id 
        self.zivs_id = zivs_id 

# Funkcija "protected1" ir dekorators, kas define "wrapper" funkciju, kura parbauda, vai lietotajs ir autentificejies pirms izpildit "func" funkciju. 
## Ja lietotajs nav autentificejies, tiek veikta paradresacija uz "index" lapu. Ja lietotajs ir autentificejies, "func" funkcija tiek izpildita. 
### Funkcijas "wrapper" dekorators "wraps" nodrosina, ka funkcijas "func" nosaukums un dokuments saglabajas "wrapper" funkcija:
def protected1(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not g.user:
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return wrapper

# si ir funkcija, kas define marsrutu "/" vai saknes lapa. 
## Ja pieprasijuma metode ir "POST", funkcija izsauc sesijas "user" dzesanu un iegust lietotajvardu un paroli no ievaditajiem datiem. 
### Tad funkcija parbauda, vai ievaditais lietotajvards un parole ir pareizi. Ja tie ir pareizi, funkcija iestata sesijas "user" vertibu uz ievadito lietotajvardu un paradrese lietotaju uz aizsargatu lapu. 
#### Ja pieprasijuma metode nav "POST", funkcija atgriež "index.html" lapas HTML kodu:
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session.pop('user', None)

        username = request.form['username']
        password = request.form['password']

        # Check if username and password are correct
        if username == 'lietotajs' and password == 'password':
            session['user'] = username
            return redirect(url_for('protected'))

    return render_template('index.html') 


# saja Flask lietotnes marsruta ir definets aizsargats cels uz lapu, kas ir pieejama tikai autorizetiem lietotajiem. 
## Funkcijai ir pievienots "protected1" dekorators, kas parbauda, vai lietotajs ir autorizejies, izmantojot funkciju "wrapper". 
### Ja lietotajs nav autorizejies, funkcija novirza vinu atpakal uz sakuma lapu, izmantojot "redirect" funkciju. 
#### Ja lietotajs ir autorizejies, funkcija atgriež aizsargatas lapas saturu, izmantojot "render_template" funkciju:
@app.route('/protected') 
@protected1
def protected(): 
    return render_template('protected.html') 
    
# si funkcija tiek izpildita pirms katras pieprasijuma apstrades un iestatit globalu mainigo g.user, lai saglabatu informaciju par pasreizejo lietotaju. 
##Tas tiek darits, lai nodrosinatu, ka pieprasijuma apstrades laika var parbaudit, vai lietotajs ir autentificejies, un var istenot atbilstosus pasakumus, ja lietotajs nav autentificejies. 
### Tas tiek sasniegts, izmantojot session objektu, kura tiek glabata informacija par pasreizejo sesiju, un get() metodi, lai iegutu vertibu, kas ir saglabata user atslegas zema nosaukuma.
@app.before_request
def before_request():
    g.user = session.get('user') 


# si funkcija ir paredzeta lietotaja izrakstisanai no vietnes, izmantojot funkciju "session.pop", kas nonem lietotaja informaciju no sesijas. 
## Funkcija tiek aizsargata, izmantojot dekoratoru "protected1", kas prasa, lai lietotajs butu pieteicies, lai pieklutu sai lapai. 
### Kad lietotajs ir izrakstijies, tiek atgriezta sakuma lapas sagatave "index.html":
@app.route('/dropsession')
@protected1
def dropsession(): 
    session.pop('user', None) 
    return render_template('index.html') 

# sis kods define marsrutu "/zivs", kas ir aizsargata ar "protected1" dekoratoru. 
## saja marsruta tiek izpildita funkcija "Index", kas pieklust datubazes tabulai "Zivs" un atgriež visus tas ierakstus ka sarakstu "all_data". 
### Pec tam tiek atverta "index_zivs.html" lapa, kas tiek atgriezta ar sarakstu "zivis" ka argumentu:
@app.route('/zivs') 
@protected1
def Index(): 
    all_data = Zivs.query.all()

    return render_template("index_zivs.html", zivis = all_data) 

# saja koda fragmenta definets Flask rikraksta marsrutetajs, kas atbild uz POST pieprasijumiem, kas nosutiti uz `/insert` marsrutu. 
## Ja pieprasijuma metode ir POST, no pieprasijuma iegust vertibas un izveido jaunu `Zivs` ierakstu ar tam. 
### Tad sis jaunais ieraksts tiek pievienots datu bazei, izmantojot SQLAlchemy un `db.session.add()` un `db.session.commit()` metodes. 
#### Beigas lietotajam tiek paradits "Dati pievienoti veiksmigi" pazinojums un tiek paradresets uz `Index` marsrutu, izmantojot `redirect()` funkciju:
@app.route('/insert', methods = ['POST']) 
@protected1
def insert(): 

    if request.method == 'POST': 

        vards = request.form['vards'] 
        vecums = request.form['vecums'] 
        suga = request.form['suga'] 
        bariba = request.form['bariba'] 

        my_data = Zivs(vards, vecums, suga, bariba) 
        db.session.add(my_data) 
        db.session.commit() 

        flash("Dati pievienoti veiksmigi") 

        return redirect (url_for('Index')) 
    
# sis kods apraksta funkciju, kas atbild par datu redigesanu zivju datubaze. 
## Ja pieprasijuma metode ir POST, funkcija atgriež konkretas zivs datu izmainas datubaze. 
### Ja pieprasijuma metode ir GET, funkcija atgriež lapu ar formu, kura var veikt izmainas zivs datiem:
@app.route('/update', methods = ['GET', 'POST']) 
@protected1
def update(): 

    if request.method == 'POST': 
        my_data = Zivs.query.get(request.form.get('id'))

        my_data.vards = request.form['vards']
        my_data.vecums = request.form['vecums']
        my_data.suga = request.form['suga']
        my_data.bariba = request.form['bariba'] 

        db.session.commit() 
        flash("Dati Redigeti Veiksmig") 

        return redirect(url_for('Index')) 

# Funkcija delete ir route dekoreta ar @app.route('/delete/<id>/', methods = ['GET', 'POST']). 
## saja funkcija notiek ieraksta dzesana datubaze, kuru identifikators tiek nodots ka argumentu caur URL adresi. 
## Pec datu dzesanas veiksanas, tiek paradits "flash" zinojums par veiksmigi veiktajiem datu dzesanas darbibas. 
### Talak notiek paradresesana uz Index lapu, izmantojot redirect(url_for('Index')):
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
@protected1
def delete(id): 
    my_data = Zivs.query.get(id) 
    db.session.delete(my_data) 
    db.session.commit() 
    flash("Dati Dzesti Veiksmigi") 

    return redirect(url_for('Index')) 

#Talak process atkartojas:
@app.route('/akvarijs') 
@protected1
def akvarijs(): 
   all_data1 = Akvarijs.query.all() 
   return render_template ("index_akvarijs.html", udens = all_data1)   

@app.route('/barosana') 
@protected1
def barosana(): 
    all_data2 = Barosana.query.all()  
    return render_template ("index_barosana.html", namnam = all_data2)

@app.route('/insert1', methods = ["POST"])
@protected1
def insert1(): 

    if request.method == 'POST': 

        barosanas_datums = request.form['barosanas_datums']
        baribas_nosaukums = request.form['baribas_nosaukums']
        daudzums_mg = request.form['daudzums_mg'] 

        my_data1 = Barosana(barosanas_datums, baribas_nosaukums, daudzums_mg)
        db.session.add(my_data1) 
        db.session.commit() 

        flash("Dati Pievienoti Veiksmigi") 

        return redirect(url_for('barosana')) 

@app.route('/insert2', methods = ["POST"])
@protected1
def insert2(): 

    if request.method == 'POST': 

        datums = request.form['datums'] 
        tilpums_l = request.form['tilpums_l'] 
        temperatura_celsija_grados = request.form['temperatura_celsija_grados'] 
        pH_limenis = request.form['pH_limenis'] 
        gaismas_limenis_W =  request.form['gaismas_limenis_W'] 
        dulkainuma_limenis_ppm =  request.form['dulkainuma_limenis_ppm'] 
        barosanas_id = request.form['barosanas_id'] 
        zivs_id = request.form['zivs_id'] 

        my_data2 = Akvarijs(datums, tilpums_l, temperatura_celsija_grados, pH_limenis, gaismas_limenis_W, dulkainuma_limenis_ppm, barosanas_id, zivs_id)
        db.session.add(my_data2) 
        db.session.commit()


        flash("Dati Pievienoti Veiksmigi") 

        return redirect(url_for('akvarijs'))  

@app.route('/update1', methods = ['GET', 'POST'])  
@protected1
def update1(): 

    if request.method == 'POST': 
        my_data1 = Akvarijs.query.get(request.form.get('id')) 

        my_data1.datums = request.form['datums'] 
        my_data1.tilpums_l = request.form['tilpums_l'] 
        my_data1.temperatura_celsija_grados = request.form['temperatura_celsija_grados'] 
        my_data1.pH_limenis = request.form['pH_limenis'] 
        my_data1.gaismas_limenis_W = request.form['gaismas_limenis_W'] 
        my_data1.dulkainuma_limenis_ppm = request.form['dulkainuma_limenis_ppm'] 
        my_data1.barosanas_id = request.form['barosanas_id'] 
        my_data1.zivs_id = request.form['zivs_id']  

        db.session.commit() 
        flash("Dati Redigeti Veiksmigi")

        return redirect(url_for('akvarijs')) 

@app.route('/update2', methods = ['GET', 'POST'])  
@protected1
def update2(): 

    if request.method == 'POST': 
        my_data2 = Barosana.query.get(request.form.get('id')) 

        my_data2.barosanas_datums = request.form['barosanas_datums']
        my_data2.baribas_nosaukums = request.form['baribas_nosaukums']
        my_data2.daudzums_mg = request.form['daudzums_mg'] 

        db.session.commit() 
        flash("Dati Redigeti Veiksmigi") 

        return redirect(url_for('barosana')) 

@app.route('/delete1/<id>/', methods = ['GET', 'POST'])
@protected1
def delete1(id): 
    my_data3 = Akvarijs.query.get(id) 
    db.session.delete(my_data3) 
    db.session.commit() 
    flash("Dati Dzesti Veiksmigi") 

    return redirect(url_for('akvarijs')) 

@app.route('/delete2/<id>/', methods = ['GET', 'POST'])
@protected1
def delete2(id): 
    my_data4 = Barosana.query.get(id) 
    db.session.delete(my_data4) 
    db.session.commit() 
    flash("Dati Dzesti Veiksmigi") 

    return redirect(url_for('barosana')) 

# si rinda koda parbauda, vai sis fails tiek izpildits ka galvenais fails (main file), kas tiek palaists tiesi no komandrindas, un tikai tad palaiž Flask aplikaciju ar debug režimu. 
# Tas ir noderigi, lai noverstu aplikacijas startesanu, ja tas tiek importets cita faila ka modulis.
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)  