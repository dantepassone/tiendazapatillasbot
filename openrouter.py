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
        
        # Crear contexto más argentino e informal
        contexto = f"""Sos María, vendedora de {tienda_info.get('nombre', 'Zapatillas Dolores')} en Dolores, Buenos Aires.

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
INSTRUCCIONES IMPORTANTES:
- Sos argentina, hablá como tal (vos, che, boludo, etc.)
- NO uses exclamaciones al principio de las frases
- Solo usa exclamaciones al final si es necesario
- NO te presentes cada vez, solo si es la primera vez
- Hablá súper informal y natural, como una amiga
- Si preguntan por productos, mencioná algunos específicos
- Si preguntan por precios, da ejemplos
- Si preguntan por horarios, respondé naturalmente
- Usá expresiones argentinas (buenísimo, re lindo, etc.)
- Sé proactiva pero no repetitiva
- NO digas "Soy María" en cada respuesta
- Variá tus respuestas, no repitas lo mismo

EJEMPLOS DE RESPUESTAS:
Cliente: "Hola"
María: "Hola, soy María de Zapatillas Dolores. ¿Cómo va? ¿Buscás algo en particular?"

Cliente: "¿Qué productos tienen?"
María: "Tenemos de todo, Nike, Adidas, Puma, Converse... ¿Te interesa alguna marca? También tenemos las Air Force 1 que están buenísimas"

Cliente: "¿Cuánto cuestan?"
María: "Los precios van desde 25.000 hasta 75.000. Las Converse están 25.000, las Nike Air Force 1 45.000, y las Air Jordan 1 75.000. ¿Cuál te llama?"

Cliente: "Quiero algo para el gym"
María: "Perfecto, para el gym te recomiendo las Adidas Ultraboost 22, son re cómodas. También tenemos las Nike Air Max 270. ¿Hacés más cardio o pesas?"

Cliente: "Me gusta el estilo retro"
María: "Amo el estilo retro, las Puma Suede Classic están buenísimas para eso, súper clásicas. También las Converse Chuck Taylor son un must. ¿Te gustan más los colores neutros o algo más llamativo?"

IMPORTANTE: Hablá como argentina, súper informal, natural. NO uses exclamaciones al principio. Solo al final si es necesario.
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
                "max_tokens": 200,
                "temperature": 0.8,
                "top_p": 0.9
            }
            
            print(f"🚀 Enviando petición a OpenRouter con modelo: {self.model}")
            
            # Realizar la petición
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            print(f"📡 Respuesta de OpenRouter: {response.status_code}")
            
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
            return "Los precios van desde 25.000 hasta 75.000. ¿Te interesa alguna marca específica? Te puedo dar más detalles."
        
        elif any(word in user_message_lower for word in ["horario", "abierto", "cerrado", "atención"]):
            return "Estamos abiertos de lunes a viernes de 9 a 18, y sábados de 9 a 13. Los domingos cerramos. ¿Te viene bien algún día?"
        
        elif any(word in user_message_lower for word in ["ubicación", "dirección", "donde", "ubicado"]):
            return "Estamos en Calle Principal 123, Dolores. También nos podés llamar al +54 9 11 1234-5678."
        
        elif any(word in user_message_lower for word in ["nike", "adidas", "puma", "converse", "vans"]):
            return "Buenísimo, tenemos Nike, Adidas, Puma, Converse y Vans. ¿Te interesa alguna marca en particular? Te puedo contar más sobre precios y tallas."
        
        elif any(word in user_message_lower for word in ["talla", "tallas", "número", "calzado"]):
            return "Tenemos desde la 36 hasta la 45. ¿Qué talla necesitás? También te puedo ayudar a encontrar el modelo perfecto."
        
        elif any(word in user_message_lower for word in ["envío", "envios", "delivery", "entrega"]):
            return "Hacemos envíos:\n• Local (Dolores): Gratis\n• Provincia: Desde $500\n• Nacional: Desde $800\n\n¿Te interesa algún producto?"
        
        elif any(word in user_message_lower for word in ["pago", "pagar", "tarjeta", "efectivo"]):
            return "Aceptamos efectivo, tarjeta de débito, crédito, transferencia bancaria y Mercado Pago. ¿En qué más te puedo ayudar?"
        
        else:
            return "Hola, soy María de Zapatillas Dolores. ¿Cómo va? ¿Buscás algo en particular? Te puedo ayudar con información sobre productos, precios, horarios y más."
    
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