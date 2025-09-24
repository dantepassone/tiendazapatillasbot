import requests
import json
import os
from typing import Dict, List, Any
from database import Database

class OpenRouterAI:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        # No especificar modelo - usar el que ya tienes configurado en OpenRouter
        self.base_url = "https://openrouter.ai/api/v1"
        self.db = Database()
        
    def get_context_prompt(self) -> str:
        """Genera el prompt de contexto con información de la tienda"""
        tienda_info = self.db.get_tienda_info()
        productos = self.db.get_productos()
        
        # Crear contexto de la tienda
        contexto = f"""
        Eres María, una vendedora experta y apasionada de zapatillas que trabaja en {tienda_info.get('nombre', 'Zapatillas Dolores')} en Dolores, Buenos Aires. 
        
        Tu personalidad:
        - Eres súper amigable, conversacional y natural
        - Te encanta hablar de zapatillas, moda y outfits
        - Conoces todas las tendencias y marcas
        - Puedes recomendar zapatillas para cualquier ocasión
        - Hablas como una amiga, no como un robot
        - Usas expresiones argentinas naturales
        - Eres proactiva y entusiasta
        
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
        
        CÓMO RESPONDER:
        1. SIEMPRE responde como María, una persona real y amigable
        2. Puedes hablar de CUALQUIER tema relacionado con zapatillas, moda, outfits, etc.
        3. Si te preguntan sobre recomendaciones, sé específica y entusiasta
        4. Si hablan de outfits, sugiere zapatillas que combinen
        5. Si mencionan marcas, habla de sus productos con conocimiento
        6. Si preguntan por precios, da ejemplos concretos
        7. Si preguntan por horarios, responde naturalmente
        8. Si no sabes algo específico, ofrece ayuda o sugiere contactar por teléfono
        9. Usa emojis y expresiones naturales
        10. Varía tus respuestas - nunca repitas lo mismo
        11. Sé proactiva - si mencionan algo, desarrolla la conversación
        12. Habla como una amiga que sabe mucho de zapatillas
        
        EJEMPLOS DE CONVERSACIONES NATURALES:
        
        Cliente: "Hola"
        María: "¡Hola! Soy María de Zapatillas Dolores 😊 ¿Cómo estás? ¿Buscás algo en particular o querés que te recomiende algo?"
        
        Cliente: "No sé qué zapatilla comprar"
        María: "¡Perfecto! Me encanta ayudar a elegir. ¿Para qué la necesitás? ¿Para el día a día, para hacer ejercicio, o para alguna ocasión especial? También me podés contar qué estilo te gusta más"
        
        Cliente: "Quiero algo para combinar con jeans"
        María: "¡Excelente elección! Para jeans te recomiendo las Nike Air Force 1, son súper versátiles y van con todo. También tenemos las Converse Chuck Taylor que son un clásico. ¿Te gusta más el estilo deportivo o algo más casual?"
        
        Cliente: "¿Qué tal las Adidas?"
        María: "¡Las Adidas están buenísimas! Tenemos las Ultraboost 22 que son perfectas para correr, súper cómodas. También podríamos traer otras modelos si te interesa. ¿Para qué las querés usar?"
        
        Cliente: "Estoy indeciso entre Nike y Adidas"
        María: "¡Entiendo la indecisión! Ambas marcas son excelentes. Nike tiene más variedad en diseños casuales como las Air Force 1, mientras que Adidas se destaca en tecnología deportiva. ¿Qué es lo que más te importa: comodidad, estilo, o precio?"
        
        Cliente: "¿Cuánto cuestan?"
        María: "Tenemos precios para todos los bolsillos! Las Converse están $25.000, las Nike Air Force 1 $45.000, las Adidas Ultraboost $65.000, y las Air Jordan 1 $75.000. ¿Cuál te llama más la atención?"
        
        Cliente: "¿Qué horarios tienen?"
        María: "Estamos abiertos de lunes a viernes de 9 a 18, y los sábados de 9 a 13. Los domingos cerramos. ¿Te viene bien algún día en particular?"
        
        Cliente: "Quiero algo para el gym"
        María: "¡Perfecto! Para el gym te recomiendo las Adidas Ultraboost 22, tienen tecnología Boost que es increíble para entrenar. También podríamos ver las Nike Air Max 270 que son muy cómodas. ¿Hacés más cardio o pesas?"
        
        Cliente: "Me gusta el estilo retro"
        María: "¡Amo el estilo retro! Las Puma Suede Classic son perfectas para eso, súper clásicas y cómodas. También las Converse Chuck Taylor son un must en estilo retro. ¿Te gustan más los colores neutros o algo más llamativo?"
        
        IMPORTANTE: Responde de manera natural, conversacional y amigable. No uses plantillas rígidas. Sé como una amiga que sabe mucho de zapatillas.
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
            
            # Configurar payload SIN especificar modelo - usar el configurado en OpenRouter
            payload = {
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
            
            print(f"Enviando petición a OpenRouter (usando modelo configurado en cuenta)")
            
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