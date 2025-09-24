#!/usr/bin/env python3
"""
Script de diagnóstico para la IA
"""

import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_openrouter_connection():
    """Prueba la conexión con OpenRouter"""
    print("🔍 Diagnosticando conexión con OpenRouter...")
    
    # Verificar API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY no está configurada")
        return False
    
    print(f"✅ API Key configurada: {api_key[:10]}...")
    
    # Configurar headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://zapatillasdolores.com",
        "X-Title": "Bot WhatsApp Zapatillas Dolores"
    }
    
    # Payload simple
    payload = {
        "model": "meta-llama/llama-3.2-3b-instruct:free",
        "messages": [
            {
                "role": "user",
                "content": "Hola, responde solo 'Hola'"
            }
        ],
        "max_tokens": 10,
        "temperature": 0.7
    }
    
    try:
        print("📡 Enviando petición a OpenRouter...")
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            ai_response = data["choices"][0]["message"]["content"].strip()
            print(f"✅ IA funcionando: {ai_response}")
            return True
        else:
            print(f"❌ Error en OpenRouter: {response.status_code}")
            print(f"Error details: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        return False

def test_bot_ai():
    """Prueba la IA del bot"""
    print("\n🤖 Probando IA del bot...")
    
    try:
        from openrouter import OpenRouterAI
        ai = OpenRouterAI()
        
        # Probar respuesta
        test_message = "Hola, ¿qué productos tienen?"
        response = ai.generate_response(test_message, "test_phone")
        
        print(f"📝 Mensaje de prueba: {test_message}")
        print(f"🤖 Respuesta del bot: {response}")
        
        # Verificar si es respuesta de respaldo
        is_fallback = "¡Hola! Bienvenido a Zapatillas Dolores" in response
        print(f"🔄 Es respuesta de respaldo: {is_fallback}")
        
        return not is_fallback
        
    except Exception as e:
        print(f"❌ Error probando bot: {str(e)}")
        return False

def main():
    """Función principal de diagnóstico"""
    print("🚀 Diagnóstico del Bot WhatsApp Zapatillas Dolores")
    print("=" * 50)
    
    # Probar conexión directa con OpenRouter
    openrouter_ok = test_openrouter_connection()
    
    # Probar IA del bot
    bot_ok = test_bot_ai()
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN DEL DIAGNÓSTICO")
    print("=" * 50)
    
    print(f"OpenRouter API: {'✅ OK' if openrouter_ok else '❌ ERROR'}")
    print(f"Bot IA: {'✅ OK' if bot_ok else '❌ ERROR'}")
    
    if not openrouter_ok:
        print("\n🔧 SOLUCIÓN:")
        print("1. Verifica que OPENROUTER_API_KEY esté configurada correctamente")
        print("2. Verifica que tengas créditos en OpenRouter")
        print("3. Verifica que el modelo esté disponible")
    
    if not bot_ok and openrouter_ok:
        print("\n🔧 SOLUCIÓN:")
        print("1. Hay un problema en el código del bot")
        print("2. Revisa los logs de Render")
    
    return openrouter_ok and bot_ok

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
