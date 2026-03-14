import nest_asyncio
nest_asyncio.apply() #este codigo lo saque de un github, no es mas que dejar correr nested async en pynb

from llama_index.llms.ollama import Ollama #llama index sirve solo todo para conectar llms con tu rag
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.settings import Settings

llm = Ollama(model="DeepSeek-R1")
embedding = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

Settings.llm = llm #settings es util para no tener que establecer el mismo llm y embedding todo el rato
Settings.embed_model = embedding #puede salir un warning si tienes una version de pytorch que no coincide con tu gpu

from llama_index.core.workflow import Event 
from llama_index.core.schema import NodeWithScore

class RetrieverEvent(Event):
    nodes: list[NodeWithScore]


    
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.response_synthesizers import CompactAndRefine
from llama_index.core.workflow import (
    Context,
    Workflow,
    StartEvent,
    StopEvent,
    step,
)

#cabe mencionar que esta implementación es cuando quieres control total
class RAG(Workflow):
    def __init__(self,llm:str="DeepSeek-R1",embedding:str="BAAI/bge-small-en-v1.5"):
        super().__init__()
        self.llm = Ollama(model=llm)
        self.embedding = HuggingFaceEmbedding(model_name=embedding)

        Settings.llm = self.llm #settings es util para no tener que establecer el mismo llm y embedding todo el rato
        Settings.embed_model = self.embedding #puede salir un warning si tienes una version de pytorch que no coincide con tu gpu

        self.index = None
        
    @step 
    async def ingesta(self, contexto:Context, evento:StartEvent) -> StopEvent | None:
        directorio = evento.get('dirname')
        if not directorio:
            return None
        documentos = SimpleDirectoryReader(directorio).load_data() #lo hago en uno por ahorrarme pasos
        self.index = VectorStoreIndex.from_documents(documentos)
        return StopEvent(result=self.index)
    
    @step
    async def retrieve(self, contexto:Context, evento:StartEvent) -> RetrieverEvent | None:
        query = evento.get('query')
        indexacion = evento.get('index') or self.index
        if not query:
            return None
        
        await contexto.set('query',query)

        if not indexacion:
            print("No hay documentos")
            return None
        
        info = indexacion.as_retriever(similarity_top_k=2)
        nodos = await info.aretrieve(query)

        return RetrieverEvent(nodes=nodos)
    
    @step 
    async def sintetizar_info(self,contexto:Context, evento:RetrieverEvent) -> StopEvent:
        resumen = CompactAndRefine(streaming=True,verbose=True)
        info = await contexto.get('query')

        respuesta = await resumen.asynthesize(info, nodes = evento.nodes)

        return StopEvent(result=respuesta)
    
    #Para correrlo podemos hacer dos cosas, o meter dos llamadas run en el main o hacerlo mas bonito ahora
    async def ingesta_SOLUCION(self,directorio:str):
        resultado = await self.run(dirname=directorio)
        self.index = resultado
        return resultado
    
    async def query(self,query:str):
        if not self.index:
            return  ValueError("No hay RAG que valga la pena")
        
        respuesta = await self.run(query=query,index=self.index)
        return respuesta



#Para correrlo creamos archivo main

async def main():
    workflow = RAG()
    
    # Ingest documents
    await workflow.ingesta_SOLUCION("data")
    
    # Perform a query
    result = await workflow.query("¿Cómo se llama el chico del CV?")
    
    # Print the response
    async for chunk in result.async_response_gen():
        print(chunk, end="", flush=True)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 
    