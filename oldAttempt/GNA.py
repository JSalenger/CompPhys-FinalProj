import time
from WindowSingleton import WindowSingleton
from graphics import update
from constants import K
from V import V

class PopulateSorter:
    def __init__(self, id, populate):
        self.id = id
        self.populate = populate
        self.distances = {}

    def getScore(self, k, sortablePopulates):
        # cousins = []
        # l = list(self.distances.keys())

        # for i in range(k):
        #     try:
        #         id_of_closest_ball = int(l[i].replace(str(self.id), ""))
        #     except ValueError:
        #         cousins.append(self)
        #         continue
        #     for j in sortablePopulates:
        #         if j.id == id_of_closest_ball:
        #             cousins.append(j)
        
        # avgSore = (self.populate.getScore().m + sum([v.populate.getScore().m for v in cousins])) / (k + 1)

        # return avgSore
        return self.populate.getScore()



class GNA:
    def __init__(self, dt, familySizes, PopulateCLS, stdDev, callbacks=[], reverseScoring=False):
        # TODO: make pop size variable
        self.dt = dt
        self.totalTime = 0

        self.familySizes = familySizes
        self.PopulateCLS = PopulateCLS
        self.stdDev = stdDev
        self.callbacks = callbacks


        self.populates = []
        self.populationSize = sum(familySizes)
        self.populatesDead = 0

        self.reverseScoring = reverseScoring
        self.epoch = 0

        for _ in range(self.populationSize):
            p = self.PopulateCLS.createNew(self.dt)
            self.populates.append(p)

    def createNextGeneration(self):
        sortablePopulates = [PopulateSorter(k, v) for k, v in enumerate(self.populates)]

        sTime = time.time()

        for k, v in enumerate(sortablePopulates):
            v.id = k

        for j, v in enumerate(sortablePopulates):
            for i in sortablePopulates[j+1:]:
                # compute distances in remaining members
                # dist should be computed as the 6 dimensional vector that includes both velocity and position
                dist = v.populate.getDistanceFromSelfTo(i.populate)

                if v.id < i.id:
                    name = str(v.id) + str(i.id)
                    v.distances[name] = dist
                    i.distances[name] = dist
                else:
                    name = str(i.id) + str(v.id)
                    v.distances[name] = dist
                    i.distances[name] = dist
            
            v.distances = {k: v for k, v in sorted(v.distances.items(), key=lambda item: item[1].m)}

        # print("running time: " + str(time.time() - sTime))
        print("pre sort idx 0: " + str(sortablePopulates[0].getScore(K, sortablePopulates=sortablePopulates)))
        sortablePopulates.sort(
            key=lambda x: x.getScore(K, sortablePopulates), reverse=True)
        
        print("post sort idx 0: " + str(sortablePopulates[0].getScore(K, sortablePopulates=sortablePopulates)))
        print("-----")
        print("Epoch " + str(self.epoch) + " finished.")
        print("Average Loss: " + str(sum([i.getScore(K, sortablePopulates) for i in sortablePopulates])/len(sortablePopulates)))
        print("Best Loss: " + str(sortablePopulates[0].getScore(K, sortablePopulates)))
        print("Worst loss: " + str(sortablePopulates[-1].getScore(K, sortablePopulates)))
        print("Average Time: " + str(sum([i.populate.getStats()[0] for i in sortablePopulates])/len(sortablePopulates)))
        print("Best Time: " + str(sortablePopulates[0].populate.getStats()[0]))
        print("Worst Time: " + str(sortablePopulates[-1].populate.getStats()[0]))
        print("Average Distance: " + str(sum([i.populate.getStats()[1] for i in sortablePopulates])/len(sortablePopulates)))
        print("Best Distance: " + str(sortablePopulates[0].populate.getStats()[1]))
        print("Worst Distance: " + str(sortablePopulates[-1].populate.getStats()[1]))
        print("Average Avg Force: " + str(sum([i.populate.getStats()[2] for i in sortablePopulates])/len(sortablePopulates)))
        print("Best Avg Force: " + str(sortablePopulates[0].populate.getStats()[2]))
        print("Worst Avg Force: " + str(sortablePopulates[-1].populate.getStats()[2]))
        print("-----")
    



        tempPopulates = []
        for k, familySize in enumerate(self.familySizes, start=0):
            for _ in range(familySize):
                if k == 0:
                    tempPopulates.append(self.PopulateCLS.createFrom(sortablePopulates[k].populate, self.stdDev, color="red"))
                else:
                    tempPopulates.append(self.PopulateCLS.createFrom(sortablePopulates[k].populate, self.stdDev))


        self.epoch += 1
        self.populatesDead = 0

        for k in self.populates:
            k.undraw()

        self.populates = tempPopulates
 
    def __call__(self):
        for i in self.populates:
            died = i()  # could replace with just "if i()"
            if died:
                self.populatesDead += 1
                # print("Populates dead: " + str(self.populatesDead))

        if self.populatesDead == self.populationSize:
            self.createNextGeneration()
            for x in self.callbacks:
                x(self)

        self.totalTime += self.dt