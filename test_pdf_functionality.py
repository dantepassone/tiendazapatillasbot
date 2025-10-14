#!/usr/bin/env python3
"""
Script para probar la funcionalidad de envío de PDF
"""

import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_pdf_functionality():
    """Prueba la funcionalidad de envío de PDF"""
    try:
        from whatsapp import WhatsAppAPI
        
        print("🧪 Iniciando prueba de funcionalidad PDF...")
        
        # Inicializar WhatsApp API
        whatsapp = WhatsAppAPI()
        
        # Verificar configuración
        print(f"📱 WhatsApp configurado: {bool(whatsapp.access_token)}")
        print(f"📱 Phone Number ID: {whatsapp.phone_number_id}")
        
        # Probar detección de palabras clave
        test_messages = [
            "lista de precios",
            "precios",
            "catálogo",
            "pdf",
            "cuanto cuesta"
        ]
        
        print("\n🔍 Probando detección de palabras clave:")
        for message in test_messages:
            message_lower = message.lower()
            price_list_keywords = [
                "lista de precios", "lista precios", "precios", "catálogo", "catalogo",
                "precio lista", "lista", "pdf", "archivo", "documento", "precio",
                "cuanto cuesta", "cuánto cuesta", "precio", "valores", "tarifa"
            ]
            
            detected = any(keyword in message_lower for keyword in price_list_keywords)
            print(f"  '{message}' -> {'✅ Detectado' if detected else '❌ No detectado'}")
        
        # Probar envío de PDF (solo si está configurado)
        if whatsapp.access_token:
            print("\n📋 Probando envío de PDF...")
            test_phone = "5492245400209"  # Número de prueba
            success = whatsapp.send_price_list_pdf(test_phone)
            print(f"📋 Resultado: {'✅ Éxito' if success else '❌ Error'}")
        else:
            print("\n❌ WhatsApp no está configurado, saltando prueba de envío")
        
        print("\n✅ Prueba completada")
        
    except Exception as e:
        print(f"❌ Error en la prueba: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de funcionalidad PDF...")
    success = test_pdf_functionality()
    sys.exit(0 if success else 1)
