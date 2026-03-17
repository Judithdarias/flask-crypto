# 📊 Aplicación Web de Gestión de Criptomonedas (Flask)

Aplicación web desarrollada en **Python** utilizando el framework **Flask** para gestionar inversiones en criptomonedas.

Permite registrar operaciones, consultar el valor actualizado de las criptos y visualizar el estado global de la inversión.

---

## 🚀 Funcionalidades

* Visualizar el listado de movimientos de criptomonedas
* Registrar **compras, ventas e intercambios (trades)**
* Consultar conversiones en tiempo real mediante la **API de CoinMarketCap**
* Almacenar operaciones en una base de datos **SQLite**
* Consultar el estado actual de la inversión

---

## 🛠️ Instalación

1. Clonar el repositorio
2. Crear y activar un entorno virtual de Python
3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

### Librerías principales

* Flask
* requests
* python-dotenv
* SQLite (incluido en Python)

---

## ⚙️ Configuración

Crear un archivo `.env` en la raíz del proyecto y añadir:

```env
API_KEY=TU_CLAVE
BASE_URL=https://pro-api.coinmarketcap.com
FLASK_APP=main.py
FLASK_DEBUG=True
```

⚠️ **Importante**

* La clave de la API es personal
* El archivo `.env` **no debe subirse al repositorio**

---

## 🗄️ Base de Datos

* Archivo: `data/crypto.sqlite`
* Tabla: `movimientos`

### Campos de la tabla

* id
* date
* time
* moneda_from
* cantidad_from
* moneda_to
* cantidad_to

La tabla se crea automáticamente al iniciar la aplicación.

---

## 💰 Tipos de Operaciones

La aplicación permite registrar:

* **Compra** → de EUR a criptomoneda
* **Venta** → de criptomoneda a EUR
* **Tradeo** → de una criptomoneda a otra

### Validaciones incluidas

* La moneda origen y destino no pueden ser iguales
* La cantidad debe ser mayor que cero
* No se puede vender o intercambiar más saldo del disponible
* Consulta automática del valor actualizado mediante CoinMarketCap

---

## 🌐 Rutas Principales

* `/` → Muestra el listado de movimientos
* `/purchase` → Permite calcular y registrar operaciones
* `/status` → Muestra el estado actual de la inversión

---

## ▶️ Ejecución de la Aplicación

En cualquier sistema operativo:

```bash
flask run
```

Modo debug:

```bash
flask run --debug
```

La aplicación se ejecutará en:

```
http://127.0.0.1:5000
```

---

## 📌 Notas

* Desarrollo web con Flask
* Consumo de APIs externas
* Gestión de bases de datos SQLite
* Arquitectura básica de aplicaciones backend
