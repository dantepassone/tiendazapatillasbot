# 🚀 Guía de Despliegue - Bot WhatsApp Zapatillas Dolores

## 📋 **Requisitos Previos**

### 1. **Cuentas Necesarias**
- ✅ **OpenRouter.ai**: Cuenta con token de API
- ✅ **WhatsApp Business API**: Token de acceso
- ✅ **Render**: Cuenta para hosting
- ✅ **GitHub**: Repositorio del código

### 2. **Variables de Entorno Requeridas**
```bash
OPENROUTER_API_KEY=tu_token_openrouter
OPENROUTER_MODEL=meta-llama/llama-3.2-3b-instruct:free
WHATSAPP_TOKEN=tu_token_whatsapp
WHATSAPP_PHONE_NUMBER_ID=tu_phone_number_id
WHATSAPP_VERIFY_TOKEN=tu_verify_token_personalizado
RENDER_URL=https://tu-app.onrender.com
```

## 🔧 **Configuración Local**

### 1. **Clonar y Configurar**
```bash
git clone https://github.com/tu-usuario/tiendazapatillasbot.git
cd tiendazapatillasbot
```

### 2. **Instalar Dependencias**
```bash
pip install -r requirements.txt
```

### 3. **Configurar Variables de Entorno**
```bash
# Copiar archivo de ejemplo
cp env.example .env

# Editar .env con tus tokens reales
nano .env
```

### 4. **Probar Localmente**
```bash
# Ejecutar pruebas
python test_bot.py

# Iniciar servidor local
python app.py
```

## 🌐 **Despliegue en Render**

### 1. **Preparar Repositorio**
```bash
# Asegurarse de que todos los archivos estén committeados
git add .
git commit -m "Initial commit: Bot WhatsApp Zapatillas Dolores"
git push origin main
```

### 2. **Crear Aplicación en Render**
1. Ir a [render.com](https://render.com)
2. Hacer clic en "New +" → "Web Service"
3. Conectar tu repositorio de GitHub
4. Seleccionar el repositorio `tiendazapatillasbot`

### 3. **Configurar la Aplicación**
- **Name**: `bot-whatsapp-zapatillas`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`

### 4. **Configurar Variables de Entorno**
En la sección "Environment Variables" de Render, agregar:

| Variable | Valor |
|----------|-------|
| `OPENROUTER_API_KEY` | Tu token de OpenRouter |
| `OPENROUTER_MODEL` | `meta-llama/llama-3.2-3b-instruct:free` |
| `WHATSAPP_TOKEN` | Tu token de WhatsApp |
| `WHATSAPP_PHONE_NUMBER_ID` | Tu Phone Number ID |
| `WHATSAPP_VERIFY_TOKEN` | Token personalizado para verificación |
| `RENDER_URL` | URL de tu app (se llenará automáticamente) |
| `PORT` | `5000` |
| `FLASK_ENV` | `production` |

### 5. **Desplegar**
1. Hacer clic en "Create Web Service"
2. Esperar a que se complete el despliegue
3. Copiar la URL generada (ej: `https://bot-whatsapp-zapatillas.onrender.com`)

## 📱 **Configurar WhatsApp Business API**

### 1. **Configurar Webhook**
1. Ir a [Facebook Developers](https://developers.facebook.com)
2. Seleccionar tu aplicación de WhatsApp Business
3. Ir a "WhatsApp" → "Configuration"
4. En "Webhook URL", ingresar: `https://tu-app.onrender.com/webhook`
5. En "Verify Token", ingresar el mismo valor que configuraste en `WHATSAPP_VERIFY_TOKEN`
6. Hacer clic en "Verify and Save"

### 2. **Configurar Número de Teléfono**
1. En la misma sección, seleccionar tu número de teléfono
2. Verificar que esté activo y configurado correctamente

## 🧪 **Probar el Bot**

### 1. **Verificar Endpoints**
```bash
# Health check
curl https://tu-app.onrender.com/health

# Información de la tienda
curl https://tu-app.onrender.com/store

# Productos
curl https://tu-app.onrender.com/products
```

### 2. **Probar WhatsApp**
1. Enviar un mensaje a tu número de WhatsApp Business
2. El bot debería responder automáticamente
3. Probar diferentes consultas:
   - "Hola"
   - "¿Qué productos tienen?"
   - "¿Cuánto cuesta una Nike?"
   - "¿Cuáles son sus horarios?"

## 🔍 **Monitoreo y Logs**

### 1. **Ver Logs en Render**
1. Ir a tu aplicación en Render
2. Hacer clic en "Logs"
3. Monitorear la actividad del bot

### 2. **Endpoints de Monitoreo**
- `GET /health` - Estado de la aplicación
- `GET /` - Información básica
- `GET /store` - Información de la tienda
- `GET /products` - Lista de productos

## 🛠️ **Mantenimiento**

### 1. **Actualizar Productos**
Editar `data/productos.json` y hacer commit:
```bash
git add data/productos.json
git commit -m "Update products"
git push origin main
```

### 2. **Actualizar Información de la Tienda**
Editar `data/tienda.json` y hacer commit:
```bash
git add data/tienda.json
git commit -m "Update store info"
git push origin main
```

### 3. **Ver Logs de Conversaciones**
El bot guarda automáticamente las conversaciones en la base de datos SQLite.

## 🚨 **Solución de Problemas**

### 1. **Bot no responde**
- Verificar que el webhook esté configurado correctamente
- Revisar logs en Render
- Verificar que las variables de entorno estén configuradas

### 2. **Error de OpenRouter**
- Verificar que el token de API sea válido
- Revisar límites de uso en OpenRouter
- Verificar que el modelo esté disponible

### 3. **Error de WhatsApp**
- Verificar que el token de WhatsApp sea válido
- Revisar que el Phone Number ID sea correcto
- Verificar que el webhook esté verificado

## 📞 **Soporte**

Si tienes problemas:
1. Revisar los logs en Render
2. Verificar la configuración de variables de entorno
3. Probar los endpoints manualmente
4. Revisar la documentación de WhatsApp Business API

## 🎉 **¡Listo!**

Tu bot de WhatsApp para la tienda de zapatillas está funcionando. Los clientes pueden:
- Consultar productos y precios
- Verificar stock y tallas
- Obtener información de la tienda
- Recibir respuestas inteligentes con IA

¡Disfruta tu nuevo bot de WhatsApp! 🛍️
