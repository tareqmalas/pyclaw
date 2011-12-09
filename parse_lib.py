import numpy as np

def parse_output(file):
    corpus = file.readlines()

    fields = ('i','j','k','mstencil/s')
    results = []
    
    for l in corpus:
        if (l.find('Ni:') == 0):
            t = map(float,l.split()[1::2])
        #new or old style
        if (l.find('MStencil/s  MAX: ') == 0 or l.find('MStencil/s  : ') == 0):
            r = t[:]
            r.append(float(l.split()[2]))
            results.append(r)

    results = np.array(results)
    return results

def to_list(file):
    corpus = file.readlines()
    fields = ('kernel', 'cold start','jam_i','jam_j','ni','nj','nk','mstencil/s')
    results = []
    key_set = set()
    
    for l in corpus:
        if (l.find('[') == 0):
            kernel = l[1:].split()[0]
            (jam_i, jam_j) = map(float, l.split()[1].split('x'))
        if (l.find('Ni:') == 0):
            (ni,nj,nk) = map(float,l.split()[1::2])
        if (l.find('L3 flushed: ') == 0):
            cold_start = float(l.split()[2])            
        #new or old style
        if (l.find('MStencil/s  MAX: ') == 0 or l.find('MStencil/s  : ') == 0):
            mstencils = float(l.split()[2])
            key = (kernel, cold_start, jam_i, jam_j, ni, nj, nk)
            if key not in key_set:
                result = [kernel, cold_start, jam_i, jam_j, ni, nj, nk, mstencils]
                results.append(result)
                key_set.add(key)

    return results

def to_csv(results, file, head=('mode','kernel','cold_start','jam_i','jam_j','ni','nj','nk','mstencil/s')):
    import csv
    ow = csv.writer(file)
    ow.writerow(head)
    ow.writerows(results)

def from_csv(file):
    import csv
    ir = csv.reader(file)
    # skip header
    header = ir.next()
    results = list(ir)
    return results, header

def to_jam_arrays(results):
    jams = {}
    for r in results:
        jam = tuple(map(float,tuple(r[2:4])))
        if jam in jams:
            jams[jam]['n'].append(r[4:7])
            jams[jam]['mstencils'].append(r[7])
        else:
            jams[jam] = {}
            jams[jam]['n'] = [r[4:7]]
            jams[jam]['mstencils'] = [r[7]]

    return jams

def to_pickle(results, file):
    import pickle
    pickle.dump(results,file)
