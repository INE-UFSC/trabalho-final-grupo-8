""" Módulo para os algoritmos de ordenação """


from abc import ABC, abstractmethod


class Algorithm(ABC):
    """ Base de um algoritmo """

    def __init__(self, array: list):
        self.__original_array = array
        self.__current_array = array
        self.__done = False

    @property
    def original_array(self):
        """ O estado original do array """
        return self.__original_array

    @property
    def current_array(self):
        """ O estado atual do array """
        return self.__current_array

    @property
    def done(self):
        """ Se a ordenação já foi concluída """
        return self.__done

    @abstractmethod
    def one_step(self):
        """ Ordernar apenas um passo """


class Quicksort(Algorithm):
    def __init__(self, array: list):
        self.__original_array = array
        self.__current_array = array
        self.__h = len(self.__original_array)-1
        self.__l = 0
        self.__setup()

    def __setup(self):
        size = self.__h - self.__l + 1
        self.__stack = [0] * (size)
        self.__top = -1
        self.__top = self.__top + 1
        self.__stack[self.__top] = self.__l
        self.__top = self.__top + 1
        self.__stack[self.__top] = self.__h

    @property
    def done(self):
        return self.__top <= 0

    def __partition(self):
        i = (self.__l - 1)
        x = self.__current_array[self.__h]

        for j in range(self.__l, self.__h):
            if self.__current_array[j] <= x:

                # increment index of smaller element
                i = i+1
                self.__current_array[i], self.__current_array[j] = self.__current_array[j], self.__current_array[i]

        self.__current_array[i+1], self.__current_array[self.__h] = self.__current_array[self.__h], self.__current_array[i+1]
        return (i+1)

    def __aux(self):
        # Pop h and l
        self.__h = self.__stack[self.__top]
        self.__top = self.__top - 1
        self.__l = self.__stack[self.__top]
        self.__top = self.__top - 1

        # Set pivot element at its correct position in
        # sorted array
        p = self.__partition()

        # If there are elements on left side of pivot,
        # then push left side to stack
        if p-1 > self.__l:
            self.__top = self.__top + 1
            self.__stack[self.__top] = self.__l
            self.__top = self.__top + 1
            self.__stack[self.__top] = p - 1

        # If there are elements on right side of pivot,
        # then push right side to stack
        if p+1 < self.__h:
            self.__top = self.__top + 1
            self.__stack[self.__top] = p + 1
            self.__top = self.__top + 1
            self.__stack[self.__top] = self.__h
        self.__top = self.__top
        self.__stack = self.__stack

    # Function to do Quick sort
    # arr[] --> Array to be sorted,
    # l  --> Starting index,
    # h  --> Ending index
    def one_step(self):
        if self.__top >= 0:
            self.__aux()
