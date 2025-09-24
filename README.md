# Bot WhatsApp - Tienda de Zapatillas Dolores

## **Información del Proyecto**
- **Ubicación**: Dolores, Provincia de Buenos Aires, Argentina
- **Tipo**: Bot de WhatsApp con IA para tienda de zapatillas
- **IA**: OpenRouter.ai (modelo gratuito)
- **API**: WhatsApp Business API oficial
- **Hosting**: Render
- **Lenguaje**: Python + Flask

## **Tecnologías Utilizadas**
- **Backend**: Python 3.9+ con Flask
- **IA**: OpenRouter.ai API
- **WhatsApp**: WhatsApp Business API oficial
- **Base de datos**: SQLite (local) / PostgreSQL (producción)
- **Hosting**: Render
- **Variables de entorno**: python-dotenv

## **Dependencias**
```
Flask==2.3.3
requests==2.31.0
python-dotenv==1.0.0
sqlite3 (built-in)
```

## **Variables de Entorno Necesarias**
```
OPENROUTER_API_KEY=tu_token_openrouter
WHATSAPP_TOKEN=tu_token_whatsapp
WHATSAPP_PHONE_NUMBER_ID=tu_phone_number_id
WHATSAPP_VERIFY_TOKEN=tu_verify_token
RENDER_URL=https://tu-app.onrender.com
```

## **Información de la Tienda**
- **Nombre**: [Nombre de tu tienda]
- **Ubicación**: Dolores, Buenos Aires, Argentina
- **Productos**: Zapatillas deportivas y casuales
- **Horarios**: [Horarios de atención]
- **Contacto**: [Teléfono/Email]

## **Funcionalidades del Bot**
- Consultas sobre productos específicos
- Verificación de stock y tallas
- Información de precios
- Horarios y ubicación
- Consultas generales sobre la tienda
- Respuestas inteligentes con IA

## **Estructura del Proyecto**
```
tiendazapatillasbot/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias Python
├── database.py           # Configuración de base de datos
├── whatsapp.py           # Lógica de WhatsApp
├── openrouter.py         # Integración con OpenRouter
├── data/
│   ├── productos.json    # Catálogo de productos
│   └── tienda.json       # Información de la tienda
├── .env                  # Variables de entorno
├── .gitignore           # Archivos a ignorar
└── README.md            # Este archivo
```

## **Instalación y Uso**

### Local
```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/tiendazapatillasbot.git
cd tiendazapatillasbot

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp env.example .env
# Editar .env con tus tokens reales

# Probar el bot
python test_bot.py

# Iniciar servidor local
python app.py
```

### Render
1. Conectar repositorio GitHub
2. Configurar variables de entorno
3. Deploy automático

**Ver [DEPLOYMENT.md](DEPLOYMENT.md) para instrucciones detalladas de despliegue.**

## **Endpoints de WhatsApp**
- `POST /webhook` - Recibe mensajes de WhatsApp
- `GET /webhook` - Verificación de webhook

## **Configuración de IA**
- **Modelo**: Usa el modelo configurado en tu cuenta de OpenRouter
- **Contexto**: Información completa de la tienda
- **Prompts**: Optimizados para consultas de zapatillas

## **Base de Datos**
- **Productos**: ID, nombre, precio, tallas, stock, descripción
- **Tienda**: Información general, horarios, contacto
- **Conversaciones**: Historial de mensajes (opcional)

## **Seguridad**
- Verificación de tokens de WhatsApp
- Validación de webhooks
- Sanitización de inputs
- Rate limiting básico

## **Próximas Mejoras**
- Integración con sistema de inventario
- Procesamiento de pedidos
- Notificaciones de stock
- Analytics de conversaciones
- Multiidioma (español/inglés)