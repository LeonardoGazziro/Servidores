class ServerRequests:

    def __init__(self):
        self.clock_ticks = 0
        self.task_info, self.servers = [], []
        self.ttask, self.umax = 0, 0
        self.input_end = False
        self.output = ''
        self.input_arq = None
        self.total = 0

    def _search_available_server(self):
        '''
        Varre os servidores para encontrar algum que esteja disponível
        :return: retorna o índice do servidor disponível, ou -1 caso não haja servidor disponível
        '''
        index = -1
        n_process = 0
        # percorre os servidores atuais
        for idx, server_process in enumerate(self.servers):
            # verifica se o servidor pode receber requisições
            if server_process < self.umax:
                if index == -1:
                    index = idx
                    n_process = server_process
                elif n_process == 0 and server_process > 0:
                    index = idx
                    n_process = server_process

        return index

    def _create_task(self):
        '''
        Cria o processo no servidor.
        :return: None
        '''
        # pega o servidor disponível
        available_server = self._search_available_server()
        '''
        Verifica se existe servidor disponível, senão inicia um novo servidor.
        Adiciona na lista de tarefas um dicionário com informações do termino da tarefa e o servidor em que está sendo 
        executada.
        '''
        if available_server >= 0:
            self.servers[available_server] += 1
            self.task_info.append({'end_task': (self.clock_ticks + self.ttask) -1, 'server': available_server})
        else:
            self.servers.append(1)
            self.task_info.append({'end_task': (self.clock_ticks + self.ttask) -1, 'server': len(self.servers) - 1})

    def _finish_task(self):
        '''
        Finaliza e elimina do servidor as tarefas que foram concluídas
        :return: None
        '''
        while len(self.task_info) > 0:
            # verifica se a primeira tarefa da lista terminou, se terminou, finaliza a tarefa e libera do servidor,
            # senão encerra o código.
            if self.task_info[0]['end_task'] < self.clock_ticks:
                self.servers[self.task_info[0]['server']] -= 1
                del(self.task_info[0])
            else:
                break

    def _receive_request(self):
        '''
        Processa as entradas e retorna o input e True caso as entradas tenham acabado.
        :return: Retorna o input e False quando houver input, se não houver input retorna None e True indicando que acabou.
        '''
        request = self.input_arq.readline()

        if request != '':
            return int(request), False
        else:
            self.input_arq.close()
            return None, True

    def _format_output(self, servers_list):
        '''
        Formata o texto de saída.
        :param servers_list: lista de servidores em uso.
        :return: retorna o texto com os servidores em uso.
        '''
        text = ''
        for server in servers_list:
            if server > 0:
                text = f'{text}, {str(server)}' if text != '' else f'{str(server)}'

        return text if text != '' else '0'

    def _ticks_cost(self, servers_list):
        total = 0
        for server in servers_list:
            if server > 0:
                total += 1

        return total

    def _create_output_file(self, output_text):
        '''
        Cria o arquivo de saída.
        :param output_text: texto a ser inserido no arquivo.
        :return: None
        '''
        output_file = open('output.txt', 'w+')
        output_file.writelines(output_text)
        output_file.write(str(self.total))
        output_file.close()

    def process_requests(self, input_path):
        self.input_arq = open(input_path, 'r')
        # primeira linha contem o valor de ttask
        self.ttask = int(self.input_arq.readline())
        # segunda linha contem o valor de umax
        self.umax = int(self.input_arq.readline())

        while True:
            self.clock_ticks += 1
            # verifica se há processos e então finaliza os processos concluídos
            if len(self.task_info) > 0:
                self._finish_task()

            # verifica se existe input
            if not self.input_end:
                # processa o input e distribui as requisições nos servidores.
                _input, self.input_end = self._receive_request()
                if not self.input_end and _input > 0:
                    for i in range(_input):
                        self._create_task()


            self.total += self._ticks_cost(self.servers)

            # salva o valor de saída
            self.output = self.output + f'{self._format_output(self.servers)} \n'

            # finaliza o processo quando não houver mais inputs e todas as tarefas estiverem concluídas
            if len(self.task_info) == 0 and self.input_end:
                break

        # cria o arquivo de saída
        self._create_output_file(self.output)
