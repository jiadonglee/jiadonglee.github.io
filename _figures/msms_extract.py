import sys, numpy as np, h5py
F = '/Users/jdli/Project/data/MSMS/msms_36m_v0.hdf5'
cols = ['phot_g_mean_mag', 'parallax', 'bp_rp', 'E_binary', 'E_single', 'predicted_class', 'chi2_mass_mh',
        'chi2_mass_mh_binary', 'fit_status_single', 'fit_status_binary', 'm1_binary', 'mh_binary', 'q_binary',
        'flux_ratio_mean', 'flag_extrap_m2', 'mass_single', 'mh_single']
out = {'bin_g0': [], 'bin_br0': [], 'sin_g0': [], 'sin_br0': []}
with h5py.File(F, 'r') as f:
    g = f['table/columns']
    n = g['source_id/data'].shape[0]
    pc_null = g['predicted_class/null_bitmap'][:]
    valid_pc = np.unpackbits(pc_null, bitorder='little')[:n].astype(bool)
    step = 3_000_000
    for i0 in range(0, n, step):
        sl = slice(i0, min(n, i0 + step))
        d = {c: g[c + '/data'][sl] for c in cols}
        pc_ok = valid_pc[sl]
        mg = d['phot_g_mean_mag'] + 5 * np.log10(d['parallax']) - 10
        base = (d['parallax'] > 0) & (mg >= 4.5)
        fit_ok = (d['fit_status_single'] >= 2) | (d['fit_status_binary'] >= 2)
        lr = np.log10(d['chi2_mass_mh'] / d['chi2_mass_mh_binary'])
        gold = (base & fit_ok & pc_ok & (d['predicted_class'] == 1) & (lr > 0.2) & (d['m1_binary'] < 1.0)
                & (d['mh_binary'] > -1) & (d['E_binary'] < 0.2) & (d['q_binary'] > 0.9) & (d['q_binary'] <= 1.0)
                & (d['flux_ratio_mean'] >= 0.2) & (d['flux_ratio_mean'] <= 1.0) & (~d['flag_extrap_m2']))
        single = (base & pc_ok & (d['predicted_class'] == 0) & (d['fit_status_single'] >= 2)
                  & (d['mass_single'] < 1.0) & (d['mh_single'] > -1) & (d['E_single'] < 0.2))
        for key, m, E in (('bin', gold, d['E_binary']), ('sin', single, d['E_single'])):
            out[key + '_g0'].append((mg - 2.74 * E)[m].astype(np.float32))
            out[key + '_br0'].append((d['bp_rp'] - 1.339 * E)[m].astype(np.float32))
        print(i0, gold.sum(), single.sum(), flush=True)
np.savez(sys.argv[1], **{k: np.concatenate(v) for k, v in out.items()})
