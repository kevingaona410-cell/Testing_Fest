¡Bienvenido de nuevo! ¿Recuerdas el challenge de la " Sock-it-to-me Chat"? Pues ahora es momento de llevarlo al siguiente nivel. Esta vez, vas a ponerte los guantes de tester para asegurarte de que todo funcione como un reloj suizo. ¿El servidor está listo para manejar conexiones múltiples? ¿Los mensajes llegan como deberían? Con este ejercicio, aprenderás a escribir pruebas que validen cada rincón de tu código, desde los detalles más pequeños hasta la interacción entre todos los componentes. ¡Prepárate para garantizar que tu chat sea tan robusto como una fortaleza digital!

Pruebas Unitarias
💡 Pruebas Unitarias 
Son pruebas que se centran en verificar si una pequeña parte específica de tu código (como una función o un método) funciona correctamente. Se prueban de manera aislada, sin depender de otras partes del sistema.

Identificar Funciones Críticas para Probar
Antes de comenzar a escribir pruebas, es importante identificar las partes del código que son más propensas a fallar o que son esenciales para el funcionamiento de la aplicación. En el caso de tu aplicación de chat en tiempo real.

🐧 Ejemplo:
Gestión de las conexiones de los clientes: Verificar que los clientes se conectan correctamente al servidor y que se gestionan de manera adecuada cuando se desconectan.
Manejo de errores: Asegurar que los errores comunes, como la pérdida de conexión o el envío fallido de un mensaje, se gestionen de manera adecuada.

Escribir Pruebas Unitarias para Cada Función
Crea pruebas unitarias utilizando la herramienta elegida según el lenguaje de programación utilizado ( Pytest, Jest, etc.)
Las pruebas unitarias deben abordar tanto los casos positivos como los negativos. 

Casos Positivos (happy path): Verificar que el sistema funcione correctamente bajo condiciones ideales. Por ejemplo, cuando se envía un mensaje válido, este debe ser aceptado y procesado sin problemas.
Casos Negativos: Probar escenarios en los que el sistema debería manejar entradas incorrectas o condiciones excepcionales. Por ejemplo, si se intenta enviar un mensaje vacío o demasiado largo, el sistema debe rechazarlo y devolver un error.
Cobertura Completa: Cada prueba debe enfocarse en un comportamiento específico. Al escribir pruebas unitarias, asegúrate de cubrir todas las posibles rutas de ejecución en la función, incluyendo los posibles errores.
Test-Driven Development - TDD
💡 Test-Driven Development (TDD)
Es un metodología de desarrollo en el que primero se escriben las pruebas antes de escribir el código que hará que esas pruebas pasen. Para ello se sigue un ciclo de tres pasos, es una metodología que te ayuda a crear código más confiable y bien estructurado desde el principio.

Primero, elige una funcionalidad específica que quieras añadir o mejorar en tu aplicación de chat. 

Por ejemplo, implementaremos la validación de mensajes para que no se envíen mensajes vacíos

Red (Escribir la Prueba y Verla Fallar): Primero, escribe la prueba para este comportamiento, sabiendo que aún no has implementado la funcionalidad. El objetivo aquí es que la prueba falle inicialmente.
Green (Escribir el Código para Hacer que la Prueba Pase): Ahora que la prueba falla (como se esperaba), escribe el código mínimo para hacerla pasar. Aquí no te preocupes por optimizar o hacerlo perfecto, solo busca que la prueba pase.
Refactor (Optimizar el Código): Con la prueba ahora pasando, revisa tu código para mejorarlo. Este es el momento de aplicar principios como DRY (Don't Repeat Yourself) y clean code para optimizar la solución sin alterar su funcionalidad.
Al aplicar TDD de esta manera, desarrollarás cada funcionalidad del programa de manera robusta y probada.

Pruebas de Integración
💡 Pruebas Integración
Estas pruebas validan que diferentes módulos o componentes de tu aplicación interactúan de manera correcta entre sí. Se enfocan en cómo se conectan las piezas, asegurando que cuando varios componentes funcionan juntos, lo hagan sin problemas.

Múltiples Conexiones
Implementa pruebas que simulen la conexión de múltiples clientes al servidor y verifica que los mensajes se distribuyan de manera adecuada entre ellos. 

Por ejemplo:

Los mensajes enviados por un cliente se reciben y retransmiten a todos los demás clientes conectados.
Probar cómo se comporta la aplicación con varios clientes enviando y recibiendo mensajes al mismo tiempo.
Asegurar que los mensajes no se pierdan ni se dupliquen durante la transmisión.
Verificación de que todos los clientes reciben los mensajes enviados en el orden correcto.
Manejo de Desconexiones Inesperadas y Errores de Red
Implementa pruebas que simulen la desconexión repentina de clientes mientras otros siguen enviando y recibiendo mensajes. Verifica que el servidor maneja estas situaciones sin bloquearse o lanzar errores inesperados y que los demás clientes no se ven afectados por la desconexión de un usuario.

Por ejemplo:

El servidor detecta cuando un cliente se desconecta y actualiza correctamente la lista de usuarios activos.
Los mensajes enviados por un cliente que se desconecta durante la transmisión no causan errores en el sistema.
El servidor sigue funcionando correctamente, incluso si varios clientes se desconectan de manera abrupta.
Resumen de Requerimientos
Requerimientos Obligatorios:
💡 Los requerimientos obligatorios deben ser completados en su totalidad o el ejercicio no se considera válido. 

Implementar pruebas unitarias para validar funciones críticas previamente definidas
Aplicar TDD para el desarrollo de al menos una funcionalidad, siguiendo el ciclo Red-Green-Refactor.
Implementar pruebas de integración que validen la interacción entre múltiples componentes (conexión de varios clientes al servidor, transmisión de mensajes, varios clientes enviando y recibiendo mensajes simultáneamente, que los mensajes no se pierdan ni se dupliquen, etc)
Implementar pruebas que simulen la desconexión repentina de uno o más clientes mientras otros siguen activos. Verificar que el servidor maneja estas situaciones sin bloqueos o errores inesperados y que los demás clientes no se ven afectados.
Asegurarse de que las pruebas cubren tanto casos positivos como negativos, incluyendo entradas inválidas y condiciones excepcionales.
Requerimientos Opcionales:
💡 Los requerimientos opcionales quedan a criterio del participante, su total y correcta implementación pueden influir en obtener una evaluación excepcional.

Realizar ajustes en el código base basado en los insights obtenidos durante las pruebas y demostrar mejoras de rendimiento o estabilidad.
Configurar un script o herramienta que ejecute todas tus pruebas con un solo comando
Implementa una herramienta de code coverage para asegurarte de que tus pruebas cubren la mayor cantidad posible del código. Intenta alcanzar al menos un 80% de cobertura, y si es posible, mejora el porcentaje de cobertura realizando pruebas adicionales. Presenta un informe con los resultados obtenidos.
Consideraciones para el ejercicio
💡 El objetivo de este ejercicio es que aprendas a desplegar y gestionar un servidor web desde cero, enfocándote en seguridad, configuración manual y buenas prácticas de administración para un entorno de producción.

No te preocupes si una prueba no sale bien en el primer intento. Haz ajustes pequeños, corre tus pruebas de nuevo y mejora tu código hasta que todo funcione como debería.
Asegúrate de que cada prueba pueda ejecutarse de forma independiente. Evita que el éxito o el fracaso de una prueba dependa de otra, ya que esto puede causar resultados engañosos.
Mantén un registro de las pruebas que realizas, los resultados que obtienes y las decisiones que tomas basadas en esos resultados.
Implementa la solución y luego optimizala:
Revisa tu aplicación de chat y asegúrate de tener el entorno listo para escribir y ejecutar pruebas.
Implementa pruebas unitarias para funciones clave como la validación de mensajes y la gestión de conexiones.
Aplica TDD para una funcionalidad específica: escribe la prueba, hazla pasar, y luego optimiza el código.
Simula múltiples clientes conectándose al servidor y verifica que los mensajes se envían y reciben correctamente.
Implementa pruebas para desconexiones inesperadas y errores comunes, asegurando que el sistema siga funcionando sin problemas.
Añade funcionalidades opcionales y documentación de los resultados.