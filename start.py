#!/usr/bin/env python3
"""
Script de inicio rápido para el Bot WhatsApp Zapatillas Dolores
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Verifica que se cumplan los requisitos"""
    print("🔍 Verificando requisitos...")
    
    # Verificar Python
    if sys.version_info < (3, 7):
        print("❌ Se requiere Python 3.7 o superior")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} detectado")
    
    # Verificar archivo .env
    if not Path(".env").exists():
        print("⚠️  Archivo .env no encontrado")
        print("   Copiando env.example a .env...")
        try:
            subprocess.run(["cp", "env.example", ".env"], check=True)
            print("✅ Archivo .env creado")
            print("   ⚠️  IMPORTANTE: Edita .env con tus tokens reales antes de continuar")
        except:
            print("❌ Error creando archivo .env")
            return False
    
    # Verificar dependencias
    try:
        import flask
        import requests
        from dotenv import load_dotenv
        print("✅ Dependencias instaladas")
    except ImportError:
        print("❌ Dependencias faltantes")
        print("   Ejecuta: pip install -r requirements.txt")
        return False
    
    return True

def install_dependencies():
    """Instala las dependencias"""
    print("📦 Instalando dependencias...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error instalando dependencias")
        return False

def run_tests():
    """Ejecuta las pruebas"""
    print("🧪 Ejecutando pruebas...")
    try:
        result = subprocess.run([sys.executable, "test_bot.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Todas las pruebas pasaron")
            return True
        else:
            print("❌ Algunas pruebas fallaron")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error ejecutando pruebas: {e}")
        return False

def start_server():
    """Inicia el servidor"""
    print("🚀 Iniciando servidor...")
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido")
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")

def main():
    """Función principal"""
    print("🤖 Bot WhatsApp Zapatillas Dolores - Inicio Rápido")
    print("=" * 50)
    
    # Verificar requisitos
    if not check_requirements():
        print("\n❌ Requisitos no cumplidos. Revisa los errores arriba.")
        return False
    
    # Preguntar si instalar dependencias
    if not Path("venv").exists():
        response = input("\n¿Instalar dependencias? (y/n): ").lower()
        if response == 'y':
            if not install_dependencies():
                return False
    
    # Preguntar si ejecutar pruebas
    response = input("\n¿Ejecutar pruebas? (y/n): ").lower()
    if response == 'y':
        if not run_tests():
            print("\n⚠️  Algunas pruebas fallaron, pero puedes continuar")
    
    # Preguntar si iniciar servidor
    response = input("\n¿Iniciar servidor? (y/n): ").lower()
    if response == 'y':
        start_server()
    
    print("\n🎉 ¡Configuración completada!")
    print("\n📚 Próximos pasos:")
    print("1. Edita .env con tus tokens reales")
    print("2. Ejecuta: python app.py")
    print("3. Configura el webhook de WhatsApp")
    print("4. ¡Disfruta tu bot!")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Operación cancelada")
        sys.exit(1)
