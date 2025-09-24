import requests
import json
import os
from typing import Dict, List, Any
from database import Database

class OpenRouterAI:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        # Usar modelo específico como respaldo
        self.model = "meta-llama/llama-3.2-3b-instruct:free"
        self.base_url = "https://openrouter.ai/api/v1"
        self.db = Database()
        
    def get_context_prompt(self) -> str:
        """Genera el prompt de contexto con información de la tienda"""
        tienda_info = self.db.get_tienda_info()
        productos = self.db.get_productos()
        
        # Crear contexto más simple y directo
        contexto = f"""Eres María, vendedora de {tienda_info.get('nombre', 'Zapatillas Dolores')} en Dolores, Buenos Aires.

INFORMACIÓN DE LA TIENDA:
- Nombre: {tienda_info.get('nombre', 'Zapatillas Dolores')}
- Ubicación: {tienda_info.get('ubicacion', 'Dolores, Buenos Aires, Argentina')}
- Teléfono: {tienda_info.get('telefono', '+54 9 11 1234-5678')}

HORARIOS:
"""
        
        if 'horarios' in tienda_info:
            for dia, horario in tienda_info['horarios'].items():
                contexto += f"- {dia.replace('_', ' ').title()}: {horario}\n"
        
        contexto += f"""
PRODUCTOS DISPONIBLES:
"""
        
        for producto in productos[:5]:  # Solo los primeros 5 productos
            contexto += f"- {producto['marca']} {producto['nombre']} - ${producto['precio']:,}\n"
        
        contexto += """
INSTRUCCIONES:
- Responde como María, una vendedora amigable
- Habla de forma natural y conversacional
- Si preguntan por productos, menciona algunos específicos
- Si preguntan por precios, da ejemplos
- Si preguntan por horarios, responde naturalmente
- Usa expresiones argentinas
- Sé proactiva y entusiasta
"""
        
        return contexto
    
    def generate_response(self, user_message: str, phone_number: str = None) -> str:
        """Genera una respuesta usando OpenRouter AI"""
        try:
            # Verificar que la API key esté configurada
            if not self.api_key:
                print("Error: OPENROUTER_API_KEY no está configurada")
                return self.get_fallback_response(user_message)
            
            print(f"🔑 API Key configurada: {self.api_key[:10]}...")
            
            # Obtener contexto de la tienda
            context_prompt = self.get_context_prompt()
            print(f"📝 Contexto generado: {len(context_prompt)} caracteres")
            
            # Preparar el mensaje completo
            full_prompt = f"{context_prompt}\n\nCliente pregunta: {user_message}\n\nRespuesta:"
            print(f"📤 Prompt completo: {len(full_prompt)} caracteres")
            
            # Configurar headers
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://zapatillasdolores.com",
                "X-Title": "Bot WhatsApp Zapatillas Dolores"
            }
            
            # Configurar payload con modelo específico
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": full_prompt
                    }
                ],
                "max_tokens": 300,
                "temperature": 0.7,
                "top_p": 0.9
            }
            
            print(f"🚀 Enviando petición a OpenRouter con modelo: {self.model}")
            print(f"📊 Payload: {json.dumps(payload, indent=2)}")
            
            # Realizar la petición
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            print(f"📡 Respuesta de OpenRouter: {response.status_code}")
            print(f"📄 Contenido de respuesta: {response.text[:500]}...")
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data["choices"][0]["message"]["content"].strip()
                print(f"✅ IA respuesta: {ai_response}")
                
                # Guardar conversación en la base de datos
                if phone_number:
                    self.db.save_conversation(phone_number, user_message, ai_response)
                
                return ai_response
            else:
                print(f"❌ Error en OpenRouter API: {response.status_code}")
                print(f"❌ Respuesta completa: {response.text}")
                return self.get_fallback_response(user_message)
                
        except Exception as e:
            print(f"❌ Error generando respuesta: {str(e)}")
            return self.get_fallback_response(user_message)
    
    def get_fallback_response(self, user_message: str) -> str:
        """Respuesta de respaldo cuando falla la IA"""
        user_message_lower = user_message.lower()
        
        # Respuestas básicas basadas en palabras clave
        if any(word in user_message_lower for word in ["precio", "cuesta", "vale", "costo"]):
            return "¡Hola! Los precios de nuestras zapatillas van desde $25.000 hasta $75.000. ¿Te interesa alguna marca o modelo específico? Puedo darte más detalles sobre precios y disponibilidad."
        
        elif any(word in user_message_lower for word in ["horario", "abierto", "cerrado", "atención"]):
            return "Nuestros horarios de atención son:\n• Lunes a Viernes: 9:00 - 18:00\n• Sábados: 9:00 - 13:00\n• Domingos: Cerrado\n\n¡Te esperamos en Dolores, Buenos Aires!"
        
        elif any(word in user_message_lower for word in ["ubicación", "dirección", "donde", "ubicado"]):
            return "Estamos ubicados en Calle Principal 123, Dolores, Buenos Aires. También puedes contactarnos al +54 9 11 1234-5678 o por email a info@zapatillasdolores.com"
        
        elif any(word in user_message_lower for word in ["nike", "adidas", "puma", "converse", "vans"]):
            return "¡Excelente elección! Tenemos varias marcas disponibles como Nike, Adidas, Puma, Converse y Vans. ¿Te interesa alguna marca específica o modelo en particular? Puedo darte más información sobre precios y tallas disponibles."
        
        elif any(word in user_message_lower for word in ["talla", "tallas", "número", "calzado"]):
            return "Tenemos tallas desde 36 hasta 45. ¿Qué talla necesitas? También puedo ayudarte a encontrar el modelo perfecto según tu preferencia de marca y estilo."
        
        elif any(word in user_message_lower for word in ["envío", "envios", "delivery", "entrega"]):
            return "Realizamos envíos:\n• Local (Dolores): Gratis\n• Provincia: Desde $500\n• Nacional: Desde $800\n\n¿Te interesa algún producto en particular?"
        
        elif any(word in user_message_lower for word in ["pago", "pagar", "tarjeta", "efectivo"]):
            return "Aceptamos:\n• Efectivo\n• Tarjeta de débito\n• Tarjeta de crédito\n• Transferencia bancaria\n• Mercado Pago\n\n¿En qué más puedo ayudarte?"
        
        else:
            return "¡Hola! Bienvenido a Zapatillas Dolores. Soy tu asistente virtual y estoy aquí para ayudarte con información sobre nuestros productos, precios, horarios y más. ¿En qué puedo asistirte hoy?"
    
    def search_products(self, query: str) -> List[Dict[str, Any]]:
        """Busca productos basado en la consulta del usuario"""
        return self.db.buscar_productos(query)
    
    def get_product_info(self, product_id: int) -> Dict[str, Any]:
        """Obtiene información detallada de un producto"""
        return self.db.get_producto_por_id(product_id)
    
    def check_stock(self, product_id: int, size: str) -> bool:
        """Verifica el stock de un producto en una talla específica"""
        return self.db.verificar_stock(product_id, size)
    
    def get_available_sizes(self, product_id: int) -> Dict[str, int]:
        """Obtiene las tallas disponibles de un producto"""
        return self.db.get_stock_disponible(product_id)