# Robot Soccer -- Multi-Agent Python Simulation

## 🎮 Descripción

Este proyecto simula **11 jugadores de Robot Soccer**, ejecutados como
**procesos independientes** en Python.\
Roles incluidos:

-   **1 Arquero**
-   **4 Defensas**
-   **6 Atacantes**

El script `manager.py` lanza y administra todos los procesos. Cada
jugador ejecuta su propio comportamiento definido en `players/`.

------------------------------------------------------------------------

## 📁 Estructura del Proyecto

    robot_soccer/
    │
    ├── requirements.txt
    ├── run_all.sh
    ├── manager.py
    │
    └── players/
        ├── base_player.py
        ├── defender.py
        ├── attacker.py
        ├── goalkeeper.py

------------------------------------------------------------------------

## 🐍 Crear entorno virtual

``` bash
python3 -m venv env
source env/bin/activate
```

Desactivar:

``` bash
deactivate
```

------------------------------------------------------------------------

## 📦 Instalar dependencias

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## ▶️ Ejecución

### Usando el script `.sh`

``` bash
chmod +x run_all.sh
./run_all.sh
```

### O ejecutando el manager:

``` bash
python3 manager.py
```

------------------------------------------------------------------------

## 📡 Logs

Cada proceso imprime mensajes como:

    [DEFENDER #2] Defendiendo zona...
    [ATTACKER #5] Atacando y buscando gol...
    [GOALKEEPER #1] Protegiendo el arco...

------------------------------------------------------------------------

## 🧩 Personalización

Edita `manager.py` para cambiar las cantidades:

``` python
ROLES = {
    "goalkeeper": 1,
    "defender": 4,
    "attacker": 6
}
```

------------------------------------------------------------------------

## ❤️ Contribuciones

Puedes agregar IA, sockets, estrategias o nuevas posiciones.
