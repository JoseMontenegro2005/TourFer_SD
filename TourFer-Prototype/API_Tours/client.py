import logging
from zeep import Client
from zeep.helpers import serialize_object

WSDL_URL = 'http://127.0.0.1:5003/?wsdl'

logging.basicConfig(level=logging.INFO)
logging.getLogger('zeep').setLevel(logging.WARNING) 

def run_soap_demo():
    print(f"Conectando a {WSDL_URL}...")
    client = Client(WSDL_URL)
    print(f"-> Conectado exitosamente al WSDL.")

    try:
                
        print("\n--- 1. Llamando a listAllTours() ---")
        all_tours = client.service.listAllTours()
        
        print(f"=> ÉXITO: Se recibieron {len(all_tours)} tours.")
        
        if all_tours and len(all_tours) > 0:
            print(f"Datos del Primer Tour (ID: {all_tours[0].id}): {all_tours[0].nombre}")

            tour_id_to_find = all_tours[0].id
            print(f"\n--- 2. Llamando a getTourById({tour_id_to_find}) ---")
            specific_tour = client.service.getTourById(tour_id=tour_id_to_find)
            
            if specific_tour:
                print(f"=> ÉXITO: Tour encontrado (Precio: ${specific_tour.precio:,.0f} COP)")
            else:
                print(f"=> FALLO: Tour ID {tour_id_to_find} no fue encontrado.")
        
        else:
            print("=> ADVERTENCIA: La base de datos no devolvió tours.")

    except Exception as e:
        print(f"\n=> ERROR CRÍTICO AL CONSUMIR EL SERVICIO:")
        print(f"Asegúrese que el servidor SOAP (puerto 5003) y MySQL están activos.")
        print(f"Detalle del error: {e}")

if __name__ == '__main__':
    run_soap_demo()
