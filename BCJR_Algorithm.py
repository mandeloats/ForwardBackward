from StateMachine import TrellisDiagram
import csv

class BCJR:
    def __init__(self, trellisDiagram):
        self.td = trellisDiagram
        self.states = self.td.getStates()
        self.observed = []
        self.omegas = []
        self.gammas = []
        self.alphas = []
        self.betas = []
        self.deltas = []
        self.possibleStates = self.td.getPossibleStates()
        self.possibleOutputs = self.td.getPossibleOutputs()
        self.possibleInputs = self.td.getPossibleInputs()
        self.length = 0
        self.channelProb = .2
        self.initialAlpha = [1,0,0,0]
        self.initialBeta = [1,0,0,0]


    def createGamma(self,observation):
        gamma = []
        for out in self.possibleOutputs:
            prob = 1
            for i in range(0, len(out)):
                if observation[i] == out[i]:
                    prob = (1-self.channelProb)*prob
                else:
                    prob = self.channelProb*prob
            gamma.append(prob)
        return gamma

    def populateGammas(self):
        for obs in self.observed:
            gamma = self.createGamma(obs)
            self.gammas.append(gamma)

    def createAlpha(self,prevAlpha,gamma):
        alpha = []
        for state in self.possibleStates:
            prob = 0
            for j in range(0,len(self.possibleStates)):#Si-1
                for input in self.possibleInputs:
                    for i in range(0, len(self.possibleOutputs)):
                        T= self.td.checkTlookup(self.possibleStates[j],state,input,self.possibleOutputs[i])
                        G = gamma[i]
                        A = prevAlpha[j]
                        prob = prob + T*G*A
            alpha.append(prob)
        return alpha

    def createBeta(self,prevBeta,gamma):
        beta = []
        for state in self.possibleStates:
            prob = 0
            for j in range(0,len(self.possibleStates)):#Si
                for input in self.possibleInputs:
                    for i in range(0, len(self.possibleOutputs)):
                        T= self.td.checkTlookup(state,self.possibleStates[j],input,self.possibleOutputs[i])
                        G = gamma[i]
                        B = prevBeta[j]
                        prob = prob + T*G*B
            beta.append(prob)
        return beta

    def createDelta(self,alpha,beta,gamma):
        delta = []
        for input in self.possibleInputs:
            prob = 0
            for curState in range(0,len(self.possibleStates)):
                for prevState in range(0,len(self.possibleStates)):
                    for i in range(0, len(self.possibleOutputs)):
                        T = self.td.checkTlookup(self.possibleStates[prevState],self.possibleStates[curState],input,self.possibleOutputs[i])
                        G = gamma[i]
                        A = alpha[prevState]
                        B = beta[curState]
                        prob = prob + T*A*B*G
            delta.append(prob)
        return delta

    def createOmega(self,alpha,beta,delta):
        omega = []
        for output in self.possibleOutputs:
            prob = 0
            for curState in range(0,len(self.possibleStates)):
                for prevState in range(0,len(self.possibleStates)):
                    for input in range(0,len(self.possibleInputs)):
                        T = self.td.checkTlookup(self.possibleStates[prevState],self.possibleStates[curState],input,output)
                        A = alpha[prevState]
                        B = beta[curState]
                        D = delta[input]
                        prob = prob + T*A*B*D
            omega.append(prob)
        return omega

    def forwardRecursion(self):
        prevAlpha = self.initialAlpha
        for i in range(0,self.length):
            alpha = self.createAlpha(prevAlpha,self.gammas[i])
            alpha = self.normalizeDistro(alpha)
            prevAlpha = alpha
            self.alphas.append(alpha)

    def backwardRecursion(self):
        prevBeta = self.initialBeta
        for i in range(0,self.length):
            beta = self.createBeta(prevBeta,self.gammas[self.length-1-i])
            beta = self.normalizeDistro(beta)
            prevBeta = beta
            self.betas.append(beta)
            self.betas.reverse()

    def populateDeltas(self):
        prevAlpha = self.initialAlpha
        beta = self.initialBeta
        for i in range(0,self.length):
            if i == self.length-1:
                beta = self.initialBeta
            else:
                beta = self.betas[i+1]
            gamma = self.gammas[i]
            delta = self.createDelta(prevAlpha,beta,gamma)
            delta = self.normalizeDistro(delta)
            self.deltas.append(delta)
            prevAlpha = self.alphas[i]

    def populateOmegas(self):
        prevAlpha = self.initialAlpha
        beta = self.initialBeta
        for i in range(0,self.length):
            if i == self.length-1:
                beta = self.initialBeta
            else:
                beta = self.betas[i+1]
            delta = self.deltas[i]
            omega = self.createOmega(prevAlpha,beta,delta)
            omega = self.normalizeDistro(omega)
            self.omegas.append(omega)
            prevAlpha = self.alphas[i]

    def normalizeDistro(self,distro):
        total = sum(distro)
        normalized = []
        for num in distro:
            normalized.append(num/total)
        return normalized

    def run(self,observed):
        self.observed = observed
        self.length = len(observed)
        self.populateGammas()
        self.forwardRecursion()
        self.backwardRecursion()
        self.populateDeltas()
        self.populateOmegas()

    def writeToFile(self):
        with open('Assignment3.csv','w') as csvfile:
            wr = csv.writer(csvfile)
            wr.writerow(["Deltas:"])
            wr.writerow(self.deltas)
            wr.writerow(["Omegas:"])
            wr.writerow(self.omegas)





class ChannelSimulation:

    def getChannelOutput(self,inputVector,bitPositions):
        position = 0
        outputVector = []
        for input in inputVector:
            output = []
            for bit in input:
                newBit = bit
                position = position + 1
                if position in bitPositions:
                    newBit = (bit+1)%2
                output.append(newBit)
            outputVector.append(output)
        return outputVector






td = TrellisDiagram()
input = [1,1,0,1,0,0,1,1,0,0]
td.runAll(input)
channel = ChannelSimulation()
flipBits = [3,6,7,9,25,27]
observed = channel.getChannelOutput(td.getOutput(),flipBits)
bcjr = BCJR(td)
bcjr.run(observed)

print("Alphas:")
print(bcjr.alphas)
print("Betas:")
print(bcjr.betas)
print("Deltas:")
print(bcjr.deltas)
print("Omegas:")
print(bcjr.omegas)

bcjr.writeToFile()

