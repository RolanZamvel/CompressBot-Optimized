# 🔁 Flujo Profesional de Desarrollo

Este es el flujo profesional y escalable que seguiremos para todas las peticiones, alineado con buenas prácticas de ingeniería de software.

---

## **1. Entender el contexto del proyecto**
Antes de escribir código:
- Revisa los **issues**, **proyectos** o **epics** asignados.
- Lee la documentación (`README.md`, `CONTRIBUTING.md`, etc.).
- Sincroniza con el equipo (reuniones, comentarios en issues, etc.).

---

## **2. Trabajar desde una rama aislada**
Nunca se trabaja directamente en `main` o `develop`.

```bash
git checkout main
git pull origin main
git checkout -b feat/nombre-descriptivo-del-cambio
```

> ✅ Usa nombres claros: `fix/login-error`, `feat/user-profile-api`, `refactor/db-connection`.

---

## **3. Desarrollar en iteraciones pequeñas y enfocadas**
- Cada commit debe resolver **una sola cosa**.
- Mensajes de commit claros y concisos (convencionales si aplica: `feat:`, `fix:`, `chore:`, etc.).
- Ejecuta pruebas locales antes de hacer push.

---

## **4. Subir cambios y crear un Pull Request (PR)**
```bash
git add .
git commit -m "feat: add user authentication endpoint"
git push origin feat/user-auth-endpoint
```

Luego en GitHub:
- Crea un **Pull Request** desde tu rama hacia `develop` (o `main`, según el flujo del equipo).
- Asigna revisores.
- Vincula el PR a un **issue** (usando keywords como `Closes #123`).

---

## **5. Revisión de código (Code Review)**
- Responde con respeto y apertura a los comentarios.
- No defiendas el código; busca la mejor solución.
- Si se piden cambios, haz nuevos commits (no reescribas el historial si ya hay revisión).

---

## **6. Integración continua (CI) y calidad**
- El PR debe pasar todas las pipelines: tests, linters, builds.
- Si falla algo, corrígelo localmente y sube los cambios.

---

## **7. Merge y limpieza**
Una vez aprobado:
- Usa **squash merge** (para features simples) o **merge commit** (para ramas complejas con historial valioso).
- Elimina la rama remota y local después del merge.

```bash
git checkout main
git pull origin main
git branch -d feat/user-auth-endpoint
```

---

## **8. Mantenimiento post-merge**
- Verifica en staging/producción si es necesario.
- Cierra issues relacionados si no se cerraron automáticamente.
- Documenta si el cambio lo requiere.

---

## 📋 **Convenciones de Commit**

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bugs
- `docs:` Cambios en documentación
- `style:` Formato, código limpio (sin cambios lógicos)
- `refactor:` Refactorización de código
- `test:` Añadir o modificar tests
- `chore:` Tareas de mantenimiento, dependencias, etc.

## 🎯 **Estado Actual del Proyecto**

**Proyecto**: CompressBot Optimized
**Repositorio**: https://github.com/RolanZamvel/CompressBot-Optimized
**Rama Principal**: main
**Última Tarea**: Testear ejecución del bot

---

*Este documento debe consultarse al inicio de cada petición para asegurar consistencia en el flujo de trabajo.*