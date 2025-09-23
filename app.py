from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from whatsapp import WhatsAppAPI
from database import Database
import logging

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar Flask app
app = Flask(__name__)

# Inicializar servicios
whatsapp_api = WhatsAppAPI()
db = Database()

@app.route("/", methods=["GET"])
def home():
    """Endpoint de inicio"""
    return jsonify({
        "status": "success",
        "message": "Bot WhatsApp Zapatillas Dolores está funcionando",
        "version": "1.0.0"
    })

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    """Verifica el webhook de WhatsApp"""
    try:
        # Obtener parámetros de la URL
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        
        logger.info(f"Verificando webhook: mode={mode}, token={token}")
        
        # Verificar webhook
        result = whatsapp_api.verify_webhook(mode, token, challenge)
        
        if result:
            logger.info("Webhook verificado exitosamente")
            return result
        else:
            logger.error("Webhook verification failed")
            return "Verification failed", 403
            
    except Exception as e:
        logger.error(f"Error verificando webhook: {str(e)}")
        return "Error", 500

@app.route("/webhook", methods=["POST"])
def webhook():
    """Recibe mensajes de WhatsApp"""
    try:
        # Obtener datos del webhook
        data = request.get_json()
        
        if not data:
            logger.warning("No data received in webhook")
            return "No data", 400
        
        logger.info(f"Webhook data received: {data}")
        
        # Verificar si es un mensaje válido
        if "entry" in data:
            for entry in data["entry"]:
                if "changes" in entry:
                    for change in entry["changes"]:
                        if "value" in change and "messages" in change["value"]:
                            messages = change["value"]["messages"]
                            
                            for message in messages:
                                # Procesar mensaje
                                success = whatsapp_api.process_message(message)
                                
                                if success:
                                    logger.info("Mensaje procesado exitosamente")
                                else:
                                    logger.error("Error procesando mensaje")
        
        return "OK", 200
        
    except Exception as e:
        logger.error(f"Error procesando webhook: {str(e)}")
        return "Error", 500

@app.route("/send-message", methods=["POST"])
def send_message():
    """Endpoint para enviar mensajes manualmente (para testing)"""
    try:
        data = request.get_json()
        
        if not data or "to" not in data or "message" not in data:
            return jsonify({"error": "Missing required fields: to, message"}), 400
        
        to = data["to"]
        message = data["message"]
        
        success = whatsapp_api.send_message(to, message)
        
        if success:
            return jsonify({"status": "success", "message": "Message sent"})
        else:
            return jsonify({"status": "error", "message": "Failed to send message"}), 500
            
    except Exception as e:
        logger.error(f"Error enviando mensaje: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/products", methods=["GET"])
def get_products():
    """Endpoint para obtener productos"""
    try:
        categoria = request.args.get("categoria")
        marca = request.args.get("marca")
        search = request.args.get("search")
        
        if search:
            products = db.buscar_productos(search)
        else:
            products = db.get_productos(categoria, marca)
        
        return jsonify({
            "status": "success",
            "products": products,
            "count": len(products)
        })
        
    except Exception as e:
        logger.error(f"Error obteniendo productos: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """Endpoint para obtener un producto específico"""
    try:
        product = db.get_producto_por_id(product_id)
        
        if product:
            return jsonify({
                "status": "success",
                "product": product
            })
        else:
            return jsonify({"error": "Product not found"}), 404
            
    except Exception as e:
        logger.error(f"Error obteniendo producto: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/store", methods=["GET"])
def get_store_info():
    """Endpoint para obtener información de la tienda"""
    try:
        store_info = db.get_tienda_info()
        
        return jsonify({
            "status": "success",
            "store": store_info
        })
        
    except Exception as e:
        logger.error(f"Error obteniendo información de la tienda: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/conversations/<phone_number>", methods=["GET"])
def get_conversations(phone_number):
    """Endpoint para obtener historial de conversaciones"""
    try:
        limit = request.args.get("limit", 10, type=int)
        conversations = db.get_conversation_history(phone_number, limit)
        
        return jsonify({
            "status": "success",
            "conversations": conversations
        })
        
    except Exception as e:
        logger.error(f"Error obteniendo conversaciones: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health_check():
    """Endpoint de health check"""
    try:
        # Verificar conexión a la base de datos
        store_info = db.get_tienda_info()
        
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "store": "loaded" if store_info else "not_loaded"
        })
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500

@app.route("/test-ai", methods=["GET"])
def test_ai():
    """Endpoint para probar la IA"""
    try:
        from openrouter import OpenRouterAI
        ai = OpenRouterAI()
        
        # Probar generación de respuesta
        test_message = "Hola, ¿qué productos tienen?"
        response = ai.generate_response(test_message, "test_phone")
        
        return jsonify({
            "status": "success",
            "test_message": test_message,
            "ai_response": response,
            "model": ai.model
        })
        
    except Exception as e:
        logger.error(f"AI test failed: {str(e)}")
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route("/test-whatsapp", methods=["GET"])
def test_whatsapp():
    """Endpoint para probar configuración de WhatsApp"""
    try:
        from whatsapp import WhatsAppAPI
        whatsapp = WhatsAppAPI()
        
        return jsonify({
            "status": "success",
            "whatsapp_configured": bool(whatsapp.access_token),
            "phone_number_id": whatsapp.phone_number_id,
            "verify_token_set": bool(whatsapp.verify_token)
        })
        
    except Exception as e:
        logger.error(f"WhatsApp test failed: {str(e)}")
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Manejo de errores 404"""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Manejo de errores 500"""
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    # Obtener puerto desde variables de entorno
    port = int(os.getenv("PORT", 5000))
    
    # Verificar variables de entorno requeridas
    required_vars = [
        "OPENROUTER_API_KEY",
        "WHATSAPP_TOKEN",
        "WHATSAPP_PHONE_NUMBER_ID",
        "WHATSAPP_VERIFY_TOKEN"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        logger.error("Please check your .env file")
        exit(1)
    
    logger.info("Starting Bot WhatsApp Zapatillas Dolores...")
    logger.info(f"Server running on port {port}")
    
    # Iniciar servidor
    app.run(
        host="0.0.0.0",
        port=port,
        debug=os.getenv("FLASK_ENV") != "production"
    )
