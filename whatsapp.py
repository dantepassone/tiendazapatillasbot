import requests
import json
import os
from typing import Dict, Any, Optional
from openrouter import OpenRouterAI
import urllib.parse

class WhatsAppAPI:
    def __init__(self):
        self.access_token = os.getenv("WHATSAPP_TOKEN")
        self.phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        self.verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN")
        self.base_url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}/messages"
        self.ai = OpenRouterAI()
        
    def send_message(self, to: str, message: str) -> bool:
        """Envía un mensaje de texto a WhatsApp"""
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "text",
                "text": {
                    "body": message
                }
            }
            
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"Mensaje enviado exitosamente a {to}")
                return True
            else:
                print(f"Error enviando mensaje: {response.status_code}")
                print(f"Respuesta: {response.text}")
                return False
                
        except Exception as e:
            print(f"Error enviando mensaje: {str(e)}")
            return False
    
    def send_template_message(self, to: str, template_name: str, language_code: str = "es") -> bool:
        """Envía un mensaje de plantilla a WhatsApp"""
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {
                        "code": language_code
                    }
                }
            }
            
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"Plantilla enviada exitosamente a {to}")
                return True
            else:
                print(f"Error enviando plantilla: {response.status_code}")
                print(f"Respuesta: {response.text}")
                return False
                
        except Exception as e:
            print(f"Error enviando plantilla: {str(e)}")
            return False
    
    def send_document_message(self, to: str, document_url: str, filename: str = "lista_precios.pdf", caption: str = "") -> bool:
        """Envía un documento PDF a WhatsApp"""
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "document",
                "document": {
                    "link": document_url,
                    "filename": filename,
                    "caption": caption
                }
            }
            
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"Documento enviado exitosamente a {to}")
                return True
            else:
                print(f"Error enviando documento: {response.status_code}")
                print(f"Respuesta: {response.text}")
                return False
                
        except Exception as e:
            print(f"Error enviando documento: {str(e)}")
            return False
    
    def send_product_message(self, to: str, product: Dict[str, Any]) -> bool:
        """Envía información de un producto en formato estructurado"""
        try:
            # Crear mensaje con información del producto
            message = f"""
🛍️ *{product['marca']} {product['nombre']}*

💰 *Precio:* ${product['precio']:,}
📏 *Tallas disponibles:* {', '.join(product['tallas'])}
🎨 *Colores:* {', '.join(product['colores'])}
📦 *Stock total:* {sum(product['stock'].values())} unidades

📝 *Descripción:*
{product['descripcion']}

¿Te interesa este producto? ¿Qué talla necesitas?
            """.strip()
            
            return self.send_message(to, message)
            
        except Exception as e:
            print(f"Error enviando información del producto: {str(e)}")
            return False
    
    def send_catalog_message(self, to: str, products: list) -> bool:
        """Envía un catálogo de productos"""
        try:
            if not products:
                message = "No encontré productos que coincidan con tu búsqueda. ¿Podrías ser más específico?"
                return self.send_message(to, message)
            
            message = "🛍️ *Catálogo de Productos*\n\n"
            
            for i, product in enumerate(products[:5], 1):  # Mostrar máximo 5 productos
                message += f"{i}. *{product['marca']} {product['nombre']}*\n"
                message += f"   💰 ${product['precio']:,}\n"
                message += f"   📏 Tallas: {', '.join(product['tallas'])}\n"
                message += f"   🎨 Colores: {', '.join(product['colores'])}\n\n"
            
            if len(products) > 5:
                message += f"... y {len(products) - 5} productos más.\n\n"
            
            message += "¿Te interesa algún producto específico? Puedo darte más detalles."
            
            return self.send_message(to, message)
            
        except Exception as e:
            print(f"Error enviando catálogo: {str(e)}")
            return False
    
    def send_store_info_message(self, to: str) -> bool:
        """Envía información de la tienda"""
        try:
            tienda_info = self.ai.db.get_tienda_info()
            
            message = f"""
🏪 *{tienda_info.get('nombre', 'Zapatillas Dolores')}*

📍 *Ubicación:* {tienda_info.get('ubicacion', 'Dolores, Buenos Aires, Argentina')}
🏠 *Dirección:* {tienda_info.get('direccion', 'Calle Principal 123, Dolores, Buenos Aires')}
📞 *Teléfono:* {tienda_info.get('telefono', '+54 9 11 1234-5678')}
📧 *Email:* {tienda_info.get('email', 'info@zapatillasdolores.com')}

🕒 *Horarios de Atención:*
            """
            
            if 'horarios' in tienda_info:
                for dia, horario in tienda_info['horarios'].items():
                    message += f"• {dia.replace('_', ' ').title()}: {horario}\n"
            
            message += f"""
💳 *Métodos de Pago:*
            """
            
            if 'metodos_pago' in tienda_info:
                for metodo in tienda_info['metodos_pago']:
                    message += f"• {metodo}\n"
            
            message += f"""
🚚 *Envíos:*
            """
            
            if 'envios' in tienda_info:
                for tipo, precio in tienda_info['envios'].items():
                    message += f"• {tipo.title()}: {precio}\n"
            
            message += "\n¡Te esperamos en nuestra tienda! 🛍️"
            
            return self.send_message(to, message)
            
        except Exception as e:
            print(f"Error enviando información de la tienda: {str(e)}")
            return False
    
    def send_price_list_pdf(self, to: str) -> bool:
        """Envía la lista de precios en PDF"""
        try:
            # URL del PDF proporcionada
            pdf_url = "https://doc-0g-5c-apps-viewer.googleusercontent.com/viewer/secure/pdf/jq1q8fvv4aj7nkrdgvl63dj88876jnbk/65m3raapm4se7qlhg2193gs5ja0tiqqu/1760484750000/drive/00711664236692323085/ACFrOgDILoXafo33PBcGg4aFLa40OhoeY44iUscZR1wuToeGycwIHQ8pQW9A-brTgcJ_KJeLYjWh0QCz0T_eg-Hgqoh3IMlc8c-1ckh7U1lCA21kS7iH0SFm40QrsuJ7hM9FSgj2vbMlOtwRMgxnNla5YB25JpgCde9faWC2Ie91j7mzYr_s13D36zA__T7gLCtDuUjlzgPWCKelyQhACpDwO00ciBYhNifFV2-iANKOAdhr1VK9Lv6NKPglLZ2GpStzvXzMzeRokdn39BTK?print=true&nonce=dd5nm6p9npifa&user=00711664236692323085&hash=dt87jesvspr4r80forvrjm1kv8c91itn"
            
            # Primero enviar un mensaje explicativo
            message = "📋 Te envío nuestra lista de precios actualizada. Ahí vas a encontrar todos los productos con sus precios y descuentos disponibles."
            self.send_message(to, message)
            
            # Luego enviar el PDF
            caption = "📋 Lista de Precios - Zapatillas Dolores\n\nAquí tenés todos nuestros productos con precios actualizados. ¡Cualquier consulta, avisame!"
            return self.send_document_message(to, pdf_url, "lista_precios.pdf", caption)
            
        except Exception as e:
            print(f"Error enviando lista de precios: {str(e)}")
            return False
    
    def process_message(self, message_data: Dict[str, Any]) -> bool:
        """Procesa un mensaje entrante y genera respuesta"""
        try:
            # Extraer información del mensaje
            phone_number = message_data.get("from")
            message_text = message_data.get("text", {}).get("body", "")
            message_id = message_data.get("id")
            
            if not phone_number or not message_text:
                print("Mensaje inválido recibido")
                return False
            
            print(f"Mensaje recibido de {phone_number}: {message_text}")
            
            # Verificar si pide lista de precios
            message_lower = message_text.lower()
            price_list_keywords = [
                "lista de precios", "lista precios", "precios", "catálogo", "catalogo",
                "precio lista", "lista", "pdf", "archivo", "documento"
            ]
            
            if any(keyword in message_lower for keyword in price_list_keywords):
                print("Usuario pidió lista de precios, enviando PDF...")
                return self.send_price_list_pdf(phone_number)
            
            # Procesar mensaje con IA
            ai_response = self.ai.generate_response(message_text, phone_number)
            
            # Enviar respuesta
            success = self.send_message(phone_number, ai_response)
            
            if success:
                print(f"Respuesta enviada a {phone_number}")
            else:
                print(f"Error enviando respuesta a {phone_number}")
            
            return success
            
        except Exception as e:
            print(f"Error procesando mensaje: {str(e)}")
            return False
    
    def process_quick_reply(self, message_data: Dict[str, Any]) -> bool:
        """Procesa respuestas rápidas (botones)"""
        try:
            phone_number = message_data.get("from")
            quick_reply = message_data.get("interactive", {}).get("button_reply", {})
            button_id = quick_reply.get("id")
            button_title = quick_reply.get("title")
            
            if not phone_number or not button_id:
                return False
            
            print(f"Respuesta rápida recibida de {phone_number}: {button_title}")
            
            # Procesar según el botón presionado
            if button_id == "catalogo":
                products = self.ai.db.get_productos()
                return self.send_catalog_message(phone_number, products)
            
            elif button_id == "tienda_info":
                return self.send_store_info_message(phone_number)
            
            elif button_id == "horarios":
                tienda_info = self.ai.db.get_tienda_info()
                message = "🕒 *Horarios de Atención:*\n\n"
                if 'horarios' in tienda_info:
                    for dia, horario in tienda_info['horarios'].items():
                        message += f"• {dia.replace('_', ' ').title()}: {horario}\n"
                return self.send_message(phone_number, message)
            
            elif button_id == "contacto":
                tienda_info = self.ai.db.get_tienda_info()
                message = f"""
📞 *Información de Contacto:*

🏠 *Dirección:* {tienda_info.get('direccion', 'Calle Principal 123, Dolores, Buenos Aires')}
📞 *Teléfono:* {tienda_info.get('telefono', '+54 9 11 1234-5678')}
📧 *Email:* {tienda_info.get('email', 'info@zapatillasdolores.com')}
                """.strip()
                return self.send_message(phone_number, message)
            
            else:
                # Respuesta genérica para botones no reconocidos
                return self.send_message(phone_number, "Gracias por tu mensaje. ¿En qué más puedo ayudarte?")
            
        except Exception as e:
            print(f"Error procesando respuesta rápida: {str(e)}")
            return False
    
    def send_welcome_message(self, phone_number: str) -> bool:
        """Envía mensaje de bienvenida con botones"""
        try:
            message = """
¡Hola! 👋 Bienvenido a *Zapatillas Dolores*

Soy tu asistente virtual y estoy aquí para ayudarte con:

🛍️ Información sobre productos
💰 Precios y disponibilidad
📏 Tallas disponibles
🕒 Horarios de atención
📍 Ubicación y contacto

¿En qué puedo asistirte hoy?
            """.strip()
            
            return self.send_message(phone_number, message)
            
        except Exception as e:
            print(f"Error enviando mensaje de bienvenida: {str(e)}")
            return False
    
    def verify_webhook(self, mode: str, token: str, challenge: str) -> Optional[str]:
        """Verifica el webhook de WhatsApp"""
        if mode == "subscribe" and token == self.verify_token:
            print("Webhook verificado exitosamente")
            return challenge
        else:
            print("Webhook verification failed")
            return None
