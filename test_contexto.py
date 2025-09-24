#!/usr/bin/env python3
"""
Script para probar el contexto de conversación del bot
"""

import os
from dotenv import load_dotenv
from database import Database
from openrouter import OpenRouterAI

def test_contexto():
    """Prueba el contexto de conversación"""
    print("🧪 Probando contexto de conversación...")
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Inicializar componentes
    db = Database()
    ai = OpenRouterAI()
    
    # Simular número de teléfono
    phone_number = "5491123456789"
    
    print(f"\n📱 Simulando conversación con: {phone_number}")
    
    # Primera conversación (sin historial)
    print("\n1️⃣ PRIMERA CONVERSACIÓN (sin historial):")
    mensaje1 = "Hola"
    print(f"Usuario: {mensaje1}")
    
    # Simular guardado de conversación
    respuesta1 = ai.generate_response(mensaje1, phone_number)
    print(f"María: {respuesta1}")
    
    # Segunda conversación (con historial)
    print("\n2️⃣ SEGUNDA CONVERSACIÓN (con historial):")
    mensaje2 = "¿Qué productos tienen?"
    print(f"Usuario: {mensaje2}")
    
    respuesta2 = ai.generate_response(mensaje2, phone_number)
    print(f"María: {respuesta2}")
    
    # Tercera conversación (más historial)
    print("\n3️⃣ TERCERA CONVERSACIÓN (más historial):")
    mensaje3 = "¿Cuánto cuestan las Nike?"
    print(f"Usuario: {mensaje3}")
    
    respuesta3 = ai.generate_response(mensaje3, phone_number)
    print(f"María: {respuesta3}")
    
    # Verificar historial en base de datos
    print("\n📚 HISTORIAL GUARDADO:")
    historial = db.get_conversation_history(phone_number, 5)
    for i, conv in enumerate(historial, 1):
        print(f"{i}. Usuario: {conv['mensaje']}")
        print(f"   María: {conv['respuesta']}")
        print(f"   Timestamp: {conv['timestamp']}")
        print()
    
    print("✅ Prueba de contexto completada!")

if __name__ == "__main__":
    test_contexto()
