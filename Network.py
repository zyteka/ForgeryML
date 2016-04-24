﻿import math
import random
import string
import random
from datetime import datetime

random.seed(datetime.now())

def GetRandom(a, b):
    return (b - a) * random.random() + a

def Matrix(I, J, fill=0.0):
    m = []
    for i in range(I):
        m.append([fill] * J)
    return m

def Sigmoid(x):
    return math.tanh(x)

def SigmoidDerivative(x):
    return 1.0 - x ** 2

class Network:
    def __init__(self, numberInput, numberHidden, numberOutput):

        self.numberInput = numberInput + 1 
        self.numberHidden = numberHidden
        self.numberOutput = numberOutput

        self.activationInput = [1.0] * self.numberInput
        self.activationHidden = [1.0] * self.numberHidden
        self.activationOutput = [1.0] * self.numberOutput
        
        self.weightsInput = makeMatrix(self.numberInput, self.numberHidden)
        self.weightsOutput = makeMatrix(self.numberHidden, self.numberOutput)


        for i in range(self.numberInput):
            for j in range(self.numberHidden):
                self.weightsInput[i][j] = rand(-0.2, 0.2)

        for j in range(self.numberHidden):
            for k in range(self.numberOutput):
                self.weightsOutput[j][k] = rand(-2.0, 2.0)

        self.ci = makeMatrix(self.numberInput, self.numberHidden)
        self.co = makeMatrix(self.numberHidden, self.numberOutput)






    def Update(self, inputs):

        if len(inputs) != self.numberInput - 1:
            raise ValueError('Improper input size in network function: Update')

        for i in range(self.numberInput - 1):
            self.activationInput[i] = inputs[i]

        for j in range(self.numberHidden):
            sum = 0.0
            for i in range(self.numberInput):
                sum = sum + self.activationInput[i] * self.weightsInput[i][j]
            self.activationHidden[j] = Sigmoid(sum)

        for k in range(self.numberOutput):
            sum = 0.0
            for j in range(self.numberHidden):
                sum = sum + self.activationHidden[j] * self.weightsOutput[j][k]
            self.activationOutput[k] = Sigmoid(sum)

        return self.activationOutput[:]






    def BackPropagation(self, targetNodes, learningRate, momentum):
        if len(targetNodes) != self.numberOutput:
            raise ValueError('Improper target size in network function: BackPropagation')

        outputDeltaErrors = [0.0] * self.numberOutput
        for k in range(self.numberOutput):
            error = targetNodes[k] - self.activationOutput[k]
            outputDeltaErrors[k] = SigmoidDerivative(self.activationOutput[k]) * error

        hiddenDeltaErrors = [0.0] * self.numberHidden
        for j in range(self.numberHidden):
            error = 0.0
            for k in range(self.numberOutput):
                error = error + outputDeltaErrors[k] * self.weightsOutput[j][k]
            hiddenDeltaErrors[j] = SigmoidDerivative(self.activationHidden[j]) * error




        for j in range(self.numberHidden):
            for k in range(self.numberOutput):
                change = outputDeltaErrors[k] * self.activationHidden[j]
                self.weightsOutput[j][k] = self.weightsOutput[j][k] + learningRate * change + momentum * self.co[j][k]
                self.co[j][k] = change

        for i in range(self.numberInput):
            for j in range(self.numberHidden):
                change = hiddenDeltaErrors[j] * self.activationInput[i]
                self.weightsInput[i][j] = self.weightsInput[i][j] + learningRate * change + momentum * self.ci[i][j]
                self.ci[i][j] = change



        error = 0.0
        for k in range(len(targetNodes)):
            error = error + 0.5 * (targetNodes[k] - self.activationOutput[k]) ** 2
        return error







    def Test(self, inputSet):
        for p in inputSet:
            print(p[0], '->', self.Update(p[0]))






    def PrintWeights(self):
        print('Input weights:')
        for i in range(self.numberInput):
            print(self.weightsInput[i])
        print()
        print('Output weights:')
        for j in range(self.numberHidden):
            print(self.weightsOutput[j])








    def Train(self, inputSet, iterations=100, learningRate=0.5, momentum=0.1):

        for i in range(iterations):
            error = 0.0
            for p in inputSet:
                inputs = p[0]
                targetNodes = p[1]
                self.Update(inputs)
                error = error + self.BackPropagation(targetNodes, learningRate, momentum)
                print('error %-.5f' % error)