# extrator-de-frames

# Considerações importantes
   - O código foi implementado em 4 classes principais, sendo essas MessageProducer, MessageConsumer, FrameExtractor e FrameOperator, respectivamente. Além disso, foi implementada uma classe extra, denominada por VideoProcesing, a qual é responsável por reunir e executar todas as instâncias e operações necessárias para o integramento das demais classes.

# MessageProducer
   - Para esta classe, foi implementado o método "send_message", o qual é responsável por enviar à fila do RabbitMQ as informações do payload (arquivo json). No construtor da classe, observa-se a inicialização dos parâmetros com o nome da fila, caminho para o arquivo json, credenciais e instância da conexão utilizando o módulo pika do Python.

    Não há nada a ressaltar sobre detalhes de implementação.

# MessageConsumer
   - Uma vez que as informações foram populadas na fila do RabbitMQ de nome 'frameExtractorProperties', a classe MessageConsumer, executa os seus métodos. Para esta classe, foram implementados os métodos "callback", o qual é responsável por sempre que chegar uma mensagem nova na fila, executar todas as linhas de código dentro de seu escopo e, o método "consume", o qual tem o papel de inicializar o consumo das informações populadas e a serem populadas na fila do RabbitMQ, consumindo, uma por vez (prefetch_count=1).

   - É necessário ressaltar, que dentro do método "callback", é utilizado um método chamado "on_message_received" definido na classe VideoProcessing, o que provavelmente causa uma possível dependência circular no código, que não foi resolvida por questão de tempo. Para solucionar essa dependência circular, é necessário ter acesso aos valores de video_ref, frame_seconds_index e op_type dentro da classe VideoProcessing, sem a utilização de métodos dessa na classe MessageConsumer.

# FrameExtractor
   - A classe FrameExtractor é literalmente responsável por fazer a extração do frame do vídeo, a partir de x segundos passados por parâmetro (frame_seconds_index). Essa classe, contém o método "extract_frame", o qual é responsável por extrair o frame do vídeo, utilizando a biblioteca OpenCV. Houve modificações nesta parte em relação ao resultado apresentado na última daily, ou seja, foram implementadas melhorias no quesito leitura e escrita de frames em disco. Sendo assim, é possível analisar que há apenas uma leitura nesta etapa (leitura do vídeo em questão necessária para a extração do frame) e, não há salvamentos. Sendo assim, o frame é retornado e mantido em memória durante a execução do programa, pois as operações de leitura/escrita, são custosas e afetam diretamente no desempenho do programa.

# FrameOperator
   - A classe FrameOperator, contém um único método chamado "apply_operation", o qual é responsável por aplicar as operações de random_rotation, flip, noise e grayscale nos frames extraídos. É necessário ressaltar, que houve uma modificação na implementação da operação de random_rotation. Sendo assim, valem as considerações abaixo:
        
   -   height, width = frame.shape[:2] #retorna uma tupla com 3 itens, sendo esses altura, largura e canais de cores do frame (retorna 3 para RGB e 1 para imagens em escala de cinza)
    

   -   angle = random.randint(0, 180)
   -   matrix = cv2.getRotationMatrix2D((width/2, height/2), angle, 1) #gera uma matriz de rotação, o primeiro parâmetro é o centro, o segundo é o angulo gerado aleatóriamente entre 0 e 180 e, o último é a escala, se definirmos maior do que 1, a imagem terá o seu tamanho ampliado

   -   img = cv2.warpAffine(frame, matrix, (width,height)) #aplica a rotação ao frame

# VideoProcessing
   -   A última classe implementada foi a VideoProcessing. Ela contém os métodos "start", o qual inicia o produtor e consumidor do RabbitMQ e "on_message_received", o qual é executado a cada nova mensagem consumida. Este último método, extrai o frame e o armazena em frame e aplica as operações necessárias. Por fim, escreve o resultado na pasta Operations_Results com o nome de cada arquivo sendo gerado com um índice diferente e nome de arquivo diferente (são concatenados os nomes das operações aplicadas ao frame).

   -    Uma consideração importante, a imagem foi salva em PNG, visto que contém um maior número de detalhes. Nesse caso, não foi considerada a eficiência de se salvar em PNG, pois como o propósito é realizar o tratamento e a análise dessas imagens, foi admitido que é mais vantajoso um maior número de detalhes do que maior eficiência (poderia ser salva em JPEG).

# Limitações e possíveis melhorias no código
   -    Existem melhorias a serem realizadas no código, pensando na questão de escalabilidade. O principal ponto a ser analisado é trocar o programa de uma versão serial para uma versão paralela, distribuindo as tarefas às threads e utilizando todos os cores e capacidade de processamento. É muito mais vantajoso, em uma máquina multicore, utilizar todos os núcleos para extrair os frames das imagens e processá-los logo a seguir. 

   -    Os contras, são que provavelmente seria necessário lidar com problemas de sincronismo, para não serem aplicadas as operações até que os frames sejam/estejam salvos, evitando assim, condições de corrida e concorrência. 

   -    Obs.: Eu utilizaria para a implementação, a biblioteca Multiprocessing do Python.
