# from langchain_community.document_loaders import PyMuPDFLoader
import os
import unicodedata
import re
# from nltk.corpus import stopwords


# class CleanText:
 
def clean_pdf(text):
   #  loader = PyMuPDFLoader(bronze_path + file_name)
   #  # here we have a class with metadata
   #  data = loader.load()
    
   #  elements = partition_pdf(file=io.BytesIO(data))
   #  print(elements)
    
   #  def medalion(text):
   #      print(text)
   #      return text
    
   #  text = [medalion(ele.text) for ele in elements]
   #  join_text = ["\n".join(text)] 
    
   #  print(join_text)
    
    # this way we get all the text of the pdf in just 1 string
   #  text = ''
   #  for i in range(len(data)):
   #      text = text + data[i].page_content

    # Normalize the text to separate accents from letters
    normalized_text = unicodedata.normalize('NFKD', text)
    
    # Remove accents by discarding non-ASCII characters
    text_without_accents = normalized_text.encode('ASCII', 'ignore').decode('utf-8')
    
    # Remove any special characters (keeping letters and numbers)
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', text_without_accents)

    # Convert the content to lowercase
    clean_text = clean_text.lower()

    stopwords_pt = [
      "a", "o", "e", "de", "em", "um", "para", "com", "nao", "uma", "os", "no", "se", "na", "por", "mais", "as", 
      "dos", "como", "mas", "foi", "ao", "ele", "das", "tem", "a", "seu", "sua", "ou", "ser", "quando", "muito", "ha", 
      "nos", "ja", "esta", "eu", "tambem", "so", "pelo", "pela", "ate", "isso", "ela", "entre", "depois", "sem", "mesmo", 
      "aos", "ter", "seus", "quem", "nas", "me", "esse", "eles", "estao", "voce", "tinha", "foram", "essa", "num", "nem", 
      "suas", "meu", "as", "minha", "tem", "numa", "pelos", "elas", "havia", "seja", "qual", "sera", "nos", "tenho", 
      "lhe", "deles", "essas", "esses", "pelas", "este", "dele", "tu", "te", "voces", "vos", "lhes", "meus", "minhas", 
      "teu", "tua", "teus", "tuas", "nosso", "nossa", "nossos", "nossas", "dela", "delas", "esta", "estes", "estas", 
      "aquele", "aquela", "aqueles", "aquelas", "isto", "aquilo", "estou", "esta", "estamos", "estao", "estive", "esteve", 
      "estivemos", "estiveram", "estava", "estavamos", "estavam", "estivera", "estiveramos", "esteja", "estejamos", 
      "estejam", "estivesse", "estivessemos", "estivessem", "estiver", "estivermos", "estiverem", "hei", "ha", "havemos", 
      "hao", "houve", "houvemos", "houveram", "houvera", "houveramos", "haja", "hajamos", "hajam", "houvesse", 
      "houvessemos", "houvessem", "houver", "houvermos", "houverem", "houverei", "houvera", "houveremos", "houverao", 
      "houveria", "houveriamos", "houveriam", "sou", "somos", "sao", "era", "eramos", "eram", "fui", "foi", "fomos", 
      "foram", "fora", "foramos", "seja", "sejamos", "sejam", "fosse", "fossemos", "fossem", "for", "formos", "forem", 
      "serei", "sera", "seremos", "serao", "seria", "seriamos", "seriam", "tenho", "tem", "temos", "tem", "tinha", 
      "tinhamos", "tinham", "tive", "teve", "tivemos", "tiveram", "tivera", "tiveramos", "tenha", "tenhamos", "tenham", 
      "tivesse", "tivessemos", "tivessem", "tiver", "tivermos", "tiverem", "terei", "tera", "teremos", "terao", "teria", 
      "teriamos", "teriam"
    ]

    words = clean_text.split()

    # Remove stopwords
    filtered_text = [word for word in words if word.lower() not in stopwords_pt]

    # Join the filtered words back into a string
    result = ' '.join(filtered_text)

    result = result.lower()
    return result