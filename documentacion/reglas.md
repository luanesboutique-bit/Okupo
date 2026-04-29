# 📜 Reglas del Proyecto y Contrato de Integración

Este documento establece el contrato oficial de colaboración entre **D'Mayoral** (Front-end: Okupo) y **D'Maria** (Back-end: Finite), definiendo la separación de responsabilidades y las normas de desarrollo.

## 🤝 Contrato de Integración (D'Mayoral <=> D'Maria)

1. **Separación de Responsabilidades**:
    - **D'Mayoral (Okupo)**: Responsable de la interfaz de usuario, experiencia de usuario (UX), y orquestación ligera de llamadas a la API.
    - **D'Maria (Finite)**: Responsable de la lógica de negocio pesada, persistencia de datos, seguridad a nivel de servidor y cumplimiento de la lógica de procesos.

2. **Sincronización de API**:
    - Ambos repositorios deben mantener un archivo `documentacion/api_uso.md` que refleje la realidad actual de los endpoints disponibles.
    - Si el Front-end (**D'Mayoral**) requiere una funcionalidad que aún no existe en el Back-end (**D'Maria**), debe seguir el **Protocolo de Adelantamiento**.

3. **Protocolo de Adelantamiento (Mocking)**:
    - El Front-end **no debe esperar** a que el Back-end termine un endpoint para avanzar.
    - Se debe crear un archivo de "plugin" o servicio de mock separado que responda a estas llamadas.
    - Este archivo debe ser fácilmente intercambiable mediante el cambio de una o dos variables de configuración (ej. `USAR_MOCKS = True`).
    - Se debe crear un archivo `documentacion/api_peticion.md` detallando exactamente qué necesita el Front-end para que el Back-end lo implemente.

4. **Desarrollo Cruzado**:
    - Los desarrolladores de D'Mayoral pueden bajar el motor de **Finite** para realizar cambios o pruebas, siempre documentando debidamente y siguiendo las reglas de D'Maria.

---

## 🛠️ Reglas de Desarrollo (Estándares finit)

Estas reglas son de cumplimiento obligatorio para todo el código dentro de este ecosistema:

1. **Idioma**: Todo el código (variables, funciones, comentarios, etc.) se escribe en **español**, a excepción de las palabras reservadas del lenguaje.
2. **Prohibición de la 'nn'**: La letra 'ñ' está estrictamente prohibida. Se debe usar **'nn'** como reemplazo (ej. `contrasenna`, `annio`).
3. **Sin Abreviaturas**: No se permiten abreviaciones de una sola palabra. Se debe usar el nombre completo para mayor claridad (ej. `usuario_id` en lugar de `uid`).
4. **Arquitectura Limpia**:
    - El código debe estar separado en capas (Infraestructura, Aplicación, Dominio, Web).
    - Bajo acoplamiento y alta cohesión.
    - Filosofía **KISS** (Keep It Simple, Stupid) y **DRY** (Don't Repeat Yourself).
5. **Genericidad**: Las funciones comunes deben ser genéricas y reutilizables.
6. **Seguimiento**: Consultar siempre estas reglas antes de cada cambio.
7. **Documentación Obligatoria**: No se considera "terminada" una tarea definitiva hasta que la documentación en `documentacion/` (`estructs.md`, `funciones.md`, `flujo.md`, etc.) esté actualizada.
8. **Filosofía DevOps**:
    - **Compilación Continua**: Todo cambio debe verificarse (`cargo check` para Rust, `compileall` para Python).
    - **Pruebas (Tests)**: Incluir tests de integración para funcionalidades de negocio o endpoints.
    - **Validación**: La tarea solo termina cuando los tests pasan con éxito.

---

## 🔄 Mantenimiento de Documentación
La documentación debe ser un reflejo fiel del código. Tras cada cambio "definitivo", es responsabilidad del desarrollador actualizar los archivos correspondientes en la carpeta `documentacion/`.
