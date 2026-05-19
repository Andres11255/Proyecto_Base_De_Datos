import random
import re

sintomas_medicamentos = {
    'Dolor y Fiebre': ['Paracetamol', 'Ibuprofeno', 'Naproxeno', 'Diclofenaco', 'Aspirina', 'Ketorolaco', 'Metamizol', 'Tramadol', 'Celecoxib', 'Meloxicam', 'Piroxicam', 'Indometacina', 'Clonixinato de lisina', 'Dexketoprofeno', 'Buprenorfina', 'Morfina', 'Oxycodona', 'Fentanilo', 'Nimesulida', 'Etoricoxib', 'Acetaminofén', 'Dipirona'],
    'Alergias': ['Loratadina', 'Cetirizina', 'Clorfenamina', 'Desloratadina', 'Fexofenadina', 'Levocetirizina', 'Difenhidramina', 'Epinastina', 'Ketotifeno', 'Mometasona', 'Fluticasona', 'Budesonida', 'Rupatadina', 'Ebastina', 'Bilastina', 'Hidroxicina', 'Clemastina', 'Azelastina', 'Olopatadina', 'Emedastina'],
    'Tos y Gripe': ['Ambroxol', 'Dextrometorfano', 'Guaifenesina', 'Bromhexina', 'Benzonatato', 'Levodropropizina', 'Oxolamina', 'Clopiperastina', 'Hedera Helix', 'Salbutamol', 'Fenilefrina', 'Pseudoefedrina', 'Oximetazolina', 'Nafazolina', 'Xilometazolina', 'Terbutalina', 'Formoterol', 'Salmeterol', 'Ipratropio', 'Tiotropio', 'Montelukast', 'Zafirlukast'],
    'Infecciones Bacterianas': ['Amoxicilina', 'Ampicilina', 'Ciprofloxacino', 'Azitromicina', 'Cefalexina', 'Ceftriaxona', 'Claritromicina', 'Levofloxacino', 'Clindamicina', 'Eritromicina', 'Doxiciclina', 'Tetraciclina', 'Gentamicina', 'Amikacina', 'Nitrofurantoína', 'Trimetoprima', 'Sulfametoxazol', 'Cefotaxima', 'Cefuroxima', 'Cefaclor', 'Dicloxacilina', 'Penicilina', 'Meropenem', 'Imipenem'],
    'Infecciones Virales': ['Aciclovir', 'Valaciclovir', 'Oseltamivir', 'Zanamivir', 'Amantadina', 'Rimantadina', 'Ribavirina', 'Ganciclovir', 'Famciclovir', 'Foscarnet', 'Entecavir', 'Tenofovir', 'Lamivudina', 'Efavirenz', 'Lopinavir', 'Ritonavir', 'Darunavir', 'Dolutegravir', 'Raltegravir', 'Maraviroc'],
    'Infecciones por Hongos': ['Fluconazol', 'Ketoconazol', 'Itraconazol', 'Clotrimazol', 'Miconazol', 'Terbinafina', 'Nistatina', 'Griseofulvina', 'Voriconazol', 'Posaconazol', 'Caspofungina', 'Micafungina', 'Anidulafungina', 'Amfotericina B', 'Tioconazol', 'Econazol', 'Sertaconazol', 'Bifonazol', 'Ciclopirox', 'Amorolfina'],
    'Problemas Estomacales': ['Omeprazol', 'Pantoprazol', 'Esomeprazol', 'Lansoprazol', 'Rabeprazol', 'Ranitidina', 'Famotidina', 'Subsalicilato de bismuto', 'Magaldrato', 'Hidróxido de aluminio', 'Hidróxido de magnesio', 'Simeticona', 'Metoclopramida', 'Ondansetrón', 'Domperidona', 'Cisaprida', 'Trimebutina', 'Pinaverio', 'Mebeverina', 'Loperamida', 'Racecadotrilo', 'Diosmectita', 'Probióticos', 'Senósidos', 'Bisacodilo', 'Lactulosa', 'Plantago psyllium', 'Polietilenglicol', 'Butilhioscina', 'Pargeverina'],
    'Hipertensión y Corazón': ['Losartán', 'Telmisartán', 'Valsartán', 'Candesartán', 'Irbesartán', 'Enalapril', 'Captopril', 'Lisinopril', 'Ramipril', 'Amlodipino', 'Nifedipino', 'Felodipino', 'Diltiazem', 'Verapamilo', 'Atenolol', 'Metoprolol', 'Propranolol', 'Bisoprolol', 'Carvedilol', 'Nebivolol', 'Furosemida', 'Hidroclorotiazida', 'Espironolactona', 'Clortalidona', 'Indapamida', 'Atorvastatina', 'Simvastatina', 'Pravastatina', 'Rosuvastatina', 'Bezafibrato', 'Fenofibrato', 'Aspirina Protect', 'Clopidogrel', 'Prasugrel', 'Ticagrelor', 'Warfarina', 'Acenocumarol', 'Rivaroxabán', 'Apixabán', 'Dabigatrán'],
    'Diabetes': ['Metformina', 'Glibenclamida', 'Glimepirida', 'Gliclazida', 'Pioglitazona', 'Rosiglitazona', 'Sitagliptina', 'Vildagliptina', 'Saxagliptina', 'Linagliptina', 'Exenatida', 'Liraglutida', 'Dulaglutida', 'Semaglutida', 'Dapagliflozina', 'Empagliflozina', 'Canagliflozina', 'Insulina Rápida', 'Insulina NPH', 'Insulina Glargina', 'Insulina Detemir', 'Insulina Degludec', 'Acarbosa', 'Miglitol'],
    'Ansiedad y Depresión': ['Fluoxetina', 'Sertralina', 'Paroxetina', 'Citalopram', 'Escitalopram', 'Venlafaxina', 'Desvenlafaxina', 'Duloxetina', 'Mirtazapina', 'Bupropión', 'Amitriptilina', 'Imipramina', 'Clomipramina', 'Diazepam', 'Clonazepam', 'Alprazolam', 'Lorazepam', 'Bromazepam', 'Midazolam', 'Zolpidem', 'Zopiclona', 'Pregabalina', 'Gabapentina', 'Valproato', 'Carbamazepina', 'Oxcarbazepina', 'Levetiracetam', 'Topiramato', 'Lamotrigina', 'Fenitoína'],
    'Cuidado Ocular': ['Hipromelosa', 'Hialuronato de sodio', 'Nafazolina ocular', 'Timolol', 'Bimatoprost', 'Latanoprost', 'Travoprost', 'Dorzolamida', 'Brimonidina', 'Prednisolona ocular', 'Dexametasona ocular', 'Diclofenaco ocular', 'Ketorolaco ocular', 'Ciprofloxacino ocular', 'Tobramicina ocular', 'Eritromicina ocular', 'Cloranfenicol ocular', 'Tetracaína', 'Proparacaína', 'Pilocarpina'],
    'Cuidado de la Piel': ['Hidrocortisona tópica', 'Betametasona', 'Clobetasol', 'Desonida', 'Mupirocina', 'Ácido fusídico', 'Retinol', 'Tretinoína', 'Adapaleno', 'Peróxido de benzoilo', 'Ácido salicílico', 'Clindamicina tópica', 'Eritromicina tópica', 'Calamina', 'Óxido de zinc', 'Pantenol', 'Urea', 'Ácido hialurónico', 'Colágeno', 'Minoxidil', 'Finasterida', 'Ketoconazol champú', 'Alquitrán de hulla'],
    'Vitaminas y Suplementos': ['Vitamina C', 'Vitamina D3', 'Vitamina E', 'Vitamina A', 'Vitamina B12', 'Vitamina B6', 'Complejo B', 'Ácido Fólico', 'Hierro', 'Calcio', 'Magnesio', 'Zinc', 'Potasio', 'Omega 3', 'Glucosamina', 'Condroitina', 'Colágeno Hidrolizado', 'Biotina', 'Melatonina', 'Ginseng', 'Ginkgo Biloba', 'Espirulina', 'Maca', 'Cúrcuma'],
    'Antiparasitarios': ['Albendazol', 'Mebendazol', 'Quinfamida', 'Secnidazol', 'Nitazoxanida', 'Metronidazol', 'Tinidazol', 'Ivermectina', 'Prazicuantel', 'Pirantel'],
    'Tiroides y Hormonas': ['Levotiroxina', 'Liotironina', 'Tiamazol', 'Propiltiouracilo', 'Estradiol', 'Progesterona', 'Testosterona', 'Dexametasona', 'Prednisona', 'Metilprednisolona', 'Deflazacort', 'Fludrocortisona']
}

medicamentos_totales = []
for sintoma, meds in sintomas_medicamentos.items():
    for med in meds:
        medicamentos_totales.append((med, sintoma))

print(f"Total medicamentos generados: {len(medicamentos_totales)}")

code = f"""
def insertar_muchos_medicamentos():
    medicamentos = {medicamentos_totales}

    try:
        conexion = conectar()
        cursor = conexion.cursor()

        for med, sintoma in medicamentos:
            import random
            stock = random.randint(15, 100)
            compra = random.randint(10, 500)
            venta = compra + random.randint(10, 200)
            
            cursor.execute('''
                INSERT INTO medicamentos (nombre, stock, precio_compra, precio_venta, fecha_caducidad, sintoma)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (med, stock, compra, venta, "2026-12-31", sintoma))

        conexion.commit()
        conexion.close()

        print("Medicamentos insertados correctamente")

    except Exception as e:
        print("Error:", e)
"""

with open('C:\\\\Users\\\\52332\\\\Desktop\\\\farmacia_app\\\\db.py', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('def insertar_muchos_medicamentos():')
if start_idx != -1:
    end_idx = content.find('def conectar():', start_idx)
    new_content = content[:start_idx] + code.strip() + '\\n\\n' + content[end_idx:]
    with open('C:\\\\Users\\\\52332\\\\Desktop\\\\farmacia_app\\\\db.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Actualizado db.py exitosamente!")
else:
    print("No se encontró la función insertar_muchos_medicamentos")
