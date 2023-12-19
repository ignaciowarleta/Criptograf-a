Manual de instalación

Para desarrollar los siguientes scripts de Python se ha hecho uso de la librería de criptografía Cryptography, en concreto, para la generación de claves RSA y la utilización de funciones hash en los ejemplos didácticos del protocolo de withdraw y de payment. También se ha hecho uso de la biblioteca matplotlib, para la representación de una gráfica en el script de coin signature. 

La instalación de dichas bibliotecas se llevaría a cabo ejecutando estos comandos en la terminal: 
	
	pip install matplotlib
	pip install cryptography

A continuación, se describen las implementaciones desarrolladas. Es importante destacar que estas implementaciones, aunque brindan una representación funcional, no alcanzan la complejidad real que caracterizaría a una implementación fiel de los protocolos.

Coin Signature

En primer lugar, se definen tres clases: Point, que representa un punto en una curva elíptica; Bank, que simboliza una entidad bancaria con la capacidad de generar claves públicas y privadas; User, que representa a un usuario del sistema y genera sus propias claves y Comercio, que representa un comercio capaz de recibir claves públicas y monedas.
El banco genera tres puntos aleatorios (P, P1, y P2) y un escalar z. Luego, calcula Q, Q1, y Q2 multiplicando cada punto por z. Los usuarios generan su par de claves, I y Q1, multiplicando un escalar u1 por P1 y P respectivamente. Además, generan otros puntos, como Q1 y Q2 actualizado con P2. El comercio puede recibir la clave pública del usuario y una moneda generada por este.
La visualización del sistema se realiza mediante la función visualize, que utiliza la librería Matplotlib para mostrar puntos y líneas conectando las claves públicas en un gráfico.
La generación de la moneda implica operaciones con puntos y la firma digital se realiza en la función generate_signature. Esta función utiliza una función de hash ficticia para obtener un valor h, genera dos puntos R y S, y devuelve una firma compuesta por estos puntos y un escalar y.
Finalmente, en la función principal main, se crean instancias del banco, usuario y comercio, se generan claves públicas y privadas, se crea una moneda y se realiza una visualización del sistema antes de que el comercio reciba la moneda y muestre sus componentes.

Un ejemplo de valores devueltos: 

Bank Public Keys:
Q: 61938 545454
Q1: 433566 646686
Q2: 600066 327006

User Public Keys:
I: 444232 661742
Q2: 613581 334371

Coin Generation:
C: 295921845 441277911
Comercio recibe moneda:
I: 444232 661742
Q2: 613581 334371
Signature:
C: 295921845 441277911
R: 127216123458 1120322635614
S: 607801933426260 906352371907476
y: 590

Gráfico generado:

<img width="506" alt="Captura de pantalla 2023-12-19 a las 17 42 07" src="https://github.com/ignaciowarleta/Criptograf-a/assets/100534029/53230e3e-4434-4ccf-8dd7-44da7415a4f3">


Puntos Azules (User Public Keys):
I: Punto correspondiente a la cuenta del usuario.
Puntos Rojos (Bank Public Keys):
Q: Clave pública permanente del banco.
Q1: Clave pública adicional del banco.
Q2: Clave pública adicional del banco.
Línea Negra:
Conectan las claves públicas entre sí y muestran las transacciones.
La línea desde Q hasta I representa la conexión entre la clave pública del banco y la cuenta del usuario.
Withdraw Protocol

Para el withdraw protocol se han desarrollado dos scripts diferentes. El primero, en la misma línea que el anterior, manteniéndose lo más fiel posible al documento. Por otro lado, el segundo ha sido desarrollado con una perspectiva más didáctica, con el objetivo de ser mostrado durante la presentación. Por ello, tan solo será descrito el primero.

Se definen, como en el código anterior, las clases: Point, Bank, User y Comercio.
El banco vuelve a generar tres puntos aleatorios (P, P1, y P2) y un escalar z. Luego, calcula Q, Q1, y Q2 multiplicando cada punto por z. Los usuarios generan de nuevo su par de claves, I y Q1, multiplicando un escalar u1 por P1 y P respectivamente. Además, generan otros puntos, como Q1 y Q2 actualizado con P2. 
El cuanto al protocolo de retiro (withdrawal_protocol), en su ejecución, el usuario comienza generando números aleatorios s, t1, y t2, que son empleados para calcular dos puntos en la curva elíptica: A y B. Posteriormente, se calcula un valor de hash (h) de los puntos A y B mediante la función de hash personalizada hash_function. El protocolo continúa con la generación de números aleatorios adicionales, incluyendo y, u, y v. Estos valores se utilizan para crear puntos R y S, que forman parte de la firma digital. Se realiza un proceso adicional de verificación de ciertos valores y, si la verificación tiene éxito, el usuario completa el retiro con éxito, proporcionando al comercio los componentes esenciales de la transacción.

Ejemplo de valores devueltos:

s: 121
t1: 950, t2: 820
A: (41694180, 48018850)
B: (1143370, 1103450)
h: 41884182142090337190489874051797915527044470672562159988635176832220534015757
y: 534
R: (274070406, 100532376)
S: (16633392780840, 19156543981300)
u: 747
v: 40
C: (33084546, 12135816)
r: 30196795919154061539108655509461626508019745438801614742493958456239001761372787
y_received: 12018324775823316492565244892765727350191858684643042667512595465583122701026369760
Retiro fallido.

S: Valor aleatorio que representa el secreto del usuario para el retiro de fondos
T1,t2: Valores aleatorios en el cálculo de B. B se compone de dos puntos, uno multiplicado por t1 y el otro por t2, ambos aleatorios.
A: Representa el punto A calculado como s*I, donde I es un punto derivado de la clave públca del usuario.
B: Es el punto B calculado como t1P1 + t2P2, donde P1 y P2 son puntos aleatorios generados por el banco.
H: Es el resultado de aplicar una función de hash a los puntos A y B. La función de hash se utiliza para garantizar la integridad y autenticidad de los datos.
Y: Es un valor aleatorio que se utiliza en el cálculo de R y S
R: Representa el punto R calculado como yP
S: Represente el punto S calculado como yI
U: Valor aleatorio que se selecciona de manera que sea coprimo con z, donde z es un valor aleatorio generado por el banco durante su inicialización.
V: es un valor aleatorio utilizado en el cálculo de C y R
C: Representa el punto C calculamos como sQ, donde Q es un punto derivado de la clave pública del banco
R: Es el resultado de un cálculo que involucra la inversa modular de u y el valor hash de varios puntos
Y_received: Es el resultado de un cálculo que implica r, z (valor secreto del banco), y y.
Payment protocol

Al igual que con el protocolo withdraw, se han implementados dos versiones del protocolo de pago. Así que, de igual manera, únicamente se describe el primer script desarrollado.

En primer lugar, se define de nuevo la clase Point para representar un punto en una curva elíptica. Luego, la clase User se encarga de gestionar la interacción del usuario con el comercio. Al inicializarse, el usuario genera aleatoriamente parámetros como u1, s, t1, y t2 mediante el método generate_key_pair.
El usuario realiza un pago a través del método payment_protocol, donde se calcula un valor de hash (h0) que incluye puntos relevantes como A, B, el número de cuenta del comercio, y la fecha y hora de la transacción. Se generan valores intermedios (y1 y y2) y se verifica la relación entre estos y ciertos puntos, así como la autenticidad de una firma mediante los métodos verify_relation y verify_signature.
Por otro lado, la clase Comercio se inicializa con claves públicas aleatorias (P, P1, y P2), un número de cuenta y una fecha y hora simulada. La función deposit en Comercio simula un depósito cuando se invoca por parte del usuario, activando el protocolo de pago del usuario.
En la función principal, se crea una instancia de Comercio y un usuario asociado a dicho comercio. Se simula un pago generando puntos aleatorios (A, B, C, R, S) y un escalar y, y luego el comercio realiza un depósito invocando el protocolo de pago del usuario. 

Ejemplo de resultado: 

Valores obtenidos durante la ejecución:
h0: 112794155742570700121886426453922534893550298892827295091099508937882518041104
y1: 41673831133896111432633134209077851122050241831335115062718353368261578175610613521
y2: 105236947307818463213720035881509725055682428867007866319995841839044389332350945
Pago rechazado.
El hecho de que el mensaje final sea «Pago rechazado» indica que la verificación de la relación entre y1, y2, y otros valores, así como la verificación de la firma digital, no se cumple.

