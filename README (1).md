# 👤 UsuariosApp — CRUD con AWS y DynamoDB

> Aplicación web para gestión de usuarios con las cuatro operaciones CRUD completas, desplegada en la capa gratuita de AWS. Backend en **Python + Flask + boto3**, base de datos **Amazon DynamoDB**.

---

## 🏗️ Arquitectura del Sistema

```
┌──────────────────────────────────────────────────────────┐
│                        USUARIO                           │
│                    (Navegador Web)                       │
└────────────────────────┬─────────────────────────────────┘
                         │ HTTPS
                         ▼
┌──────────────────────────────────────────────────────────┐
│               AWS — Capa Gratuita (us-east-2)            │
│                                                          │
│  ┌───────────────────────────────────────────────────┐   │
│  │        Elastic Beanstalk (EC2 t2.micro)           │   │
│  │                                                   │   │
│  │  ┌─────────────┐    ┌────────────────────────┐   │   │
│  │  │  Frontend   │    │  Backend               │   │   │
│  │  │ HTML/CSS/JS │───▶│  Python + Flask        │   │   │
│  │  │ Jinja2      │    │  boto3 (AWS SDK)       │   │   │
│  │  └─────────────┘    └───────────┬────────────┘   │   │
│  └─────────────────────────────────┼────────────────┘   │
│                                    │ boto3              │
│  ┌─────────────────────────────────▼────────────────┐   │
│  │              Amazon DynamoDB                      │   │
│  │           Tabla: Usuarios                         │   │
│  │           Partition Key: id (String)              │   │
│  │           Región: us-east-2 (Ohio)                │   │
│  └───────────────────────────────────────────────────┘   │
│                                                          │
│  ┌───────────────────────────────────────────────────┐   │
│  │              AWS IAM                              │   │
│  │   Usuario: Deivid                                 │   │
│  │   Política: Mínimo privilegio sobre tabla         │   │
│  └───────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

---

## ⚙️ Servicios AWS Utilizados (Capa Gratuita)

| Servicio | Uso | Límite gratuito |
|---|---|---|
| **Elastic Beanstalk** | Aloja la aplicación web | Gratis (usa EC2 gratuito) |
| **EC2 t2.micro** | Servidor de cómputo | 750 h/mes (12 meses) |
| **Amazon DynamoDB** | Base de datos NoSQL | 25 GB + 25 WCU/RCU/mes |
| **IAM** | Control de acceso | Siempre gratis |

---

## 🗄️ Diseño de la Tabla DynamoDB

**Nombre:** `Usuarios` · **Región:** `us-east-2` (Ohio)

| Atributo | Tipo | Rol |
|---|---|---|
| `id` | String | Partition Key |
| `nombre` | String | Atributo |
| `correo` | String | Atributo |

> **Decisión técnica:** Se usó `id` como Partition Key de tipo String para flexibilidad. No se requirió Sort Key para este caso de uso CRUD simple.

---

## 🚀 Pasos de Instalación y Despliegue

### Requisitos previos
- Python 3.8+
- pip
- Cuenta AWS con capa gratuita activa
- AWS CLI configurado

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/usuarios-app.git
cd usuarios-app
```

### 2. Instalar dependencias
```bash
pip install flask boto3
```

### 3. Crear la tabla DynamoDB
```bash
aws dynamodb create-table \
  --table-name Usuarios \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-2
```

### 4. Ejecutar localmente
```bash
python app.py
```
Abrir en el navegador: `http://127.0.0.1:5000`

### 5. Desplegar en Elastic Beanstalk
```bash
pip install awsebcli
eb init usuarios-app --platform python-3.8 --region us-east-2
eb create usuarios-env --instance-type t2.micro
eb deploy
eb open
```

---

## 🔄 Operaciones CRUD Implementadas

### ➕ CREATE — `POST /guardar`
Registra un nuevo usuario en DynamoDB. Valida que id, nombre y correo estén completos y que el correo tenga formato válido antes de guardar.

### 📋 READ — `GET /`
Lista todos los usuarios de la tabla. Incluye búsqueda en tiempo real por nombre o correo desde el frontend.

### ✏️ UPDATE — `GET /editar/<id>` + `POST /actualizar`
Carga el formulario con los datos pre-cargados del usuario. Actualiza nombre y correo en DynamoDB manteniendo el mismo id.

### 🗑️ DELETE — `GET /eliminar/<id>`
Elimina el usuario con confirmación explícita mediante modal antes de ejecutar la acción.

---

## 🔐 Seguridad

- HTTPS habilitado en Elastic Beanstalk
- IAM usuario Deivid con política de mínimo privilegio
- Sin credenciales hardcodeadas en el código fuente
- Validación de inputs en frontend y backend
- Confirmación explícita antes de eliminar

---

## 🛠️ Manejo de Errores

| Situación | Comportamiento |
|---|---|
| Campo vacío | Mensaje de error inline en el formulario |
| Correo inválido | Mensaje de error específico en el campo |
| Error en DynamoDB | Mensaje de error al usuario |
| Cancelar eliminación | Modal se cierra, no se realiza ninguna acción |

---

## 📁 Estructura del Proyecto

```
usuarios-app/
├── templates/
│   ├── index.html       # Vista principal — READ + CREATE
│   └── editar.html      # Vista edición — UPDATE
├── app.py               # Backend Flask + boto3
└── README.md
```

---

## 💡 Decisiones Técnicas

| Decisión | Justificación |
|---|---|
| **Python + Flask** | Ligero, fácil de desplegar, compatible con Elastic Beanstalk |
| **boto3** | SDK oficial de AWS para Python; integración directa con DynamoDB |
| **DynamoDB** | Serverless, sin servidor que administrar, ideal para capa gratuita |
| **PAY_PER_REQUEST** | Se mantiene dentro del límite gratuito sin calcular capacidad |
| **Jinja2 templates** | Renderizado en servidor; sin necesidad de API REST separada |

---

## 👥 Equipo

| Integrante | Responsabilidad |
|---|---|
| Persona 1 | Cuenta AWS, DynamoDB, IAM, despliegue |
| Persona 2 | Backend Python/Flask, lógica CRUD, conexión boto3 |
| Persona 3 | Frontend, documentación técnica, sustentación |

---

## 📎 Entregables

- 🔗 **URL de la app:** *(pendiente — Persona 1)*
- 💾 **Repositorio:** `https://github.com/tu-usuario/usuarios-app`
- 📄 **Documentación:** Este README

---
*Actividad Práctica — 30% de la nota final | AWS Capa Gratuita + Amazon DynamoDB*
