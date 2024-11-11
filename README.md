# 🎮 SUDOKING - Resolvedor de Sudokus

<div align="center">

![SUDOKING Logo](assets/images/logo.png)

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Pygame](https://img.shields.io/badge/Pygame-2.5.2-yellow.svg)](https://www.pygame.org/)

</div>

## 📝 Descripción

SUDOKING es una aplicación de escritorio moderna y elegante que permite a los usuarios jugar, resolver y generar puzzles de Sudoku. Implementada en Python utilizando Pygame, la aplicación combina una interfaz gráfica intuitiva con un potente algoritmo de resolución basado en backtracking.

## ✨ Características Principales

- 🎯 **Interfaz Gráfica Intuitiva**
  - Diseño limpio y moderno
  - Selección de casillas con el ratón
  - Entrada de números mediante teclado
  - Feedback visual inmediato

- 🎲 **Funcionalidades del Juego**
  - Generación de nuevos puzzles
  - Tres niveles de dificultad (Fácil, Normal, Difícil)
  - Sistema de validación en tiempo real
  - Resolución automática de puzzles

- 🏆 **Sistema de Puntuación**
  - Tracking de tiempo
  - Tabla de puntuaciones altas
  - Puntuación basada en dificultad y tiempo
  - Guardado automático de records

- ⚙️ **Configuración Personalizable**
  - Ajustes de dificultad
  - Temas de color
  - Configuración de sonido
  - Tamaño de fuente ajustable

## 🚀 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/kigaldev/SUDOKING
cd sudoking
```

2. Crea un entorno virtual e instala las dependencias:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Ejecuta el programa:
```bash
python sudoking.py
```

## 🎮 Cómo Jugar

1. **Controles Básicos**:
   - Click izquierdo para seleccionar una casilla
   - Números 1-9 para insertar valores
   - 'R' para resolver automáticamente
   - 'C' para limpiar el tablero
   - 'V' para verificar la solución

2. **Interfaz**:
   - Panel principal con el tablero de Sudoku
   - Botones de acción en la parte inferior
   - Indicador de tiempo y puntuación
   - Feedback visual de errores

## 🛠️ Estructura del Proyecto

```
sudoking/
├── sudoking.py          # Archivo principal
├── gui.py              # Interfaz gráfica
├── sudoku_solver.py    # Algoritmo de resolución
├── utils.py            # Utilidades
├── requirements.txt    # Dependencias
├── LICENSE            # Licencia MIT
└── assets/           # Recursos
    ├── fonts/        # Fuentes
    └── images/       # Imágenes
```

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir los cambios que te gustaría realizar.

1. Fork el proyecto
2. Crea tu rama de características (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📜 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

Este proyecto ha sido desarrollado con la asistencia de:
- ChatGPT 4.0 Omni
- Claude 3.5 Sonnet

Un agradecimiento especial a estas herramientas de IA por su ayuda en la generación y optimización del código.

## 📞 Contacto

Si tienes alguna pregunta o sugerencia, no dudes en:
- Abrir un issue
- Enviar un pull request
- Contactar por correo: [kikegallego@kikegallego.com]

---
<div align="center">
Hecho con ❤️ por [KIGALDEV]

</div>