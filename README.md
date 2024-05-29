# PixelSafe
Esta es una aplicación de encriptación de imágenes y marcas de agua para el curso de *Criptografía*.

**Autores**
- Natalia Monroy Rosas
- David García Pardo
- Estevan Garcia Niño
- Diego Morales Granados

<div align="center">
    <img src="secretsafe_logo.png" alt="Texto alternativo" width="500" height="500"/>
</div>

## Instalación
Para instalar PixelSafe:
### 1. Descargar repositorio
Puede hacer esto descargando el archivo `.zip` de este repositorio
### 2. Crear ambiente virtual
Esto se hace para que las dependencias usadas por PixelSafe puedan funcionar correctamente y de manera segura. Primero nos movemos a el folder de gui:
```
  cd path/to/folder/gui
  ```
- Crear ambiente virtual
  ```
  python -m venv myenv
  ```
- Activar ambiente virtual
  ```
  source myenv/bin/activate
  ```
### 3. Instalar dependencias
En la carpeta del repositorio esta el archivo `requirements.txt` con la lista de todas las dependencias que usa PixelSafe. Estas pueden ser instaladas de esta manera:
```
pip install -r ../requirements.txt
```

### 4. Ejecutar PixelSafe
Hay que asegurarse de estar en la carpeta `gui` del proyecto. Luego, PixelSafe puede ser ejecutada de esta forma:
```
python main.py
```

---

Universidad Nacional de Colombia.
Departamento de Matemáticas 
2024
