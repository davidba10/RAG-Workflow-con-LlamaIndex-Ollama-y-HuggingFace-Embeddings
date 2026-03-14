# RAG Workflow con LlamaIndex, Ollama y HuggingFace Embeddings

Este proyecto implementa un sistema **RAG (Retrieval-Augmented Generation)** usando **LlamaIndex Workflows**.

El objetivo es construir un pipeline RAG **modular y controlable**, separando claramente las fases de:

1. Ingesta de documentos  
2. Recuperación de información relevante  
3. Generación de respuestas usando un modelo de lenguaje  

El sistema permite crear **asistentes de conocimiento locales** capaces de responder preguntas basándose en documentos propios.

---

# Tecnologías utilizadas

- **LlamaIndex** → orquestación del pipeline RAG  
- **Ollama** → ejecución local del modelo de lenguaje  
- **HuggingFace Embeddings** → generación de embeddings  
- **Python** → implementación del sistema  
- **nest_asyncio** → compatibilidad con entornos async como notebooks  

---

# Arquitectura del sistema

El flujo completo del sistema sigue la arquitectura típica de un sistema RAG:

```
User Query
↓
Embedding de la consulta
↓
Vector Search (VectorStoreIndex)
↓
Top-K documentos relevantes
↓
LLM (DeepSeek-R1)
↓
Respuesta final
```

Este enfoque permite combinar:

- **búsqueda semántica**
- **generación de texto**
- **razonamiento contextual**

---

# Arquitectura del Workflow

El proyecto implementa un **workflow basado en eventos** utilizando `Workflow` de LlamaIndex.

Componentes principales:

### RetrieverEvent
Evento intermedio que transporta los nodos recuperados desde la fase de retrieval hacia la fase de síntesis.

### Clase RAG

Clase principal del workflow que implementa todo el pipeline.

Métodos principales:

- **ingesta()**  
  Carga documentos y construye el índice vectorial.

- **retrieve()**  
  Recupera los fragmentos más relevantes para la consulta.

- **sintetizar_info()**  
  Genera la respuesta final usando el LLM.

- **ingesta_SOLUCION()**  
  Helper para ejecutar la ingesta fácilmente.

- **query()**  
  Ejecuta el pipeline completo para una consulta.

---

# Flujo del sistema

## 1 Ingesta

Los documentos se cargan desde un directorio local usando:

```
SimpleDirectoryReader
```

Después se crea un índice vectorial:

```
VectorStoreIndex
```

Cada documento se convierte en **fragmentos embebidos** dentro del espacio vectorial.

---

## 2 Retrieval

Cuando el usuario hace una consulta:

1. se genera el embedding de la query
2. se busca en el índice vectorial
3. se recuperan los nodos más similares

Configuración actual:

```
similarity_top_k = 2
```

---

## 3 Síntesis

Los nodos recuperados se envían al sintetizador:

```
CompactAndRefine
```

El LLM utiliza estos nodos como **contexto** para generar la respuesta final.

---

# Estructura del proyecto

```
.
├── myfirstrag.py
├── data/
│   └── documentos de ejemplo
└── README.md
```

---

# Requisitos

Instalar dependencias:

```bash
pip install llama-index
pip install llama-index-llms-ollama
pip install llama-index-embeddings-huggingface
pip install nest_asyncio
```

También necesitas **Ollama instalado**.

---

# Descargar el modelo

Descargar el modelo utilizado:

```bash
ollama pull deepseek-r1
```

---

# Uso

Coloca tus documentos en un directorio:

```
data/
```

Luego ejecuta el script:

```bash
python myfirstrag.py
```

---

# Ejemplo de ejecución

El flujo principal realiza:

1. Crear una instancia de `RAG`
2. Ingestar los documentos
3. Ejecutar una consulta

Ejemplo de query:

```
¿Cómo se llama el chico del CV?
```

El sistema:

- recupera documentos relevantes
- usa el LLM para generar la respuesta
- imprime la respuesta en streaming

---

# Configuración actual

El sistema utiliza:

**LLM**

```
deepseek-r1
```

**Embedding model**

```
BAAI/bge-small-en-v1.5
```

Ambos se configuran en `Settings` y dentro de la clase `RAG`.

---

# Casos de uso

Este tipo de arquitectura RAG puede utilizarse para:

- asistentes sobre documentación interna
- chat con PDFs
- análisis automático de CVs
- motores de búsqueda semánticos
- copilotos empresariales
- sistemas de soporte técnico
- asistentes de investigación

---

# Posibles mejoras

Algunas extensiones interesantes para el proyecto:

- añadir soporte para múltiples documentos
- usar un vector database externo (Chroma, Weaviate, Qdrant)
- añadir memoria conversacional
- implementar ranking de documentos
- crear una interfaz web
- integrar streaming completo de respuestas

---

# Conclusión

Este proyecto demuestra cómo construir un sistema **RAG completo y modular** utilizando herramientas modernas de IA.

Separar claramente las fases de:

- ingesta
- retrieval
- generación

permite construir sistemas de **búsqueda semántica y asistentes inteligentes** capaces de trabajar con conocimiento personalizado.
