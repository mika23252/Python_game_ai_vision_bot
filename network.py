import random
import pickle
import os.path


def lerp(a, b, t):
    return a + (b - a) * t


def save(data):
    with open('best_brain.pkl', 'wb') as f:
        pickle.dump(data, f)


def discard():
    if os.path.exists('best_brain.pkl'):
        os.remove('best_brain.pkl')


def mutate(network, amount=1):
    arr = [len(el.inputs) for el in network.levels]
    arr.append(len(network.levels[-1].outputs))
    newNetwork = Network(arr)

    for o in range(len(network.levels)):
        for i in range(len(network.levels[o].biases)):
            newNetwork.levels[o].biases[i] = lerp(network.levels[o].biases[i], random.random() * 2 - 1, amount)

        for i in range(len(network.levels[o].weights)):
            for j in range(len(network.levels[o].weights[i])):
                newNetwork.levels[o].weights[i][j] = lerp(network.levels[o].weights[i][j], random.random() * 2 - 1, amount)
    return newNetwork


class Network:
    def __init__(self, neuronCounts):
        self.levels = []
        for i in range(len(neuronCounts) - 1):
            self.levels.append(Level(neuronCounts[i], neuronCounts[i + 1]))

    def feedForward(self, givenInputs, network):
        outputs = feedForward(givenInputs, network.levels[0])

        for i in range(1, len(network.levels)):
            outputs = feedForward(outputs, network.levels[i])

        return outputs


def feedForward(givenInputs, level):
    for i in range(len(level.inputs)):
        level.inputs[i] = givenInputs[i]

    for i in range(len(level.outputs)):
        sum = 0
        for j in range(len(level.inputs)):
            sum += level.inputs[j] * level.weights[i][j]

        level.outputs[i] = 1 if sum > level.biases[i] else 0

    return level.outputs


class Level:
    def __init__(self, inputCount, outputCount):
        self.inputs = [0] * inputCount
        self.outputs = [0] * outputCount
        self.biases = [0] * outputCount

        self.weights = []
        for i in range(outputCount):
            a = []
            for j in range(inputCount):
                a.append(0)
            self.weights.append(a)

        self.__randomize()

    def __randomize(self):
        for i in range(len(self.inputs)):
            for j in range(len(self.outputs)):
                self.weights[j][i] = random.uniform(-1, 1)

        for i in range(len(self.biases)):
            self.biases[i] = random.uniform(-1, 1)
