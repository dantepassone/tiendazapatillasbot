import requests
import json
import os
from typing import Dict, List, Any
from database import Database

class OpenRouterAI:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-chat-v3-0324:free")
        self.base_url = "https://openrouter.ai/api/v1"
        self.db = Database()
        
    def get_context_prompt(self) -> str:
        """Genera el prompt de contexto con información de la tienda"""
        tienda_info = self.db.get_tienda_info()
        productos = self.db.get_productos()
        
        # Crear contexto de la tienda
        contexto = f"""
        Eres un asistente virtual de {tienda_info.get('nombre', 'Zapatillas Dolores')}, 
        una tienda de zapatillas ubicada en {tienda_info.get('ubicacion', 'Dolores, Buenos Aires, Argentina')}.
        
        INFORMACIÓN DE LA TIENDA:
        - Nombre: {tienda_info.get('nombre', 'Zapatillas Dolores')}
        - Ubicación: {tienda_info.get('ubicacion', 'Dolores, Buenos Aires, Argentina')}
        - Dirección: {tienda_info.get('direccion', 'Calle Principal 123, Dolores, Buenos Aires')}
        - Teléfono: {tienda_info.get('telefono', '+54 9 11 1234-5678')}
        - Email: {tienda_info.get('email', 'info@zapatillasdolores.com')}
        - Descripción: {tienda_info.get('descripcion', 'Tienda especializada en zapatillas deportivas y casuales')}
        
        HORARIOS DE ATENCIÓN:
        """
        
        if 'horarios' in tienda_info:
            for dia, horario in tienda_info['horarios'].items():
                contexto += f"- {dia.replace('_', ' ').title()}: {horario}\n"
        
        contexto += f"""
        
        MÉTODOS DE PAGO:
        """
        if 'metodos_pago' in tienda_info:
            for metodo in tienda_info['metodos_pago']:
                contexto += f"- {metodo}\n"
        
        contexto += f"""
        
        ENVÍOS:
        """
        if 'envios' in tienda_info:
            for tipo, precio in tienda_info['envios'].items():
                contexto += f"- {tipo.title()}: {precio}\n"
        
        contexto += f"""
        
        CATÁLOGO DE PRODUCTOS DISPONIBLES:
        """
        
        for producto in productos[:10]:  # Mostrar solo los primeros 10 productos
            contexto += f"""
        - {producto['marca']} {producto['nombre']}
          Categoría: {producto['categoria']}
          Precio: ${producto['precio']:,}
          Tallas disponibles: {', '.join(producto['tallas'])}
          Colores: {', '.join(producto['colores'])}
          Stock: {sum(producto['stock'].values())} unidades
          Descripción: {producto['descripcion']}
        """
        
        contexto += """
        
        INSTRUCCIONES IMPORTANTES:
        1. Siempre responde en español argentino, de manera amigable y profesional
        2. Si preguntan por un producto específico, busca en el catálogo y proporciona información detallada
        3. Si preguntan por precios, siempre menciona el precio en pesos argentinos
        4. Si preguntan por stock, verifica la disponibilidad de tallas
        5. Si no encuentras un producto específico, sugiere alternativas similares
        6. Siempre menciona que pueden visitar la tienda o contactar por teléfono para más información
        7. Si preguntan por horarios, proporciona la información de horarios de atención
        8. Si preguntan por métodos de pago, lista los disponibles
        9. Si preguntan por envíos, proporciona la información de costos
        10. Mantén un tono amigable y profesional, como un vendedor experto en zapatillas
        
        Responde de manera concisa pero completa a las consultas de los clientes.
        """
        
        return contexto
    
    def generate_response(self, user_message: str, phone_number: str = None) -> str:
        """Genera una respuesta usando OpenRouter AI"""
        try:
            # Verificar que la API key esté configurada
            if not self.api_key:
                print("Error: OPENROUTER_API_KEY no está configurada")
                return self.get_fallback_response(user_message)
            
            # Obtener contexto de la tienda
            context_prompt = self.get_context_prompt()
            
            # Preparar el mensaje completo
            full_prompt = f"{context_prompt}\n\nCliente pregunta: {user_message}\n\nRespuesta:"
            
            # Configurar headers
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://zapatillasdolores.com",
                "X-Title": "Bot WhatsApp Zapatillas Dolores"
            }
            
            # Configurar payload
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": full_prompt
                    }
                ],
                "max_tokens": 500,
                "temperature": 0.7,
                "top_p": 0.9,
                "frequency_penalty": 0.1,
                "presence_penalty": 0.1
            }
            
            print(f"Enviando petición a OpenRouter con modelo: {self.model}")
            
            # Realizar la petición
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            print(f"Respuesta de OpenRouter: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data["choices"][0]["message"]["content"].strip()
                
                # Guardar conversación en la base de datos
                if phone_number:
                    self.db.save_conversation(phone_number, user_message, ai_response)
                
                return ai_response
            else:
                print(f"Error en OpenRouter API: {response.status_code}")
                print(f"Respuesta: {response.text}")
                return self.get_fallback_response(user_message)
                
        except Exception as e:
            print(f"Error generando respuesta: {str(e)}")
            return self.get_fallback_response(user_message)
    
    def get_fallback_response(self, user_message: str) -> str:
        """Respuesta de respaldo cuando falla la IA"""
        user_message_lower = user_message.lower()
        
        # Respuestas básicas basadas en palabras clave
        if any(word in user_message_lower for word in ["precio", "cuesta", "vale", "costo"]):
            return "¡Hola! Los precios de nuestras zapatillas van desde $25.000 hasta $65.000. ¿Te interesa alguna marca o modelo específico? Puedo darte más detalles sobre precios y disponibilidad."
        
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
