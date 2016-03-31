
class State:
    def run(self, input):
        assert 0, "run not implemented"
    def next(self, input):
        assert 0, "next not implemented"

class StateMachine:
    def __init__(self, initialState):
        self.currentState = initialState
    def runAll(self, inputVector):
        for i in inputVector:
            self.currentState = self.currentState.next(i)
            self.currentState.run(i)


class TrellisDiagram(StateMachine):
    def __init__(self):
        StateMachine.__init__(self,TrellisDiagram.state0)
        self.possibleStates = [0,1,2,3]
        self.possibleInputs = [0,1]
        self.Tlookup= []
        self.states = []
        self.output = []
        self.populateTlookup()

    def populateTlookup(self):
        """[PreviousState,CurrentState,Input,Output]"""
        for state in self.possibleStates:
            self.setState(state)
            for input in self.possibleInputs:
                next = self.currentState.next(input)
                out = self.currentState.run(input)
                row = [state,next.getState(),input,out]
                self.Tlookup.append(row)
                self.setState(state)
        self.setState(0)

    def runAll(self, inputVector):
        self.states = []
        self.output = []
        for i in inputVector:
            self.output.append(self.currentState.run(i))
            self.currentState = self.currentState.next(i)
            self.states.append(self.currentState.getState())

    def setState(self,state):
        if state == 0:
            self.currentState = TrellisDiagram.state0
        if state == 1:
            self.currentState = TrellisDiagram.state1
        if state == 2:
            self.currentState = TrellisDiagram.state2
        if state == 3:
            self.currentState = TrellisDiagram.state3

    def checkTlookup(self,previousState,currentState,input,output):
        check = [previousState,currentState,input,output]
        if check in self.Tlookup:
            return 1
        else:
            return 0

    def getStates(self):
        return self.states
    def getOutput(self):
        return self.output

    def getPossibleOutputs(self):
        possOut = []
        for row in self.Tlookup:
            possOut.append(row[3])
        return possOut

    def getPossibleStates(self):
        return self.possibleStates
    def getPossibleInputs(self):
        return self.possibleInputs

class State0(State):
    def run(self, input):
        if input == 1:
            return [1,1,1]
        if input == 0:
            return [0,0,0]
    def next(self, input):
        if input == 1:
            return TrellisDiagram.state1
        if input == 0:
            return TrellisDiagram.state0
    def getState(self):
        return 0

class State1(State):
    def run(self, input):
        if input == 1:
            return [0,1,0]
        if input == 0:
            return [1,0,1]
    def next(self, input):
        if input == 1:
            return TrellisDiagram.state3
        if input == 0:
            return TrellisDiagram.state2
    def getState(self):
        return 1

class State2(State):
    def run(self,input):
        if input == 1:
            return [1,0,0]
        if input == 0:
            return [0,1,1]
    def next(self, input):
        if input == 1:
            return TrellisDiagram.state1
        if input == 0:
            return TrellisDiagram.state0
    def getState(self):
        return 2

class State3(State):
    def run(self,input):
        if input == 1:
            return [0,0,1]
        if input == 0:
            return [1,1,0]
    def next(self, input):
        if input == 1:
            return TrellisDiagram.state3
        if input == 0:
            return TrellisDiagram.state2
    def getState(self):
        return 3

TrellisDiagram.state0 = State0()
TrellisDiagram.state1 = State1()
TrellisDiagram.state2 = State2()
TrellisDiagram.state3 = State3()






