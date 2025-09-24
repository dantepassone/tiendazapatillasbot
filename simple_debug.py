#!/usr/bin/env python3
"""
Diagnóstico simple para la IA
"""

import os

def check_environment():
    """Verifica las variables de entorno"""
    print("🔍 Verificando variables de entorno...")
    
    # Verificar OPENROUTER_API_KEY
    api_key = os.getenv("OPENROUTER_API_KEY")
    if api_key:
        print(f"✅ OPENROUTER_API_KEY: {api_key[:10]}...")
    else:
        print("❌ OPENROUTER_API_KEY: NO CONFIGURADA")
    
    # Verificar otras variables
    whatsapp_token = os.getenv("WHATSAPP_TOKEN")
    if whatsapp_token:
        print(f"✅ WHATSAPP_TOKEN: {whatsapp_token[:10]}...")
    else:
        print("❌ WHATSAPP_TOKEN: NO CONFIGURADA")
    
    phone_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    if phone_id:
        print(f"✅ WHATSAPP_PHONE_NUMBER_ID: {phone_id}")
    else:
        print("❌ WHATSAPP_PHONE_NUMBER_ID: NO CONFIGURADA")
    
    verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN")
    if verify_token:
        print(f"✅ WHATSAPP_VERIFY_TOKEN: {verify_token[:10]}...")
    else:
        print("❌ WHATSAPP_VERIFY_TOKEN: NO CONFIGURADA")
    
    return bool(api_key)

def test_openrouter_simple():
    """Prueba simple de OpenRouter"""
    print("\n🤖 Probando OpenRouter...")
    
    try:
        import requests
        
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("❌ No hay API key configurada")
            return False
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "meta-llama/llama-3.2-3b-instruct:free",
            "messages": [{"role": "user", "content": "Hola"}],
            "max_tokens": 10
        }
        
        print("📡 Enviando petición...")
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )
        
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            ai_response = data["choices"][0]["message"]["content"].strip()
            print(f"✅ IA funcionando: {ai_response}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Función principal"""
    print("🚀 Diagnóstico Simple del Bot")
    print("=" * 40)
    
    # Verificar variables de entorno
    env_ok = check_environment()
    
    # Probar OpenRouter
    ai_ok = test_openrouter_simple()
    
    print("\n" + "=" * 40)
    print("📊 RESUMEN")
    print("=" * 40)
    print(f"Variables de entorno: {'✅ OK' if env_ok else '❌ ERROR'}")
    print(f"OpenRouter IA: {'✅ OK' if ai_ok else '❌ ERROR'}")
    
    if not env_ok:
        print("\n🔧 SOLUCIÓN:")
        print("Configura las variables de entorno en Render")
    
    if not ai_ok and env_ok:
        print("\n🔧 SOLUCIÓN:")
        print("1. Verifica que tu API key de OpenRouter sea válida")
        print("2. Verifica que tengas créditos en OpenRouter")
        print("3. Verifica que el modelo esté disponible")
    
    return env_ok and ai_ok

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
