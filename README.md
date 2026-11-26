# Achilata Salta · @achilatasalta

Este repositorio tiene **todo el proyecto**: el manual de marca, el logo, las fotos, y las piezas para Instagram. Es privado.

## Abrirlo en otra computadora

1. **Instalá Git:** [git-scm.com](https://git-scm.com).
2. **Descargá el proyecto.** En la carpeta donde lo quieras, abrí una terminal y corré:
   ```
   git clone https://github.com/lauticolquesosa/achilata-salta.git "Proyecto - Achilata"
   ```
   Te va a pedir que inicies sesión en GitHub.
3. **Instalá las fuentes.** Las de Bricolage Grotesque están en `06_Assets/fuentes/`: doble clic en cada una y después *Instalar*. Ink Free ya viene con Windows.
4. **Abrí la carpeta con Claude Code.** `CLAUDE.md` tiene todas las reglas del proyecto.
5. **Copiá la memoria de Claude,** si querés el mismo contexto que en la compu original.
   - Está en `.claude/memoria/`.
   - Va a `C:\Users\<usuario>\.claude\projects\<carpeta del proyecto>\memory\`.
   - El nombre de esa carpeta es la ruta del proyecto con guiones. Se crea la primera vez que abrís Claude Code ahí.

## Guardar los cambios y traerlos

**Para guardar cambios y subirlos:**
```
git add -A
git commit -m "lo que cambiaste"
git push
```

**Para traer lo último antes de trabajar:**
```
git pull
```

## Herramientas

Para los scripts de diseño y el PDF del perfil completo hacen falta:
```
pip install pymupdf pillow playwright
python -m playwright install chromium
```

Para editar fotos también se usan `opencv-python`, `numpy` y `rembg`.

## Estructura

| Carpeta | Qué hay |
|---|---|
| `01_Contexto` | El negocio, el producto, Salta, el público y la competencia |
| `02_Marca` | El manual de marca en Illustrator y PDF, y `logo.ai` con sus PNG |
| `03_Estrategia` | El sistema de contenido y el perfil de Instagram |
| `04_Contenido` | Las reglas, las publicaciones del feed P01 a P12, las historias H01 en adelante y las destacadas |
| `05_Referencias` | Las cuentas y las imágenes de referencia, y su análisis |
| `06_Assets` | Los logos, las tramas, el goteo, las fuentes y las fotos |
| `07_Pendientes.md` | Lo que falta confirmar |

## Uso y licencias
- **Código:** los scripts, de `06_Assets/fotos/herramientas/`, se pueden usar libremente bajo licencia MIT.
- **Marca:** el logo, el manual, las piezas y las fotos de Achilata Salta están para ver y aprender de ellos. El uso comercial de la marca no está permitido.
- **Referencias:** las capturas de `05_Referencias/` son de sus dueños y están solo como referencia.
- **Fuentes:** Bricolage Grotesque tiene licencia SIL Open Font License.
