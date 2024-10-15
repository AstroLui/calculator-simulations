import os
import random
import simpy
import io
import sys

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
    
    def run_with_output_capture(self):
        # Redirect stdout to capture print statements
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        try:
            self.run()
        finally:
            # Restore stdout
            sys.stdout = old_stdout
        return buffer.getvalue()

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
                return

            yield request
            yield env.process(wl.serve(name))
            print("[w] (%s) %s is in waiting lane" % (self.toc(env.now), name))

        print("[v] (%s) %s is in drive-thru counter" % (self.toc(env.now), name))

        with ce12.employee.request() as request:
            if env.now + self.time_counter_a + self.time_counter_b >= self.sim_time:
                print("[!] Not enough time! Assumed %s is quickly finished" % name)
                yield env.timeout(0.5)
                return

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
                return

            yield request

            yield env.process(ce3.serve(name))
            print("[^] (%s) %s leaves" % (self.toc(env.now), name))

            self.temp = int(name[5:])
            self.calc[int(name[5:])] = env.now - self.calc[int(name[5:])]

    def customer3A(self, env, name, wl, ce1, ce2, ce3):
        with wl.lane.request() as request:
            if env.now >= self.sim_time:
                print("[!] Not enough time! %s cancelled" % name)
                return

            yield request
            yield env.process(wl.serve(name))
            print("[w] (%s) %s is in waiting lane" % (self.toc(env.now), name))

        print("[v] (%s) %s is in drive-thru counter" % (self.toc(env.now), name))

        with ce1.employee.request() as request:
            if env.now + self.time_counter_a >= self.sim_time:
                print("[!] Not enough time! Assumed %s is quickly finished" % name)
                yield env.timeout(0.5)
                return

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
                return

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
                return

            yield request

            yield env.process(ce3.serve(name))
            print("[^] (%s) %s leaves" % (self.toc(env.now), name))

            self.temp = int(name[5:])
            self.calc[int(name[5:])] = env.now - self.calc[int(name[5:])]

if __name__ == "__main__":
    simulation = DriveThruSimulation(num_counters=3)
    simulation.run()