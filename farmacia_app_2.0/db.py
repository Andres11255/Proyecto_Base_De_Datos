import json
import os
import random
from datetime import datetime, timedelta

print("Cargando db.py (Versión JSON Local)...")

DB_FILE = "farmacia_db.json"

MEDICAMENTOS_DEFECTO = [('Paracetamol', 'Dolor y Fiebre'), ('Ibuprofeno', 'Dolor y Fiebre'), ('Naproxeno', 'Dolor y Fiebre'), ('Diclofenaco', 'Dolor y Fiebre'), ('Aspirina', 'Dolor y Fiebre'), ('Ketorolaco', 'Dolor y Fiebre'), ('Metamizol', 'Dolor y Fiebre'), ('Tramadol', 'Dolor y Fiebre'), ('Celecoxib', 'Dolor y Fiebre'), ('Meloxicam', 'Dolor y Fiebre'), ('Piroxicam', 'Dolor y Fiebre'), ('Indometacina', 'Dolor y Fiebre'), ('Clonixinato de lisina', 'Dolor y Fiebre'), ('Dexketoprofeno', 'Dolor y Fiebre'), ('Buprenorfina', 'Dolor y Fiebre'), ('Morfina', 'Dolor y Fiebre'), ('Oxycodona', 'Dolor y Fiebre'), ('Fentanilo', 'Dolor y Fiebre'), ('Nimesulida', 'Dolor y Fiebre'), ('Etoricoxib', 'Dolor y Fiebre'), ('Acetaminofén', 'Dolor y Fiebre'), ('Dipirona', 'Dolor y Fiebre'), ('Loratadina', 'Alergias'), ('Cetirizina', 'Alergias'), ('Clorfenamina', 'Alergias'), ('Desloratadina', 'Alergias'), ('Fexofenadina', 'Alergias'), ('Levocetirizina', 'Alergias'), ('Difenhidramina', 'Alergias'), ('Epinastina', 'Alergias'), ('Ketotifeno', 'Alergias'), ('Mometasona', 'Alergias'), ('Fluticasona', 'Alergias'), ('Budesonida', 'Alergias'), ('Rupatadina', 'Alergias'), ('Ebastina', 'Alergias'), ('Bilastina', 'Alergias'), ('Hidroxicina', 'Alergias'), ('Clemastina', 'Alergias'), ('Azelastina', 'Alergias'), ('Olopatadina', 'Alergias'), ('Emedastina', 'Alergias'), ('Ambroxol', 'Tos y Gripe'), ('Dextrometorfano', 'Tos y Gripe'), ('Guaifenesina', 'Tos y Gripe'), ('Bromhexina', 'Tos y Gripe'), ('Benzonatato', 'Tos y Gripe'), ('Levodropropizina', 'Tos y Gripe'), ('Oxolamina', 'Tos y Gripe'), ('Clopiperastina', 'Tos y Gripe'), ('Hedera Helix', 'Tos y Gripe'), ('Salbutamol', 'Tos y Gripe'), ('Fenilefrina', 'Tos y Gripe'), ('Pseudoefedrina', 'Tos y Gripe'), ('Oximetazolina', 'Tos y Gripe'), ('Nafazolina', 'Tos y Gripe'), ('Xilometazolina', 'Tos y Gripe'), ('Terbutalina', 'Tos y Gripe'), ('Formoterol', 'Tos y Gripe'), ('Salmeterol', 'Tos y Gripe'), ('Ipratropio', 'Tos y Gripe'), ('Tiotropio', 'Tos y Gripe'), ('Montelukast', 'Tos y Gripe'), ('Zafirlukast', 'Tos y Gripe'), ('Amoxicilina', 'Infecciones Bacterianas'), ('Ampicilina', 'Infecciones Bacterianas'), ('Ciprofloxacino', 'Infecciones Bacterianas'), ('Azitromicina', 'Infecciones Bacterianas'), ('Cefalexina', 'Infecciones Bacterianas'), ('Ceftriaxona', 'Infecciones Bacterianas'), ('Claritromicina', 'Infecciones Bacterianas'), ('Levofloxacino', 'Infecciones Bacterianas'), ('Clindamicina', 'Infecciones Bacterianas'), ('Eritromicina', 'Infecciones Bacterianas'), ('Doxiciclina', 'Infecciones Bacterianas'), ('Tetraciclina', 'Infecciones Bacterianas'), ('Gentamicina', 'Infecciones Bacterianas'), ('Amikacina', 'Infecciones Bacterianas'), ('Nitrofurantoína', 'Infecciones Bacterianas'), ('Trimetoprima', 'Infecciones Bacterianas'), ('Sulfametoxazol', 'Infecciones Bacterianas'), ('Cefotaxima', 'Infecciones Bacterianas'), ('Cefuroxima', 'Infecciones Bacterianas'), ('Cefaclor', 'Infecciones Bacterianas'), ('Dicloxacilina', 'Infecciones Bacterianas'), ('Penicilina', 'Infecciones Bacterianas'), ('Meropenem', 'Infecciones Bacterianas'), ('Imipenem', 'Infecciones Bacterianas'), ('Aciclovir', 'Infecciones Virales'), ('Valaciclovir', 'Infecciones Virales'), ('Oseltamivir', 'Infecciones Virales'), ('Zanamivir', 'Infecciones Virales'), ('Amantadina', 'Infecciones Virales'), ('Rimantadina', 'Infecciones Virales'), ('Ribavirina', 'Infecciones Virales'), ('Ganciclovir', 'Infecciones Virales'), ('Famciclovir', 'Infecciones Virales'), ('Foscarnet', 'Infecciones Virales'), ('Entecavir', 'Infecciones Virales'), ('Tenofovir', 'Infecciones Virales'), ('Lamivudina', 'Infecciones Virales'), ('Efavirenz', 'Infecciones Virales'), ('Lopinavir', 'Infecciones Virales'), ('Ritonavir', 'Infecciones Virales'), ('Darunavir', 'Infecciones Virales'), ('Dolutegravir', 'Infecciones Virales'), ('Raltegravir', 'Infecciones Virales'), ('Maraviroc', 'Infecciones Virales'), ('Fluconazol', 'Infecciones por Hongos'), ('Ketoconazol', 'Infecciones por Hongos'), ('Itraconazol', 'Infecciones por Hongos'), ('Clotrimazol', 'Infecciones por Hongos'), ('Miconazol', 'Infecciones por Hongos'), ('Terbinafina', 'Infecciones por Hongos'), ('Nistatina', 'Infecciones por Hongos'), ('Griseofulvina', 'Infecciones por Hongos'), ('Voriconazol', 'Infecciones por Hongos'), ('Posaconazol', 'Infecciones por Hongos'), ('Caspofungina', 'Infecciones por Hongos'), ('Micafungina', 'Infecciones por Hongos'), ('Anidulafungina', 'Infecciones por Hongos'), ('Amfotericina B', 'Infecciones por Hongos'), ('Tioconazol', 'Infecciones por Hongos'), ('Econazol', 'Infecciones por Hongos'), ('Sertaconazol', 'Infecciones por Hongos'), ('Bifonazol', 'Infecciones por Hongos'), ('Ciclopirox', 'Infecciones por Hongos'), ('Amorolfina', 'Infecciones por Hongos'), ('Omeprazol', 'Problemas Estomacales'), ('Pantoprazol', 'Problemas Estomacales'), ('Esomeprazol', 'Problemas Estomacales'), ('Lansoprazol', 'Problemas Estomacales'), ('Rabeprazol', 'Problemas Estomacales'), ('Ranitidina', 'Problemas Estomacales'), ('Famotidina', 'Problemas Estomacales'), ('Subsalicilato de bismuto', 'Problemas Estomacales'), ('Magaldrato', 'Problemas Estomacales'), ('Hidróxido de aluminio', 'Problemas Estomacales'), ('Hidróxido de magnesio', 'Problemas Estomacales'), ('Simeticona', 'Problemas Estomacales'), ('Metoclopramida', 'Problemas Estomacales'), ('Ondansetrón', 'Problemas Estomacales'), ('Domperidona', 'Problemas Estomacales'), ('Cisaprida', 'Problemas Estomacales'), ('Trimebutina', 'Problemas Estomacales'), ('Pinaverio', 'Problemas Estomacales'), ('Mebeverina', 'Problemas Estomacales'), ('Loperamida', 'Problemas Estomacales'), ('Racecadotrilo', 'Problemas Estomacales'), ('Diosmectita', 'Problemas Estomacales'), ('Probióticos', 'Problemas Estomacales'), ('Senósidos', 'Problemas Estomacales'), ('Bisacodilo', 'Problemas Estomacales'), ('Lactulosa', 'Problemas Estomacales'), ('Plantago psyllium', 'Problemas Estomacales'), ('Polietilenglicol', 'Problemas Estomacales'), ('Butilhioscina', 'Problemas Estomacales'), ('Pargeverina', 'Problemas Estomacales'), ('Losartán', 'Hipertensión y Corazón'), ('Telmisartán', 'Hipertensión y Corazón'), ('Valsartán', 'Hipertensión y Corazón'), ('Candesartán', 'Hipertensión y Corazón'), ('Irbesartán', 'Hipertensión y Corazón'), ('Enalapril', 'Hipertensión y Corazón'), ('Captopril', 'Hipertensión y Corazón'), ('Lisinopril', 'Hipertensión y Corazón'), ('Ramipril', 'Hipertensión y Corazón'), ('Amlodipino', 'Hipertensión y Corazón'), ('Nifedipino', 'Hipertensión y Corazón'), ('Felodipino', 'Hipertensión y Corazón'), ('Diltiazem', 'Hipertensión y Corazón'), ('Verapamilo', 'Hipertensión y Corazón'), ('Atenolol', 'Hipertensión y Corazón'), ('Metoprolol', 'Hipertensión y Corazón'), ('Propranolol', 'Hipertensión y Corazón'), ('Bisoprolol', 'Hipertensión y Corazón'), ('Carvedilol', 'Hipertensión y Corazón'), ('Nebivolol', 'Hipertensión y Corazón'), ('Furosemida', 'Hipertensión y Corazón'), ('Hidroclorotiazida', 'Hipertensión y Corazón'), ('Espironolactona', 'Hipertensión y Corazón'), ('Clortalidona', 'Hipertensión y Corazón'), ('Indapamida', 'Hipertensión y Corazón'), ('Atorvastatina', 'Hipertensión y Corazón'), ('Simvastatina', 'Hipertensión y Corazón'), ('Pravastatina', 'Hipertensión y Corazón'), ('Rosuvastatina', 'Hipertensión y Corazón'), ('Bezafibrato', 'Hipertensión y Corazón'), ('Fenofibrato', 'Hipertensión y Corazón'), ('Aspirina Protect', 'Hipertensión y Corazón'), ('Clopidogrel', 'Hipertensión y Corazón'), ('Prasugrel', 'Hipertensión y Corazón'), ('Ticagrelor', 'Hipertensión y Corazón'), ('Warfarina', 'Hipertensión y Corazón'), ('Acenocumarol', 'Hipertensión y Corazón'), ('Rivaroxabán', 'Hipertensión y Corazón'), ('Apixabán', 'Hipertensión y Corazón'), ('Dabigatrán', 'Hipertensión y Corazón'), ('Metformina', 'Diabetes'), ('Glibenclamida', 'Diabetes'), ('Glimepirida', 'Diabetes'), ('Gliclazida', 'Diabetes'), ('Pioglitazona', 'Diabetes'), ('Rosiglitazona', 'Diabetes'), ('Sitagliptina', 'Diabetes'), ('Vildagliptina', 'Diabetes'), ('Saxagliptina', 'Diabetes'), ('Linagliptina', 'Diabetes'), ('Exenatida', 'Diabetes'), ('Liraglutida', 'Diabetes'), ('Dulaglutida', 'Diabetes'), ('Semaglutida', 'Diabetes'), ('Dapagliflozina', 'Diabetes'), ('Empagliflozina', 'Diabetes'), ('Canagliflozina', 'Diabetes'), ('Insulina Rápida', 'Diabetes'), ('Insulina NPH', 'Diabetes'), ('Insulina Glargina', 'Diabetes'), ('Insulina Detemir', 'Diabetes'), ('Insulina Degludec', 'Diabetes'), ('Acarbosa', 'Diabetes'), ('Miglitol', 'Diabetes'), ('Fluoxetina', 'Ansiedad y Depresión'), ('Sertralina', 'Ansiedad y Depresión'), ('Paroxetina', 'Ansiedad y Depresión'), ('Citalopram', 'Ansiedad y Depresión'), ('Escitalopram', 'Ansiedad y Depresión'), ('Venlafaxina', 'Ansiedad y Depresión'), ('Desvenlafaxina', 'Ansiedad y Depresión'), ('Duloxetina', 'Ansiedad y Depresión'), ('Mirtazapina', 'Ansiedad y Depresión'), ('Bupropión', 'Ansiedad y Depresión'), ('Amitriptilina', 'Ansiedad y Depresión'), ('Imipramina', 'Ansiedad y Depresión'), ('Clomipramina', 'Ansiedad y Depresión'), ('Diazepam', 'Ansiedad y Depresión'), ('Clonazepam', 'Ansiedad y Depresión'), ('Alprazolam', 'Ansiedad y Depresión'), ('Lorazepam', 'Ansiedad y Depresión'), ('Bromazepam', 'Ansiedad y Depresión'), ('Midazolam', 'Ansiedad y Depresión'), ('Zolpidem', 'Ansiedad y Depresión'), ('Zopiclona', 'Ansiedad y Depresión'), ('Pregabalina', 'Ansiedad y Depresión'), ('Gabapentina', 'Ansiedad y Depresión'), ('Valproato', 'Ansiedad y Depresión'), ('Carbamazepina', 'Ansiedad y Depresión'), ('Oxcarbazepina', 'Ansiedad y Depresión'), ('Levetiracetam', 'Ansiedad y Depresión'), ('Topiramato', 'Ansiedad y Depresión'), ('Lamotrigina', 'Ansiedad y Depresión'), ('Fenitoína', 'Ansiedad y Depresión'), ('Hipromelosa', 'Cuidado Ocular'), ('Hialuronato de sodio', 'Cuidado Ocular'), ('Nafazolina ocular', 'Cuidado Ocular'), ('Timolol', 'Cuidado Ocular'), ('Bimatoprost', 'Cuidado Ocular'), ('Latanoprost', 'Cuidado Ocular'), ('Travoprost', 'Cuidado Ocular'), ('Dorzolamida', 'Cuidado Ocular'), ('Brimonidina', 'Cuidado Ocular'), ('Prednisolona ocular', 'Cuidado Ocular'), ('Dexametasona ocular', 'Cuidado Ocular'), ('Diclofenaco ocular', 'Cuidado Ocular'), ('Ketorolaco ocular', 'Cuidado Ocular'), ('Ciprofloxacino ocular', 'Cuidado Ocular'), ('Tobramicina ocular', 'Cuidado Ocular'), ('Eritromicina ocular', 'Cuidado Ocular'), ('Cloranfenicol ocular', 'Cuidado Ocular'), ('Tetracaína', 'Cuidado Ocular'), ('Proparacaína', 'Cuidado Ocular'), ('Pilocarpina', 'Cuidado Ocular'), ('Hidrocortisona tópica', 'Cuidado de la Piel'), ('Betametasona', 'Cuidado de la Piel'), ('Clobetasol', 'Cuidado de la Piel'), ('Desonida', 'Cuidado de la Piel'), ('Mupirocina', 'Cuidado de la Piel'), ('Ácido fusídico', 'Cuidado de la Piel'), ('Retinol', 'Cuidado de la Piel'), ('Tretinoína', 'Cuidado de la Piel'), ('Adapaleno', 'Cuidado de la Piel'), ('Peróxido de benzoilo', 'Cuidado de la Piel'), ('Ácido salicílico', 'Cuidado de la Piel'), ('Clindamicina tópica', 'Cuidado de la Piel'), ('Eritromicina tópica', 'Cuidado de la Piel'), ('Calamina', 'Cuidado de la Piel'), ('Óxido de zinc', 'Cuidado de la Piel'), ('Pantenol', 'Cuidado de la Piel'), ('Urea', 'Cuidado de la Piel'), ('Ácido hialurónico', 'Cuidado de la Piel'), ('Colágeno', 'Cuidado de la Piel'), ('Minoxidil', 'Cuidado de la Piel'), ('Finasterida', 'Cuidado de la Piel'), ('Ketoconazol champú', 'Cuidado de la Piel'), ('Alquitrán de hulla', 'Cuidado de la Piel'), ('Vitamina C', 'Vitaminas y Suplementos'), ('Vitamina D3', 'Vitaminas y Suplementos'), ('Vitamina E', 'Vitaminas y Suplementos'), ('Vitamina A', 'Vitaminas y Suplementos'), ('Vitamina B12', 'Vitaminas y Suplementos'), ('Vitamina B6', 'Vitaminas y Suplementos'), ('Complejo B', 'Vitaminas y Suplementos'), ('Ácido Fólico', 'Vitaminas y Suplementos'), ('Hierro', 'Vitaminas y Suplementos'), ('Calcio', 'Vitaminas y Suplementos'), ('Magnesio', 'Vitaminas y Suplementos'), ('Zinc', 'Vitaminas y Suplementos'), ('Potasio', 'Vitaminas y Suplementos'), ('Omega 3', 'Vitaminas y Suplementos'), ('Glucosamina', 'Vitaminas y Suplementos'), ('Condroitina', 'Vitaminas y Suplementos'), ('Colágeno Hidrolizado', 'Vitaminas y Suplementos'), ('Biotina', 'Vitaminas y Suplementos'), ('Melatonina', 'Vitaminas y Suplementos'), ('Ginseng', 'Vitaminas y Suplementos'), ('Ginkgo Biloba', 'Vitaminas y Suplementos'), ('Espirulina', 'Vitaminas y Suplementos'), ('Maca', 'Vitaminas y Suplementos'), ('Cúrcuma', 'Vitaminas y Suplementos'), ('Albendazol', 'Antiparasitarios'), ('Mebendazol', 'Antiparasitarios'), ('Quinfamida', 'Antiparasitarios'), ('Secnidazol', 'Antiparasitarios'), ('Nitazoxanida', 'Antiparasitarios'), ('Metronidazol', 'Antiparasitarios'), ('Tinidazol', 'Antiparasitarios'), ('Ivermectina', 'Antiparasitarios'), ('Prazicuantel', 'Antiparasitarios'), ('Pirantel', 'Antiparasitarios'), ('Levotiroxina', 'Tiroides y Hormonas'), ('Liotironina', 'Tiroides y Hormonas'), ('Tiamazol', 'Tiroides y Hormonas'), ('Propiltiouracilo', 'Tiroides y Hormonas'), ('Estradiol', 'Tiroides y Hormonas'), ('Progesterona', 'Tiroides y Hormonas'), ('Testosterona', 'Tiroides y Hormonas'), ('Dexametasona', 'Tiroides y Hormonas'), ('Prednisona', 'Tiroides y Hormonas'), ('Metilprednisolona', 'Tiroides y Hormonas'), ('Deflazacort', 'Tiroides y Hormonas'), ('Fludrocortisona', 'Tiroides y Hormonas')]


def _crear_base_datos_inicial():
    datos = {
        "medicamentos": [],
        "ventas": [],
        "ventas_historicas": [],
        "seq_medicamento": 1,
        "seq_venta": 1,
        "seq_venta_historica": 1
    }
    
    # Inicializar con los medicamentos por defecto
    for med, sintoma in MEDICAMENTOS_DEFECTO:
        stock = random.randint(15, 100)
        compra = float(random.randint(10, 500))
        venta = compra + float(random.randint(10, 200))
        
        item = {
            "id": datos["seq_medicamento"],
            "nombre": med,
            "stock": stock,
            "precio_compra": compra,
            "precio_venta": venta,
            "fecha_caducidad": "2026-12-31",
            "sintoma": sintoma
        }
        datos["medicamentos"].append(item)
        datos["seq_medicamento"] += 1
        
    return datos

def _cargar_datos():
    if not os.path.exists(DB_FILE):
        datos = _crear_base_datos_inicial()
        _guardar_datos(datos)
        return datos
    
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _guardar_datos(datos):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def _tupla_medicamento(item):
    return (
        item["id"],
        item["nombre"],
        item["stock"],
        item["precio_compra"],
        item["precio_venta"],
        item["fecha_caducidad"],
        item["sintoma"]
    )

def conectar():
    # Simula la conexión, asegurándose que la bd existe.
    try:
        print("Cargando base de datos local JSON...")
        _cargar_datos()
        print("Carga exitosa.")
        return True
    except Exception as e:
        print("ERROR REAL:", e)
        return False

# ===============================
# INSERTAR MEDICAMENTO
# ===============================
def insertar_medicamento(nombre, stock, compra, venta, fecha, sintoma):
    datos = _cargar_datos()
    nuevo_id = datos["seq_medicamento"]
    datos["seq_medicamento"] += 1
    
    nuevo_item = {
        "id": nuevo_id,
        "nombre": nombre,
        "stock": stock,
        "precio_compra": compra,
        "precio_venta": venta,
        "fecha_caducidad": fecha,
        "sintoma": sintoma
    }
    datos["medicamentos"].append(nuevo_item)
    _guardar_datos(datos)

# ===============================
# OBTENER MEDICAMENTOS
# ===============================
def obtener_medicamentos():
    datos = _cargar_datos()
    return [_tupla_medicamento(m) for m in datos["medicamentos"]]

# ===============================
# BUSCAR MEDICAMENTOS POR NOMBRE
# ===============================
def buscar_medicamentos(texto):
    datos = _cargar_datos()
    texto = texto.lower()
    resultados = [m for m in datos["medicamentos"] if texto in m["nombre"].lower()]
    return [_tupla_medicamento(m) for m in resultados]

# ===============================
# BUSCAR MEDICAMENTOS POR SÍNTOMA
# ===============================
def buscar_por_sintoma(sintoma):
    datos = _cargar_datos()
    sintoma = sintoma.lower()
    resultados = [m for m in datos["medicamentos"] if sintoma in m["sintoma"].lower()]
    return [_tupla_medicamento(m) for m in resultados]

# ===============================
# ELIMINAR MEDICAMENTO
# ===============================
def eliminar_medicamento(id_med):
    datos = _cargar_datos()
    datos["medicamentos"] = [m for m in datos["medicamentos"] if m["id"] != id_med]
    # No eliminamos el historial porque no hay ON DELETE CASCADE automático en JSON.
    _guardar_datos(datos)

# ===============================
# VENDER MEDICAMENTO
# ===============================
def vender_medicamento(id_med, cantidad):
    datos = _cargar_datos()
    
    for m in datos["medicamentos"]:
        if m["id"] == id_med:
            if m["stock"] >= cantidad:
                m["stock"] -= cantidad
                
                nueva_venta = {
                    "id": datos["seq_venta"],
                    "medicamento_id": id_med,
                    "cantidad": cantidad,
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                datos["ventas"].append(nueva_venta)
                datos["seq_venta"] += 1
                
                _guardar_datos(datos)
                print("Venta realizada y registrada exitosamente")
                return
            else:
                print("Stock insuficiente")
                return
    print("Medicamento no encontrado")

# ===============================
# MEDICAMENTOS POR CADUCAR
# ===============================
def obtener_por_caducar(dias=30):
    datos = _cargar_datos()
    limite = datetime.now() + timedelta(days=dias)
    resultados = []
    
    for m in datos["medicamentos"]:
        try:
            fecha_dt = datetime.strptime(m["fecha_caducidad"], "%Y-%m-%d")
            if fecha_dt <= limite:
                resultados.append(m)
        except:
            pass
            
    return [_tupla_medicamento(m) for m in resultados]

# ===============================
# VENTAS AGRUPADAS POR MEDICAMENTO
# ===============================
def ventas_por_medicamento():
    datos = _cargar_datos()
    ventas_agrupadas = {}
    
    # Crear un diccionario para encontrar los medicamentos por id fácilmente
    med_dict = {m["id"]: m for m in datos["medicamentos"]}
    
    for v in datos["ventas"]:
        med_id = v["medicamento_id"]
        cantidad = v["cantidad"]
        if med_id in med_dict:
            m = med_dict[med_id]
            nombre = m["nombre"]
            precio = float(m["precio_venta"])
            
            if nombre not in ventas_agrupadas:
                ventas_agrupadas[nombre] = {"cantidad": 0, "ingreso": 0.0}
            
            ventas_agrupadas[nombre]["cantidad"] += cantidad
            ventas_agrupadas[nombre]["ingreso"] += cantidad * precio
            
    # Formato de retorno: lista de tuplas (nombre, cantidad, ingreso)
    return [(nombre, v["cantidad"], v["ingreso"]) for nombre, v in ventas_agrupadas.items()]

# ===============================
# STOCK BAJO
# ===============================
def obtener_stock_bajo(limite=20):
    datos = _cargar_datos()
    resultados = [m for m in datos["medicamentos"] if m["stock"] <= limite]
    return [_tupla_medicamento(m) for m in resultados]

# ===============================
# AÑADIR STOCK
# ===============================
def agregar_stock_medicamento(id_med, cantidad):
    datos = _cargar_datos()
    for m in datos["medicamentos"]:
        if m["id"] == id_med:
            m["stock"] += cantidad
            _guardar_datos(datos)
            return

# ===============================
# ARCHIVAR VENTAS (CERRAR SEMANA)
# ===============================
def archivar_ventas_semana():
    try:
        datos = _cargar_datos()
        
        fecha_corte = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        for v in datos["ventas"]:
            venta_hist = {
                "id": datos["seq_venta_historica"],
                "medicamento_id": v["medicamento_id"],
                "cantidad": v["cantidad"],
                "fecha_venta": v["fecha"],
                "fecha_corte": fecha_corte
            }
            datos["ventas_historicas"].append(venta_hist)
            datos["seq_venta_historica"] += 1
            
        datos["ventas"] = [] # Vaciar ventas actuales
        _guardar_datos(datos)
        return True
    except Exception as e:
        print("Error al archivar ventas:", e)
        return False

# ===============================
# ACTUALIZACIÓN MASIVA DE CADUCIDADES
# ===============================
def actualizar_caducidades_masivas():
    datos = _cargar_datos()
    ids = [m["id"] for m in datos["medicamentos"]]
    
    if len(ids) <= 4:
        return
        
    ids_ignorados = random.sample(ids, 4)
    
    for m in datos["medicamentos"]:
        if m["id"] not in ids_ignorados:
            try:
                dt = datetime.strptime(m["fecha_caducidad"], "%Y-%m-%d")
                nueva_dt = dt.replace(year=dt.year + 1)
                m["fecha_caducidad"] = nueva_dt.strftime("%Y-%m-%d")
            except:
                pass
                
    _guardar_datos(datos)
    print("Caducidades actualizadas masivamente (se ignoraron 4).")

# ===============================
# OBTENER HISTORIAL DE VENTAS POR SEMANA
# ===============================
def obtener_historial_por_semanas():
    datos = _cargar_datos()
    
    # Agrupar por (fecha_corte (solo dia), nombre_medicamento)
    # Retorna: (semana, nombre, total_vendido, total_ingreso)
    agrupacion = {}
    med_dict = {m["id"]: m for m in datos["medicamentos"]}
    
    for v in datos["ventas_historicas"]:
        med_id = v["medicamento_id"]
        if med_id in med_dict:
            m = med_dict[med_id]
            nombre = m["nombre"]
            precio = float(m["precio_venta"])
            
            # Solo la fecha yyyy-mm-dd
            semana = v["fecha_corte"].split(" ")[0]
            
            key = (semana, nombre)
            if key not in agrupacion:
                agrupacion[key] = {"total_vendido": 0, "total_ingreso": 0.0}
                
            agrupacion[key]["total_vendido"] += v["cantidad"]
            agrupacion[key]["total_ingreso"] += v["cantidad"] * precio
            
    lista = []
    for (semana, nombre), valores in agrupacion.items():
        lista.append((semana, nombre, valores["total_vendido"], valores["total_ingreso"]))
        
    # Ordenar por semana DESC, total_ingreso DESC
    lista.sort(key=lambda x: (x[0], x[3]), reverse=True)
    return lista