import json
import os
from openpyxl import load_workbook
import openpyxl
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime as dt, timedelta
from sqlalchemy.exc import IntegrityError
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logistik.db'
db = SQLAlchemy(app)

migrate = Migrate(app, db)
def parse_date(date_string):
        if date_string:
            return dt.strptime(date_string, '%d-%m-%Y')
        return None

class Fahrzeug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fahrzeugkennung = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, fahrzeugkennung):
        self.fahrzeugkennung = fahrzeugkennung

    def to_dict(self):
        return {
            'id': self.id,
            'fahrzeugkennung': self.fahrzeugkennung
        }
    
def capitalize_first_letter(s):
    return s.capitalize() if s else s

class Bestellung(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    bestelldatum = db.Column(db.Date, default=dt.date, nullable=False)
    auftraggeber = db.Column(db.String(80), nullable=False)
    projekt = db.Column(db.String(80), nullable=False)
    bestellnummer = db.Column(db.String(80), nullable=True)
    bearbeiter = db.Column(db.String(80), nullable=False)
    fahrzeug_id = db.Column(db.Integer, ForeignKey('fahrzeug.id'), nullable=True)
    fahrzeug = relationship('Fahrzeug', backref='bestellungen')
    banf = db.Column(db.String(80), nullable=True)
    lieferant = db.Column(db.String(80), nullable=True)
    bemerkung = db.Column(db.String(255), nullable=True)
    teilenummer = db.Column(db.String(80), nullable=True)
    bezeichnung = db.Column(db.String(255), nullable=False)
    menge = db.Column(db.Integer, nullable=False)
    bezug = db.Column(db.String(80), nullable=False)
    liefertermin = db.Column(db.Date, nullable=True)
    liefertermin_status = db.Column(db.String(255), nullable=True)
    eingangsdatum = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(255), nullable=True)

    def __init__(self, **kwargs):
        super(Bestellung, self).__init__(**kwargs)
        self.auftraggeber = capitalize_first_letter(self.auftraggeber)
        self.projekt = capitalize_first_letter(self.projekt)
        self.bearbeiter = capitalize_first_letter(self.bearbeiter)
        self.lieferant = capitalize_first_letter(self.lieferant)
        self.bemerkung = capitalize_first_letter(self.bemerkung)
        self.bezeichnung = capitalize_first_letter(self.bezeichnung)
        
        if self.eingangsdatum is None:
            self.status = 'offen'
 
    def to_dict(self):
        return {
            'id': self.id,
            'bestelldatum': self.bestelldatum.strftime('%d-%m-%Y') if self.bestelldatum else '',
            'auftraggeber': self.auftraggeber,
            'projekt': self.projekt,
            'bestellnummer': self.bestellnummer,
            'bearbeiter': self.bearbeiter,
            'fahrzeug_id': self.fahrzeug_id,
            'banf': self.banf,
            'lieferant': self.lieferant,
            'bemerkung': self.bemerkung,
            'teilenummer': self.teilenummer,
            'bezeichnung': self.bezeichnung,
            'menge': self.menge,
            'bezug': self.bezug,
            'liefertermin': self.liefertermin.strftime('%d-%m-%Y') if self.liefertermin else '',
            'liefertermin_status': self.liefertermin_status,
            'eingangsdatum': self.eingangsdatum.strftime('%d-%m-%Y') if self.eingangsdatum else '',
            'status': self.status
        }

    __table_args__ = (
        CheckConstraint("bezug IN ('Lager', 'Extern', 'Werk 19', 'Werk 10', 'Hausteil')", name='bezug_options'),
        CheckConstraint("status IN ('offen', 'geliefert')", name='status_options'),
        CheckConstraint("liefertermin_status IN ('bestätigt', 'nicht bestätigt', 'überschritten')", name='liefertermin_status_options'),
    )

@app.route('/get-fahrzeuge')
def get_fahrzeuge():
    fahrzeuge = Fahrzeug.query.all()
    fahrzeug_liste = [{"id": f.id, "fahrzeugkennung": f.fahrzeugkennung} for f in fahrzeuge]
    return jsonify(fahrzeug_liste)

def get_today_date_string():
    """Gibt das heutige Datum im Format 'dd-mm-yyyy' zurück."""
    return dt.today().strftime('%d-%m-%Y')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.json
        app.logger.info("Empfangene Daten: %s", data)


        fahrzeug_id = data.get('fahrzeug_id')  
        fahrzeug = Fahrzeug.query.filter_by(id=fahrzeug_id).first()
        if not fahrzeug:
            app.logger.error("Fahrzeug mit der Kennung %s nicht gefunden", fahrzeug_id)
            return jsonify({'error': 'Fahrzeug mit der angegebenen Kennung nicht gefunden.'}), 400
        bestelldatum = parse_date(data['bestelldatum'])

        grunddaten = {
        'bestelldatum': bestelldatum,
        'auftraggeber': data['auftraggeber'],
        'projekt': data['projekt'],
        'bearbeiter': data['bearbeiter'],
        'fahrzeug_id': fahrzeug.id,
        'lieferant': data['lieferant'],
        'bemerkung': data['bemerkung'],
        }

        for row in data['tableRows']:
            if not all(key in row for key in ['teilenummer', 'bezeichnung', 'menge', 'bezug', 'liefertermin']):
                return "Missing required fields in table rows", 400

            liefertermin_obj = parse_date(row['liefertermin']).date() if row['liefertermin'] else None
            eingangsdatum_obj = parse_date(row.get('eingangsdatum')).date() if row.get('eingangsdatum') else None

            heute = dt.today().date()
            liefertermin_status = 'überschritten' if liefertermin_obj and liefertermin_obj < heute else 'nicht bestätigt'
            print(heute, liefertermin_obj)
            zeilen_banf = data['banf'] if row['bezug'] in ['Extern', 'Hausteil'] else None
            zeilen_bestellnummer = data['bestellnummer'] if row['bezug'] in ['Extern', 'Hausteil', 'Werk 10', 'Werk 19'] else None

       
            new_order = Bestellung(
                **grunddaten,
                bestellnummer = zeilen_bestellnummer,
                banf = zeilen_banf,
                teilenummer = row['teilenummer'],
                bezeichnung = row['bezeichnung'],
                menge = row['menge'],
                bezug = row['bezug'],
                liefertermin = liefertermin_obj,
                eingangsdatum = eingangsdatum_obj,
                liefertermin_status = liefertermin_status,  
                status='offen'   
            )
            db.session.add(new_order)

        db.session.commit()
        return jsonify({'message': 'complete'}), 201
    
    #Fehler-Handling
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Erforderliche Felder fehlen oder sind ungültig"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/bestellliste')
def bestellliste():
    return render_template('bestellliste.html')

@app.route('/api/bestellliste')
def api_bestellliste():
    bestellungen = Bestellung.query.all()
    bestellungen_data = [bestellung.to_dict() for bestellung in bestellungen]
    return jsonify(bestellungen_data)

@app.route('/update-order-bestellliste', methods=['PUT'])
def update_order_bestellliste():
    try:
        rows = request.get_json()
        for row in rows:
            bestellung_id = row[0]
            eingangsdatum = row[2]
            status = 'geliefert' if eingangsdatum else 'offen'

            if bestellung_id is not None:
                eingangsdatum_obj = dt.strptime(eingangsdatum, '%d-%m-%Y') if eingangsdatum else None
                Bestellung.query.filter_by(id=bestellung_id).update({'eingangsdatum': eingangsdatum_obj, 'status': status})
        
        db.session.commit()
        return jsonify({'message': 'Update erfolgreich'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/bestellliste_safe')
def bestellliste_safe():
    return render_template('bestellliste_safe.html')

@app.route('/saveData', methods=['PUT'])
def saveData():
    try:
        bestellungen_raw = request.get_json() 

        bestellungen = []
        for bestellung in bestellungen_raw:
            bestellungen.append({
                'id': bestellung[0],
                'bestelldatum': bestellung[1],
                'eingangsdatum': bestellung[2],
                'status': bestellung[3],
                'auftraggeber': bestellung[4],
                'bearbeiter': bestellung[5],
                'teilenummer': bestellung[6],
                'bezeichnung': bestellung[7],
                'menge': bestellung[8],
                'projekt': bestellung[9],
                'fahrzeugkennung': bestellung[10],  
                'bestellnummer': bestellung[11],
                'banf': bestellung[12],
                'lieferant': bestellung[13],
                'bemerkung': bestellung[14],
                'bezug': bestellung[15],
                'liefertermin': bestellung[16],
                'liefertermin_status': bestellung[17]
            })


        for bestellung_data in bestellungen:
            bestellung_id = bestellung_data.get('id')
            if bestellung_id is None:
                continue 

            bestellung = Bestellung.query.get(bestellung_id)
            if bestellung:
                
                bestellung.bestelldatum = parse_date(bestellung_data.get('bestelldatum', bestellung.bestelldatum))
                bestellung.auftraggeber = bestellung_data.get('auftraggeber', bestellung.auftraggeber)
                bestellung.bearbeiter = bestellung_data.get('bearbeiter', bestellung.bearbeiter)
                bestellung.teilenummer = bestellung_data.get('teilenummer', bestellung.teilenummer)
                bestellung.bezeichnung = bestellung_data.get('bezeichnung', bestellung.bezeichnung)
                bestellung.menge = bestellung_data.get('menge', bestellung.menge)
                bestellung.projekt = bestellung_data.get('projekt', bestellung.projekt)
                bestellung.fahrzeug_id = bestellung_data.get('fahrzeugkennung', bestellung.fahrzeug_id) # Stellen Sie sicher, dass das korrekte Feld hier verwendet wird
                bestellung.bestellnummer = bestellung_data.get('bestellnummer', bestellung.bestellnummer)
                bestellung.banf = bestellung_data.get('banf', bestellung.banf)
                bestellung.lieferant = bestellung_data.get('lieferant', bestellung.lieferant)
                bestellung.bemerkung = bestellung_data.get('bemerkung', bestellung.bemerkung)
                bestellung.bezug = bestellung_data.get('bezug', bestellung.bezug)
                bestellung.liefertermin = parse_date(bestellung_data.get('liefertermin', bestellung.liefertermin))
                bestellung.liefertermin_status = bestellung_data.get('liefertermin_status', bestellung.liefertermin_status)
                bestellung.eingangsdatum = parse_date(bestellung_data.get('eingangsdatum', bestellung.eingangsdatum))
                bestellung.status = bestellung_data.get('status', bestellung.status)

        db.session.commit()
        return jsonify({'message': 'Daten erfolgreich aktualisiert'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/bestellliste_master')
def bestellliste_master():
    return render_template('bestellliste_master.html')

@app.route('/startseite')
def startseite():
    return render_template('startseite.html')

@app.route('/api/ueberfaellige-lieferungen')
def ueberfaellige_lieferungen():
    heute = dt.today()
    ueberfaellige_lieferungen = Bestellung.query.filter(
        Bestellung.liefertermin < heute, 
        Bestellung.status != 'geliefert'
    ).all()

    bezug_count = {}
    for bestellung in ueberfaellige_lieferungen:
        bezug = bestellung.bezug
        bezug_count[bezug] = bezug_count.get(bezug, 0) + 1

    return jsonify(bezug_count)
@app.route('/api/bestellungen-nach-bezug')
def bestellungen_nach_bezug():
    start_datum = request.args.get('start', type=lambda s: dt.strptime(s, '%Y-%m-%d'))
    end_datum = request.args.get('end', type=lambda s: dt.strptime(s, '%Y-%m-%d'))
    bestellungen = Bestellung.query.filter(
        Bestellung.bestelldatum >= start_datum,
        Bestellung.bestelldatum <= end_datum
    ).all()
    bezug_count = {}
    for bestellung in bestellungen:
        bezug = bestellung.bezug
        if bezug not in bezug_count:
            bezug_count[bezug] = 0
        bezug_count[bezug] += 1

    return jsonify(bezug_count)
@app.route('/daten', methods=['GET'])
def daten_abrufen():
    teilenummer = request.args.get('teilenummer')
    try:
        bestellungen = Bestellung.query.filter_by(teilenummer=teilenummer, status='offen').all()
        filtered_data = [bestellung.to_dict() for bestellung in bestellungen]
        
        return jsonify(filtered_data)
    except Exception as e:
        return jsonify(error=str(e)), 500
def update_order(id):
    bestellung = Bestellung.query.filter_by(id=id).first()
    if bestellung:
        bestellung.eingangsdatum = parse_date(dt.today())
        bestellung.status = 'geliefert'
        db.session.commit()
        return True
    return False
@app.route('/update-order', methods=['PUT'])
def update_order_endpoint():
    try:
        data = request.get_json()
        id = data['id']
        if update_order(id):
            return jsonify(message="Bestellung erfolgreich aktualisiert"), 200
        else:
            return jsonify(error="Bestellung nicht gefunden"), 404
    except Exception as e:
        return jsonify(error=str(e)), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=12003)
