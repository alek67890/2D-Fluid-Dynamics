# -*- coding: utf-8 -*-

import funkcje_testowe
import numpy as np


class Krok(funkcje_testowe.Step):

    def __init__(self, N, visc, diff, dt):
        funkcje_testowe.Step.__init__(self, N)
        self.size = (N + 2)
        self.u = np.zeros((self.size, self.size))
        self.v = np.zeros((self.size, self.size))
        self.dens = np.zeros((self.size, self.size))
        self.dens_prev = np.zeros((self.size, self.size))
        self.u_prev = np.zeros((self.size, self.size))
        self.v_prev = np.zeros((self.size, self.size))
        self.visc = visc
        self.diff = diff
        self.dt = dt
        self.bor = np.ones((self.size, self.size))
        self.fill_bor()

    def krok(self):
        self.u, self.v = self.vel_step( self.u, self.v, self.u_prev, self.v_prev, self.visc, self.dt)
        self.dens = self.dens_step( self.dens, self.dens_prev, self.u, self.v, self.diff, self.dt)
        d1 = self.dens[1 : self.N + 1, 1 : self.N + 1].sum()
        self.dens_prev = np.zeros((self.size, self.size))
        self.u_prev = np.zeros((self.size, self.size))
        self.v_prev = np.zeros((self.size, self.size))

        # more = (self.dens[1 : self.size, 1 : self.size] > 0.003) * 1
        # diffrence = (d1 - self.sum_dens)/(more.sum())
        # self.dens[1 : self.size, 1 : self.size] += more * - diffrence

        self.dens[1: self.N + 1, 1: self.N + 1] -= (d1 - self.sum_dens) * (self.dens[1 : self.N + 1, 1 : self.N + 1] / d1 *1.0)

        # v_prev[1:N + 1, 1:N + 1] = v_prev[1:N + 1, 1:N + 1] + 5 #proby grawitacja
        #print d1, self.dens.sum(), self.v.sum(), self.u.sum()
        return self.dens , self.u, self.v

    def krok2(self):
        self.u, self.v = self.vel_step2( self.u, self.v, self.u_prev, self.v_prev, self.visc, self.dt)
        self.dens = self.dens_step2( self.dens, self.dens_prev, self.u, self.v, self.diff, self.dt)
        d1 = self.dens[1 : self.N + 1, 1 : self.N + 1].sum()
        self.dens_prev = np.zeros((self.size, self.size))
        self.u_prev = np.zeros((self.size, self.size))
        self.v_prev = np.zeros((self.size, self.size))

        # more = (self.dens[1 : self.size, 1 : self.size] > 0.003) * 1
        # diffrence = (d1 - self.sum_dens)/(more.sum())
        # self.dens[1 : self.size, 1 : self.size] += more * - diffrence

        self.dens[1: self.N + 1, 1: self.N + 1] -= (d1 - self.sum_dens) * (self.dens[1 : self.N + 1, 1 : self.N + 1] / d1 *1.0)

        # v_prev[1:N + 1, 1:N + 1] = v_prev[1:N + 1, 1:N + 1] + 5 #proby grawitacja
        #print d1, self.dens.sum(), self.v.sum(), self.u.sum()
        return self.dens , self.u, self.v

    def sila_scenariusz_1(self):
        #self.v_prev[1: self.N + 1, 1: self.N + 1] = 0.1
        d1 = self.dens[1 : self.N + 1, 1 : self.N + 1].sum()
        self.v_prev[1: self.N + 1, 1: self.N + 1] = 0.15 * np.absolute(self.dens[1: self.N + 1, 1: self.N + 1])
        #for i in range(self.N):
            #for j in range(self.N):
                #if self.dens[i,j] > .05:
                    #self.v_prev[i, j] = .35 * self.dens[i,j]

    # def sila(self):
    #     self.v_prev[12:18, 32] = 45
    #     self.v_prev[46:52, 32] = -45
    #     self.u_prev[32, 12:18] = -45
    #     self.u_prev[32, 46:52] = 45

    def zalanie_scenariusz_1(self):
        self.dens[0:self.size, 0:self.size] = 0
        #self.dens[20:45 , 20 : 45] = 1
        self.dens[1:66 , 30 : 50] = 1
        #self.dens[5:60 , 5 : 45] = 1
        self.sum_dens = self.dens[1: self.N + 1, 1: self.N + 1].sum()

    def fill_bor(self):
        self.bor[:, 0] = 0
        self.bor[:, self.size-1] = 0
        self.bor[0, :] = 0
        self.bor[self.size - 1,:] = 0
        for i in range(self.size):
            self.bor[i,50] = 0
        self.bor[32,50] = 1
        #print(self.bor)


    def sila_scenariusz_2(self):
        self.v_prev[12:18, 32] = 45
        self.v_prev[46:52, 32] = -45
        self.u_prev[32, 12:18] = -45
        self.u_prev[32, 46:52] = 45

    def zalanie_scenariusz_2(self):
        self.dens[0:self.size, 0:self.size] = 0.4
        self.dens[20:45 , 20 : 45] = 1
        self.sum_dens = self.dens[1: self.N + 1, 1: self.N + 1].sum()

    def sila_scenariusz_3(self):
        self.radius = 4.0
        self.circle_step = 12.0
        for i in range (0,int(round(self.circle_step))):
            #promień- odległość siły od środka
            k = i / (self.circle_step+1.0)
            x = int(round(32.0 + np.cos(2.0*np.pi*k)*self.radius))
            y = int(round(32.0 + np.sin(2.0*np.pi*k)*self.radius))
            self.v_prev[x,y] = np.sin(2.0*np.pi*k)*250.0
            self.u_prev[x,y] = np.cos(2.0*np.pi*k)*250.0
            #print self.v_prev[x,y],  self.u_prev[x, y]


    def zalanie_scenariusz_3(self):
        self.dens[0:self.size, 0:self.size] = 0.4
        self.dens[20:45 , 20 : 45] = 0.7
        self.sum_dens = self.dens[1: self.N + 1, 1: self.N + 1].sum()

    def sila_scenariusz_4(self):
        d1 = self.dens[1 : self.N + 1, 1 : self.N + 1].sum()
        self.v_prev[1: self.N + 1, 1: self.N + 1] = 0.15 * np.absolute(self.dens[1: self.N + 1, 1: self.N + 1])
        self.u_prev[8, 0:self.size] = 30    # ustawienia sil
        self.u_prev[57, 0:self.size] = -30





    def zalanie_scenariusz_4(self):
        # self.dens[0:self.size, 0:self.size] = 0.4     # ustawienia wody
        self.dens[0:18, 0:self.size] = 0.4
        self.dens[48:self.size, 0:self.size] = 0.7
        #self.dens[20:45, 20: 45] = 1
        self.sum_dens = self.dens[1: self.N + 1, 1: self.N + 1].sum()
