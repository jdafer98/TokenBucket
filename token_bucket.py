

class TokenBucket:
    def __init__(self,maxc=4000,pps=100,tgr=(2000,1)):
         self.max_capacity = maxc #Máxima capacidad del cubo. Cada testigo representa un byte
         self.current_tokens = maxc/2 #Tokens actuales en el cubo
         self.current_tokens2 = 0 #Tokens en el segundo cubo
         self.time = 0 #La instancia de TokenBucket lleva la cuenta de un tiempo ficticio
         self.packets_per_second = pps #cada iteración se aumenta en tick_size unidades la variable time para representar el paso del tiempo
         self.token_generation_rate = tgr #Tupla que representa (cuantos_tokens,a_que_frecuencia) se generan en el cubo. 
         self.last_fill = 0 #ultima vez que se llenó el cubo
         self.pattern = [] #patrón que representa una secuencia de paquetes que llegan al cubo. Son túplas (n paquetes, x capacidad)
         self.result = [] #Lista con los resultados. Cada valor de la lista result es una n-upla con valores relevantes para su posterior representación. Status puede ser '0' enviado o '1' descartado/atrasado
         self.q = []
         self.mode = 3 # 1: Policing, 2: Shaping, 3: Dual_Token_Bucket con Policing-->Shaping.

    def tick(self):
        self.time = self.time + 1

    def set_pattern(self,p):
        self.pattern = p

    def fill(self):
        self.current_tokens = self.current_tokens + self.token_generation_rate[0]
        
        if self.current_tokens > self.max_capacity:
            diff = self.current_tokens - self.max_capacity
            self.current_tokens = self.max_capacity

            if self.mode == 3:
                self.current_tokens2 = self.current_tokens2 + diff
                if self.current_tokens2 > self.max_capacity:
                    self.current_tokens2 = self.max_capacity

        self.last_fill = self.time

    def check_fill(self):
        has_been_filled = False

        if self.last_fill + self.token_generation_rate[1] <= self.time:
            self.fill()
            has_been_filled = True

        return has_been_filled

    def send(self,bytess):
        status_code = 0
        byte_count = 0

        if bytess <= self.current_tokens:
            self.current_tokens = self.current_tokens - bytess
            byte_count = byte_count + bytess

            if self.mode == 2:
                done = False

                while not done:
                    if self.q != []:
                        if self.q[-1] <= self.current_tokens:
                            b = self.q.pop()
                            self.current_tokens = self.current_tokens - b
                            byte_count = byte_count + b
                        else:
                            done = True
                    else: done = True
 
        else:
            if self.mode == 3:
                if bytess <= self.current_tokens2:
                    self.current_tokens2 = self.current_tokens2 - bytess
                    byte_count = byte_count + bytess


                done = False

                while not done:
                    if self.q != []:
                        if self.q[-1] <= self.current_tokens2:
                            b = self.q.pop()
                            self.current_tokens = self.current_tokens2 - b
                            byte_count = byte_count + b
                        else:
                            done = True
                    else: done = True
                
                else:
                    status_code = 2
                    byte_cont = bytess

            else:
                #Policing (Solo dropeas el paquete)
                status_code = 1
                byte_count = bytess

        return (status_code,byte_count)

    def begin(self):
        print("START!")
        self.time = 0
        self.last_fill = 0
        self.result = []
        self.result.append((0,0,self.current_tokens,0,False,0))
        self.tick()
        pins = 0 #packets in a second. Lleva la cuenta de los paquetes que se han enviado en el segundo actual
        mbins = 0 #megabytes in a second. Lleva la cuenta de los MB en el segundo actual.
        discarted_delayed = 0
        totalins = 0 #total Bytes in a second

        for p in self.pattern:
            for i in range(p[0]):
                status = self.send(p[1])
                pins = pins + 1
                if status[0] == 0:
                    mbins = mbins + status[1]
                elif (status[0] == 1 and self.mode == 1) or (status[0] == 1 and self.mode == 2) or (status[0] == 2 and self.mode == 3):
                    discarted_delayed = discarted_delayed + status[1]
                    if self.mode == 2:
                        self.q.append(status[1])

                totalins = totalins + p[1]

                if pins == self.packets_per_second:
                    self.tick()
                    has_been_filled = self.check_fill()
                    self.result.append((mbins,discarted_delayed,self.current_tokens,totalins,has_been_filled,self.current_tokens2))
                    mbins = 0
                    pins = 0
                    discarted_delayed = 0
                    totalins = 0
