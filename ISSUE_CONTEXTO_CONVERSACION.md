# Issue: Implementar Contexto de Conversación en el Bot de WhatsApp

## **Problema Actual**
El bot de WhatsApp no tiene memoria de la conversación, lo que causa:
- Se presenta ("Hola, soy María") en cada mensaje
- No recuerda lo que hablaron antes
- No tiene contexto de la conversación
- Respuestas repetitivas y poco naturales

## **Solución Propuesta**
Implementar un sistema de contexto que:
- Recuerde los últimos 3-5 mensajes de cada usuario
- Incluya ese historial en el prompt de la IA
- Haga la conversación más fluida y natural
- Evite presentaciones repetitivas

## **Cambios Necesarios**

### **1. Modificar `database.py`**
```python
def get_conversation_history(self, phone_number: str, limit: int = 5) -> List[Dict]:
    """Obtiene el historial de conversación de un usuario"""
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT user_message, ai_response, timestamp 
        FROM conversaciones 
        WHERE phone_number = ? 
        ORDER BY timestamp DESC 
        LIMIT ?
    """, (phone_number, limit))
    
    history = cursor.fetchall()
    conn.close()
    
    return [{"user": row[0], "ai": row[1], "timestamp": row[2]} for row in history]
```

### **2. Modificar `openrouter.py`**
```python
def get_context_prompt(self, phone_number: str = None) -> str:
    """Genera el prompt con contexto de conversación"""
    # ... código existente ...
    
    # Agregar historial de conversación si existe
    if phone_number:
        history = self.db.get_conversation_history(phone_number, 3)
        if history:
            contexto += "\n\nCONVERSACIÓN ANTERIOR:\n"
            for msg in reversed(history):  # Orden cronológico
                contexto += f"Usuario: {msg['user']}\n"
                contexto += f"María: {msg['ai']}\n"
    
    # ... resto del código ...
```

### **3. Modificar `generate_response`**
```python
def generate_response(self, user_message: str, phone_number: str = None) -> str:
    """Genera respuesta con contexto"""
    try:
        # ... código existente ...
        
        # Usar contexto con historial
        context_prompt = self.get_context_prompt(phone_number)
        full_prompt = f"{context_prompt}\n\nCliente pregunta: {user_message}\n\nRespuesta:"
        
        # ... resto del código ...
```

## **Beneficios**
- ✅ Conversación más natural y fluida
- ✅ No más presentaciones repetitivas
- ✅ Mejor experiencia de usuario
- ✅ Respuestas más contextuales
- ✅ Menos repetición de información

## **Consideraciones Técnicas**
- **Límite de tokens**: El historial no debe ser muy largo para evitar límites de tokens
- **Privacidad**: El historial se guarda localmente en SQLite
- **Rendimiento**: Solo se cargan los últimos 3-5 mensajes por usuario

## **Testing**
- Probar conversación larga con múltiples temas
- Verificar que no se presente repetidamente
- Confirmar que recuerda información previa
- Validar que funciona con múltiples usuarios

## **Prioridad**
**Alta** - Mejora significativa en la experiencia del usuario

## **Estimación**
2-3 horas de desarrollo + testing
