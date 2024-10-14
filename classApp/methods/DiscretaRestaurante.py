# """
# # Resthru
# ## Restaurant QM Simulation

# ## Covers

# - Waiting for other processes
# - Resources: Resource

# ## Scenario

# A drive-thru restaurant has a specific number of counters
# and define a service processes that takes some (random) time.

# Customer process arrive at the restaurant at a random time.
# If the first counter is available, they start the service process
# and wait to finish. If not, they wait until they can use one.
# After finished, customer proceed to the next counter until
# all counters are passed.

# The complete service processes are:
# - order
# - pay
# - take
# """

# import os
# import sys
# import random
# import datetime
# import simpy

# global STATE, TEMP, SUM_ALL
# STATE = 0
# TEMP = 0
# SUM_ALL = 0.00
# CALC = [0] * 500  # Input capacity
# RANDOM_SEED = 42  # Random helper

# # Simulation time in minutes
# HOUR_OPEN = 7  # Morning
# HOUR_CLOSE = 23  # Night
# START = HOUR_OPEN * 60
# SIM_TIME = HOUR_CLOSE * 60

# print(START)
# print(SIM_TIME)

# SIM_FACTOR = 1 / 60  # Simulation realtime factor
# PEAK_START = 11
# PEAK_END = 13
# PEAK_TIME = 60 * (PEAK_END - PEAK_START)  # Range of peak hours

# NUM_COUNTERS = 1  # Number of counters in the drive-thru
# # Minutes it takes in each counters
# TIME_COUNTER_A = 2
# TIME_COUNTER_B = 1
# TIME_COUNTER_C = 3

# # Create a customer every [min, max] minutes
# CUSTOMER_RANGE_NORM = [5, 10]  # in normal hours
# CUSTOMER_RANGE_PEAK = [1, 5]  # in peak hours
# """
# Define clear screen function
# """


# def clear():
#     os.system(['clear', 'cls'][os.name == 'nt'])


# """
# Define exact clock format function
# """


# def toc(raw):
#     clock = ('%02d:%02d' % (raw / 60, raw % 60))
#     return clock


# """
# Waiting lane class
# """


# class waitingLane(object):

#     def __init__(self, env):
#         self.env = env
#         self.lane = simpy.Resource(env, 3)

#     def serve(self, cust):
#         yield self.env.timeout(0)
#         print("[w] (%s) %s entered the area" % (toc(env.now), cust))


# """
# First counter class
# """


# class counterFirst(object):

#     def __init__(self, env):
#         self.env = env
#         self.employee = simpy.Resource(env, 1)

#     def serve(self, cust):
#         yield self.env.timeout(
#             random.randint(TIME_COUNTER_A - 1, TIME_COUNTER_A + 1))
#         print("[?] (%s) %s ordered the menu" % (toc(env.now), cust))


# """
# Second counter class
# """


# class counterSecond(object):

#     def __init__(self, env):
#         self.env = env
#         self.employee = simpy.Resource(env, 1)

#     def serve(self, cust):
#         yield self.env.timeout(
#             random.randint(TIME_COUNTER_B - 1, TIME_COUNTER_B + 1))
#         print("[$] (%s) %s paid the order" % (toc(env.now), cust))


# """
# First+Second counter class
# """


# class counterFirstSecond(object):

#     def __init__(self, env):
#         self.env = env
#         self.employee = simpy.Resource(env, 1)

#     def serve(self, cust):
#         yield self.env.timeout(
#             random.randint(TIME_COUNTER_A - 1, TIME_COUNTER_A + 1))
#         print("[?] (%s) %s ordered the menu" % (toc(env.now), cust))

#         yield self.env.timeout(
#             random.randint(TIME_COUNTER_B - 1, TIME_COUNTER_B + 1))
#         print("[$] (%s) %s paid the order" % (toc(env.now), cust))


# """
# Third counter class
# """


# class counterThird(object):

#     def __init__(self, env):
#         self.env = env
#         self.employee = simpy.Resource(env, 1)

#     def serve(self, cust):
#         yield self.env.timeout(
#             random.randint(TIME_COUNTER_C - 1, TIME_COUNTER_C + 1))
#         print("[#] (%s) %s took the order" % (toc(env.now), cust))


# """
# The customer process (each customer has a name)
# arrives at the drive-thru lane, counter, then serviced by the empoyee (ce).
# It then starts the service process for each counters then leaves.
# """
# """
# (Type 2) Define customer behavior at first counter
# """


# def customer2A(env, name, wl, ce12, ce3):

#     with wl.lane.request() as request:

#         if (env.now >= SIM_TIME):
#             print("[!] Not enough time! %s cancelled" % name)
#             env.exit()

#         yield request
#         yield env.process(wl.serve(name))
#         print("[w] (%s) %s is in waiting lane" % (toc(env.now), name))

#     # Start the actual drive-thru process
#     print("[v] (%s) %s is in drive-thru counter" % (toc(env.now), name))

#     with ce12.employee.request() as request:

#         if (env.now + TIME_COUNTER_A + TIME_COUNTER_B >= SIM_TIME):
#             print("[!] Not enough time! Assumed %s is quickly finished" % name)
#             yield env.timeout(0.5)
#             env.exit()

#         yield request

#         CALC[int(name[5:])] = env.now
#         yield env.process(ce12.serve(name))
#         print("[?] (%s) %s choose the order" % (toc(env.now), name))

#         yield env.process(ce12.serve(name))
#         print("[$] (%s) %s is paying and will take the order" %
#               (toc(env.now), name))
#         env.process(customer2B(env, name, ce12, ce3))


# """
# (Type 2) Define customer behavior at second counter
# """


# def customer2B(env, name, ce12, ce3):

#     with ce3.employee.request() as request:

#         if (env.now + TIME_COUNTER_C >= SIM_TIME):
#             print("[!] Not enough time! Assumed %s is quickly finished" % name)
#             yield env.timeout(0.5)
#             env.exit()

#         yield request

#         yield env.process(ce3.serve(name))
#         print("[^] (%s) %s leaves" % (toc(env.now), name))

#         global TEMP
#         TEMP = int(name[5:])
#         CALC[int(name[5:])] = env.now - CALC[int(name[5:])]


# """
# (Type 3) Define customer behavior at first counter
# """


# def customer3A(env, name, wl, ce1, ce2, ce3):

#     with wl.lane.request() as request:

#         if (env.now >= SIM_TIME):
#             print("[!] Not enough time! %s cancelled" % name)
#             env.exit()

#         yield request
#         yield env.process(wl.serve(name))
#         print("[w] (%s) %s is in waiting lane" % (toc(env.now), name))

#     # Start the actual drive-thru process
#     print("[v] (%s) %s is in drive-thru counter" % (toc(env.now), name))

#     with ce1.employee.request() as request:

#         if (env.now + TIME_COUNTER_A >= SIM_TIME):
#             print("[!] Not enough time! Assumed %s is quickly finished" % name)
#             yield env.timeout(0.5)

#         yield request

#         CALC[int(name[5:])] = env.now
#         yield env.process(ce1.serve(name))
#         print("[?] (%s) %s choose the order" % (toc(env.now), name))

#         print("[2] (%s) %s will pay the order" % (toc(env.now), name))
#         env.process(customer3B(env, name, ce1, ce2, ce3))


# """
# (Type 3) Define customer behavior at second counter
# """


# def customer3B(env, name, ce1, ce2, ce3):

#     with ce2.employee.request() as request:

#         if (env.now + TIME_COUNTER_B >= SIM_TIME):
#             print("[!] Not enough time! Assumed %s is quickly finished" % name)
#             yield env.timeout(0.5)
#             env.exit()

#         yield request

#         yield env.process(ce2.serve(name))
#         print("[$] (%s) %s is paying the order" % (toc(env.now), name))

#         print("[3] (%s) %s will take the order" % (toc(env.now), name))
#         env.process(customer3C(env, name, ce1, ce2, ce3))


# """
# (Type 3) Define customer behavior at third counter
# """


# def customer3C(env, name, ce1, ce2, ce3):

#     with ce3.employee.request() as request:

#         if (env.now + TIME_COUNTER_C >= SIM_TIME):
#             print("[!] Not enough time! Assumed %s is quickly finished" % name)
#             yield env.timeout(0.5)
#             env.exit()

#         yield request

#         yield env.process(ce3.serve(name))
#         print("[^] (%s) %s leaves" % (toc(env.now), name))

#         global TEMP
#         TEMP = int(name[5:])
#         CALC[int(name[5:])] = env.now - CALC[int(name[5:])]


# """
# Define detail of 2 counters setup environment
# """


# def setup2(env, cr):
#     # Create all counters
#     wl = waitingLane(env)
#     ce12 = counterFirstSecond(env)
#     ce3 = counterThird(env)
#     i = 0

#     # Create more customers while the simulation is running
#     while True:
#         yield env.timeout(random.randint(*cr))
#         i += 1
#         env.process(customer2A(env, "Cust %d" % i, wl, ce12, ce3))


# """
# Define detail of 3 counters setup environment
# """


# def setup3(env, cr):
#     # Create all counters
#     wl = waitingLane(env)
#     ce1 = counterFirst(env)
#     ce2 = counterSecond(env)
#     ce3 = counterThird(env)
#     i = 0

#     # Create more customers while the simulation is running
#     while True:
#         yield env.timeout(random.randint(*cr))
#         i += 1
#         env.process(customer3A(env, "Cust %d" % i, wl, ce1, ce2, ce3))


# """
# Run the main program, execute via editor or terminal.
# """
# if __name__ == "__main__":

#     clear()
#     print("""
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >> Restaurant Queuing Model Simulation
# >> Drive-Thru Fast Food Restaurant Design Model Evaluation
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>""")

#     # Check if the number of counters is specified
#     if len(sys.argv) < 2:
#         nc = 3
#     else:
#         nc = int(sys.argv[1])

#     # random.seed(RANDOM_SEED) # Helps reproducing the results

#     # Has the environment in realtime (wall clock)
#     # env = simpy.RealtimeEnvironment(factor=SIM_FACTOR)

#     # Has the environment in manual step through
#     env = simpy.Environment(initial_time=START)
#     print("Environment created at %d!" % env.now)

#     # Decide the counter model setup
#     if nc == 2:
#         env.process(setup2(env, CUSTOMER_RANGE_NORM))
#     elif nc == 3:
#         env.process(setup3(env, CUSTOMER_RANGE_NORM))

#     print("Setup initialized!")

#     print("Start simulation!")
#     env.run(until=SIM_TIME)

#     for i in range(TEMP + 1):
#         SUM_ALL += CALC[i]

#     averageTimeService = SUM_ALL / (TEMP + 1)
#     servicePerSecond = 1.00 / (averageTimeService * 60)
#     servicePerMinute = servicePerSecond * 60

#     print("The end!")
#     print("[i] Model: %d counters" % nc)
#     print("[i] Average time:       %.4f" % averageTimeService)
#     print("[i] Service per minute: %f" % servicePerMinute)

#     # print(CALC)

import os
import random
import simpy

class DriveThruSimulation:
    def __init__(self, num_counters=3, random_seed=42, hour_open=7, hour_close=23, sim_factor=1/60, peak_start=11, peak_end=13, customer_range_norm=[5, 10], customer_range_peak=[1, 5]):
        self.num_counters = num_counters
        self.random_seed = random_seed
        self.hour_open = hour_open
        self.hour_close = hour_close
        self.sim_factor = sim_factor
        self.peak_start = peak_start
        self.peak_end = peak_end
        self.customer_range_norm = customer_range_norm
        self.customer_range_peak = customer_range_peak

        self.start = self.hour_open * 60
        self.sim_time = self.hour_close * 60
        self.peak_time = 60 * (self.peak_end - self.peak_start)
        self.time_counter_a = 2
        self.time_counter_b = 1
        self.time_counter_c = 3

        self.state = 0
        self.temp = 0
        self.sum_all = 0.00
        self.calc = [0] * 500

        random.seed(self.random_seed)

    def clear(self):
        os.system(['clear', 'cls'][os.name == 'nt'])

    def toc(self, raw):
        return '%02d:%02d' % (raw / 60, raw % 60)

    def run(self):
        self.clear()
        print("""
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
>> Restaurant Queuing Model Simulation
>> Drive-Thru Fast Food Restaurant Design Model Evaluation
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>""")

        env = simpy.Environment(initial_time=self.start)
        print("Environment created at %d!" % env.now)

        if self.num_counters == 2:
            env.process(self.setup2(env, self.customer_range_norm))
        elif self.num_counters == 3:
            env.process(self.setup3(env, self.customer_range_norm))

        print("Setup initialized!")
        print("Start simulation!")
        env.run(until=self.sim_time)

        for i in range(self.temp + 1):
            self.sum_all += self.calc[i]

        average_time_service = self.sum_all / (self.temp + 1)
        service_per_second = 1.00 / (average_time_service * 60)
        service_per_minute = service_per_second * 60

        print("The end!")
        print("[i] Model: %d counters" % self.num_counters)
        print("[i] Average time:       %.4f" % average_time_service)
        print("[i] Service per minute: %f" % service_per_minute)

    def setup2(self, env, cr):
        wl = self.WaitingLane(env)
        ce12 = self.CounterFirstSecond(env)
        ce3 = self.CounterThird(env)
        i = 0

        while True:
            yield env.timeout(random.randint(*cr))
            i += 1
            env.process(self.customer2A(env, "Cust %d" % i, wl, ce12, ce3))

    def setup3(self, env, cr):
        wl = self.WaitingLane(env)
        ce1 = self.CounterFirst(env)
        ce2 = self.CounterSecond(env)
        ce3 = self.CounterThird(env)
        i = 0

        while True:
            yield env.timeout(random.randint(*cr))
            i += 1
            env.process(self.customer3A(env, "Cust %d" % i, wl, ce1, ce2, ce3))

    class WaitingLane:
        def __init__(self, env):
            self.env = env
            self.lane = simpy.Resource(env, 3)

        def serve(self, cust):
            yield self.env.timeout(0)
            print("[w] (%s) %s entered the area" % (self.env.now, cust))

    class CounterFirst:
        def __init__(self, env):
            self.env = env
            self.employee = simpy.Resource(env, 1)

        def serve(self, cust):
            yield self.env.timeout(random.randint(1, 3))
            print("[?] (%s) %s ordered the menu" % (self.env.now, cust))

    class CounterSecond:
        def __init__(self, env):
            self.env = env
            self.employee = simpy.Resource(env, 1)

        def serve(self, cust):
            yield self.env.timeout(random.randint(1, 2))
            print("[$] (%s) %s paid the order" % (self.env.now, cust))

    class CounterFirstSecond:
        def __init__(self, env):
            self.env = env
            self.employee = simpy.Resource(env, 1)

        def serve(self, cust):
            yield self.env.timeout(random.randint(1, 3))
            print("[?] (%s) %s ordered the menu" % (self.env.now, cust))
            yield self.env.timeout(random.randint(1, 2))
            print("[$] (%s) %s paid the order" % (self.env.now, cust))

    class CounterThird:
        def __init__(self, env):
            self.env = env
            self.employee = simpy.Resource(env, 1)

        def serve(self, cust):
            yield self.env.timeout(random.randint(2, 4))
            print("[#] (%s) %s took the order" % (self.env.now, cust))

    def customer2A(self, env, name, wl, ce12, ce3):
        with wl.lane.request() as request:
            if env.now >= self.sim_time:
                print("[!] Not enough time! %s cancelled" % name)
                env.exit()

            yield request
            yield env.process(wl.serve(name))
            print("[w] (%s) %s is in waiting lane" % (self.toc(env.now), name))

        print("[v] (%s) %s is in drive-thru counter" % (self.toc(env.now), name))

        with ce12.employee.request() as request:
            if env.now + self.time_counter_a + self.time_counter_b >= self.sim_time:
                print("[!] Not enough time! Assumed %s is quickly finished" % name)
                yield env.timeout(0.5)
                env.exit()

            yield request

            self.calc[int(name[5:])] = env.now
            yield env.process(ce12.serve(name))
            print("[?] (%s) %s choose the order" % (self.toc(env.now), name))

            yield env.process(ce12.serve(name))
            print("[$] (%s) %s is paying and will take the order" % (self.toc(env.now), name))
            env.process(self.customer2B(env, name, ce12, ce3))

    def customer2B(self, env, name, ce12, ce3):
        with ce3.employee.request() as request:
            if env.now + self.time_counter_c >= self.sim_time:
                print("[!] Not enough time! Assumed %s is quickly finished" % name)
                yield env.timeout(0.5)
                env.exit()

            yield request

            yield env.process(ce3.serve(name))
            print("[^] (%s) %s leaves" % (self.toc(env.now), name))

            self.temp = int(name[5:])
            self.calc[int(name[5:])] = env.now - self.calc[int(name[5:])]

    def customer3A(self, env, name, wl, ce1, ce2, ce3):
        with wl.lane.request() as request:
            if env.now >= self.sim_time:
                print("[!] Not enough time! %s cancelled" % name)
                env.exit()

            yield request
            yield env.process(wl.serve(name))
            print("[w] (%s) %s is in waiting lane" % (self.toc(env.now), name))

        print("[v] (%s) %s is in drive-thru counter" % (self.toc(env.now), name))

        with ce1.employee.request() as request:
            if env.now + self.time_counter_a >= self.sim_time:
                print("[!] Not enough time! Assumed %s is quickly finished" % name)
                yield env.timeout(0.5)

            yield request

            self.calc[int(name[5:])] = env.now
            yield env.process(ce1.serve(name))
            print("[?] (%s) %s choose the order" % (self.toc(env.now), name))

            print("[2] (%s) %s will pay the order" % (self.toc(env.now), name))
            env.process(self.customer3B(env, name, ce1, ce2, ce3))

    def customer3B(self, env, name, ce1, ce2, ce3):
        with ce2.employee.request() as request:
            if env.now + self.time_counter_b >= self.sim_time:
                print("[!] Not enough time! Assumed %s is quickly finished" % name)
                yield env.timeout(0.5)
                env.exit()

            yield request

            yield env.process(ce2.serve(name))
            print("[$] (%s) %s is paying the order" % (self.toc(env.now), name))

            print("[3] (%s) %s will take the order" % (self.toc(env.now), name))
            env.process(self.customer3C(env, name, ce1, ce2, ce3))

    def customer3C(self, env, name, ce1, ce2, ce3):
        with ce3.employee.request() as request:
            if env.now + self.time_counter_c >= self.sim_time:
                print("[!] Not enough time! Assumed %s is quickly finished" % name)
                yield env.timeout(0.5)
                env.exit()

            yield request

            yield env.process(ce3.serve(name))
            print("[^] (%s) %s leaves" % (self.toc(env.now), name))

            self.temp = int(name[5:])
            self.calc[int(name[5:])] = env.now - self.calc[int(name[5:])]

if __name__ == "__main__":
    simulation = DriveThruSimulation(num_counters=3)
    simulation.run()