def read_file(folder, filename):
    from os import path
    file = open(path.join(folder, filename))
    return file.readlines()

class COSMO_Run:
    def __init__(self, folder, name, cosmolog="exe.log", slurmlog="cosmo_benchmark.out"):
        self.name = name
        self.timings = []
        if slurmlog:
            file = read_file(folder, slurmlog)
            self.timings.append(("total", COSMO_Run.get_slurm_timing(file)))
        if cosmolog:
            file = read_file(folder, cosmolog)
            benchmark = COSMO_Run.find_cosmo_benchmark(file)
            self.benchmark_metadata = benchmark
            for result in benchmark:
                tag = result["tag"]
                for val in ["min", "max", "mean"]:
                    idx = "{tag} {val}".format(tag=tag, val=val)
                    self.timings.append((idx, result[val]))

    def __str__(self):
        res = self.name
        pad = "\n    "
        for (k, v) in self.timings:
            res += pad
            res += "{k}: {v}s".format(k=k, v=v)
        return res

    @staticmethod
    def find_cosmo_benchmark(file, start=" END OF TIME STEPPING"):
        import re

        regex = re.compile(r'\s*(?P<id>\d+)\s+(?P<tag>\S+)\s+(?P<ncalls>\d+)\s+(?P<min>\d+\.*\d+)\s+(?P<max>\d+\.*\d+)\s+(?P<mean>\d+\.*\d+)')

        startpoint = not start
        matches = []
        for line in file:
            # Search for the startpoint
            if not startpoint:
                startpoint = line.startswith(start)
                # continue to next file if it is not found
                if not startpoint:
                    continue
            match = regex.match(line)
            if match:
                matches.append({
                    'id': match.group('id'),
                    'tag': match.group('tag'),
                    'ncalls': match.group('ncalls'),
                    'min': match.group('min'),
                    'max': match.group('max'),
                    'mean': match.group('mean')
                })
        return matches

    @staticmethod
    def parse_time(file, time_string="Start"):
        import re
        regex = re.compile(time_string+'\S*\s+(\d+)')
        for line in file:
            match = regex.search(line)
            if match:
                return match.group(1)

    @staticmethod
    def get_slurm_timing(file):
        start = COSMO_Run.parse_time(file, "Start")
        end = COSMO_Run.parse_time(file, "End")
        return float(end)-float(start)