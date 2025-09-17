import sqlite3
import json
import os
from typing import Dict, List, Any

class Database:
    def __init__(self, db_path: str = "tienda.db"):
        self.db_path = db_path
        self.init_database()
        self.load_initial_data()
    
    def init_database(self):
        """Inicializa la base de datos con las tablas necesarias"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de productos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                marca TEXT NOT NULL,
                categoria TEXT NOT NULL,
                precio REAL NOT NULL,
                tallas TEXT NOT NULL,
                stock TEXT NOT NULL,
                colores TEXT NOT NULL,
                descripcion TEXT,
                imagen TEXT
            )
        ''')
        
        # Tabla de tienda
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tienda (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                ubicacion TEXT NOT NULL,
                direccion TEXT,
                telefono TEXT,
                email TEXT,
                horarios TEXT NOT NULL,
                metodos_pago TEXT NOT NULL,
                envios TEXT NOT NULL,
                redes_sociales TEXT,
                descripcion TEXT
            )
        ''')
        
        # Tabla de conversaciones (opcional, para historial)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT NOT NULL,
                mensaje TEXT NOT NULL,
                respuesta TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def load_initial_data(self):
        """Carga los datos iniciales desde los archivos JSON"""
        # Cargar datos de la tienda
        if os.path.exists("data/tienda.json"):
            with open("data/tienda.json", "r", encoding="utf-8") as f:
                tienda_data = json.load(f)
                self.save_tienda_data(tienda_data)
        
        # Cargar datos de productos
        if os.path.exists("data/productos.json"):
            with open("data/productos.json", "r", encoding="utf-8") as f:
                productos_data = json.load(f)
                self.save_productos_data(productos_data["productos"])
    
    def save_tienda_data(self, tienda_data: Dict[str, Any]):
        """Guarda los datos de la tienda en la base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Limpiar datos existentes
        cursor.execute("DELETE FROM tienda")
        
        # Insertar nuevos datos
        cursor.execute('''
            INSERT INTO tienda (nombre, ubicacion, direccion, telefono, email, 
                              horarios, metodos_pago, envios, redes_sociales, descripcion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            tienda_data["nombre"],
            tienda_data["ubicacion"],
            tienda_data.get("direccion", ""),
            tienda_data.get("telefono", ""),
            tienda_data.get("email", ""),
            json.dumps(tienda_data["horarios"]),
            json.dumps(tienda_data["metodos_pago"]),
            json.dumps(tienda_data["envios"]),
            json.dumps(tienda_data.get("redes_sociales", {})),
            tienda_data.get("descripcion", "")
        ))
        
        conn.commit()
        conn.close()
    
    def save_productos_data(self, productos_data: List[Dict[str, Any]]):
        """Guarda los datos de productos en la base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Limpiar datos existentes
        cursor.execute("DELETE FROM productos")
        
        # Insertar nuevos datos
        for producto in productos_data:
            cursor.execute('''
                INSERT INTO productos (id, nombre, marca, categoria, precio, 
                                    tallas, stock, colores, descripcion, imagen)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                producto["id"],
                producto["nombre"],
                producto["marca"],
                producto["categoria"],
                producto["precio"],
                json.dumps(producto["tallas"]),
                json.dumps(producto["stock"]),
                json.dumps(producto["colores"]),
                producto.get("descripcion", ""),
                producto.get("imagen", "")
            ))
        
        conn.commit()
        conn.close()
    
    def get_tienda_info(self) -> Dict[str, Any]:
        """Obtiene la información de la tienda"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tienda LIMIT 1")
        row = cursor.fetchone()
        
        if row:
            tienda_info = {
                "nombre": row[1],
                "ubicacion": row[2],
                "direccion": row[3],
                "telefono": row[4],
                "email": row[5],
                "horarios": json.loads(row[6]),
                "metodos_pago": json.loads(row[7]),
                "envios": json.loads(row[8]),
                "redes_sociales": json.loads(row[9]),
                "descripcion": row[10]
            }
        else:
            tienda_info = {}
        
        conn.close()
        return tienda_info
    
    def get_productos(self, categoria: str = None, marca: str = None) -> List[Dict[str, Any]]:
        """Obtiene la lista de productos con filtros opcionales"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM productos WHERE 1=1"
        params = []
        
        if categoria:
            query += " AND categoria = ?"
            params.append(categoria)
        
        if marca:
            query += " AND marca = ?"
            params.append(marca)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        productos = []
        for row in rows:
            producto = {
                "id": row[0],
                "nombre": row[1],
                "marca": row[2],
                "categoria": row[3],
                "precio": row[4],
                "tallas": json.loads(row[5]),
                "stock": json.loads(row[6]),
                "colores": json.loads(row[7]),
                "descripcion": row[8],
                "imagen": row[9]
            }
            productos.append(producto)
        
        conn.close()
        return productos
    
    def get_producto_por_id(self, producto_id: int) -> Dict[str, Any]:
        """Obtiene un producto específico por ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
        row = cursor.fetchone()
        
        if row:
            producto = {
                "id": row[0],
                "nombre": row[1],
                "marca": row[2],
                "categoria": row[3],
                "precio": row[4],
                "tallas": json.loads(row[5]),
                "stock": json.loads(row[6]),
                "colores": json.loads(row[7]),
                "descripcion": row[8],
                "imagen": row[9]
            }
        else:
            producto = {}
        
        conn.close()
        return producto
    
    def buscar_productos(self, termino: str) -> List[Dict[str, Any]]:
        """Busca productos por nombre, marca o descripción"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT * FROM productos 
            WHERE nombre LIKE ? OR marca LIKE ? OR descripcion LIKE ?
        '''
        termino_busqueda = f"%{termino}%"
        cursor.execute(query, (termino_busqueda, termino_busqueda, termino_busqueda))
        rows = cursor.fetchall()
        
        productos = []
        for row in rows:
            producto = {
                "id": row[0],
                "nombre": row[1],
                "marca": row[2],
                "categoria": row[3],
                "precio": row[4],
                "tallas": json.loads(row[5]),
                "stock": json.loads(row[6]),
                "colores": json.loads(row[7]),
                "descripcion": row[8],
                "imagen": row[9]
            }
            productos.append(producto)
        
        conn.close()
        return productos
    
    def verificar_stock(self, producto_id: int, talla: str) -> bool:
        """Verifica si hay stock de un producto en una talla específica"""
        producto = self.get_producto_por_id(producto_id)
        if not producto:
            return False
        
        stock = producto["stock"]
        return talla in stock and stock[talla] > 0
    
    def get_stock_disponible(self, producto_id: int) -> Dict[str, int]:
        """Obtiene el stock disponible de un producto"""
        producto = self.get_producto_por_id(producto_id)
        if not producto:
            return {}
        
        return {talla: cantidad for talla, cantidad in producto["stock"].items() if cantidad > 0}
    
    def save_conversation(self, phone_number: str, mensaje: str, respuesta: str):
        """Guarda una conversación en el historial"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversaciones (phone_number, mensaje, respuesta)
            VALUES (?, ?, ?)
        ''', (phone_number, mensaje, respuesta))
        
        conn.commit()
        conn.close()
    
    def get_conversation_history(self, phone_number: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Obtiene el historial de conversaciones de un número"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT mensaje, respuesta, timestamp 
            FROM conversaciones 
            WHERE phone_number = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (phone_number, limit))
        
        rows = cursor.fetchall()
        conversaciones = []
        
        for row in rows:
            conversacion = {
                "mensaje": row[0],
                "respuesta": row[1],
                "timestamp": row[2]
            }
            conversaciones.append(conversacion)
        
        conn.close()
        return conversaciones
