#!/usr/bin/env python3
"""
Script de prueba para el bot de WhatsApp
"""

import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_database():
    """Prueba la conexión a la base de datos"""
    print("🔍 Probando base de datos...")
    try:
        from database import Database
        db = Database()
        
        # Probar obtener información de la tienda
        tienda_info = db.get_tienda_info()
        print(f"✅ Tienda cargada: {tienda_info.get('nombre', 'N/A')}")
        
        # Probar obtener productos
        productos = db.get_productos()
        print(f"✅ Productos cargados: {len(productos)} productos")
        
        # Probar búsqueda
        busqueda = db.buscar_productos("nike")
        print(f"✅ Búsqueda funcionando: {len(busqueda)} resultados para 'nike'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en base de datos: {str(e)}")
        return False

def test_openrouter():
    """Prueba la conexión con OpenRouter"""
    print("\n🤖 Probando OpenRouter AI...")
    try:
        from openrouter import OpenRouterAI
        ai = OpenRouterAI()
        
        # Probar generación de respuesta
        respuesta = ai.generate_response("Hola, ¿qué productos tienen?")
        print(f"✅ IA funcionando: {respuesta[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en OpenRouter: {str(e)}")
        return False

def test_whatsapp():
    """Prueba la configuración de WhatsApp"""
    print("\n📱 Probando configuración de WhatsApp...")
    try:
        from whatsapp import WhatsAppAPI
        whatsapp = WhatsAppAPI()
        
        # Verificar variables de entorno
        required_vars = [
            "WHATSAPP_TOKEN",
            "WHATSAPP_PHONE_NUMBER_ID",
            "WHATSAPP_VERIFY_TOKEN"
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            print(f"⚠️  Variables faltantes: {missing_vars}")
            print("   (Esto es normal si no has configurado el .env aún)")
            return False
        else:
            print("✅ Configuración de WhatsApp completa")
            return True
            
    except Exception as e:
        print(f"❌ Error en WhatsApp: {str(e)}")
        return False

def test_flask_app():
    """Prueba la aplicación Flask"""
    print("\n🌐 Probando aplicación Flask...")
    try:
        from app import app
        
        with app.test_client() as client:
            # Probar endpoint de inicio
            response = client.get("/")
            if response.status_code == 200:
                print("✅ Endpoint de inicio funcionando")
            else:
                print(f"❌ Error en endpoint de inicio: {response.status_code}")
                return False
            
            # Probar endpoint de productos
            response = client.get("/products")
            if response.status_code == 200:
                print("✅ Endpoint de productos funcionando")
            else:
                print(f"❌ Error en endpoint de productos: {response.status_code}")
                return False
            
            # Probar endpoint de tienda
            response = client.get("/store")
            if response.status_code == 200:
                print("✅ Endpoint de tienda funcionando")
            else:
                print(f"❌ Error en endpoint de tienda: {response.status_code}")
                return False
            
            return True
            
    except Exception as e:
        print(f"❌ Error en Flask: {str(e)}")
        return False

def main():
    """Función principal de prueba"""
    print("🚀 Iniciando pruebas del Bot WhatsApp Zapatillas Dolores...\n")
    
    tests = [
        ("Base de datos", test_database),
        ("OpenRouter AI", test_openrouter),
        ("WhatsApp", test_whatsapp),
        ("Flask App", test_flask_app)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error inesperado en {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Mostrar resumen
    print("\n" + "="*50)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print("="*50)
    print(f"Pruebas pasadas: {passed}/{total}")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! El bot está listo para usar.")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
