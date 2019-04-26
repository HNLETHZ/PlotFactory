import ROOT as rt
import pandas, root_numpy
import root_pandas


cut_l0ml2m    = 'l0_pt > 25 & l2_pt > 15 & l0_id_m & l2_id_m & l0_reliso_rho_03 < 0.15 & l2_reliso_rho_03 < 0.15'
cut_l0ml2m    += ' & l0_q * l2_q < 0 & l1_pt > 5'

l1_e_tight = 'l1_pt > 5 & l1_MediumNoIso & l1_reliso05 < 0.1 & abs(l1_dxy) > 0.05 & ' + l1_fake_e_dr
l1_e_lnt   = 'l1_pt > 5 & l1_LooseNoIso  & l1_reliso05 > 0.1 & abs(l1_dxy) > 0.05 & ' + l1_fake_e_dr #FIXME
l1_e_loose = 'l1_pt > 5 & l1_LooseNoIso  & abs(l1_dxy) > 0.05 & ' + l1_fake_e_dr

( ( (dataset['l0_gen_match_isDirectPromptTauDecayProductFinalState'] == 1)  |  (dataset['l0_gen_match_isDirectHardProcessTauDecayProductFinalState'] == 1)  |  (dataset['l0_gen_match_fromHardProcessFinalState'] == 1)  |  (dataset['l0_gen_match_isPromptFinalState'] == 1) ) & ( abs( (dataset['l0_gen_match_pdgid']) == 11)  | abs( (dataset['l0_gen_match_pdgid']) == 22)  )  &  ( sqrt( ( (dataset['l0_eta']-dataset['l0_gen_match_eta'])**2 + (' + dPhi00DS + ')**2 ) < 0.04 ) )

#dPhi00 = '( (FF(dataset['l0_phi']-dataset['l0_gen_match_phi'] + 2*pi) * (FF(dataset['l0_phi']-dataset['l0_gen_match_phi'] < -pi) + (FF(dataset['l0_phi']-dataset['l0_gen_match_phi'] - 2*pi) * (FF(dataset['l0_phi']-dataset['l0_gen_match_phi'] > pi) )' 

def skimTrees(ch,sample,treeDir,cut,START=0,STOP=1):

    treeFile = rt.TFile(treeDir+suffix) 
    tree     = treeFile.Get('tree')

    nevents = tree.GetEntries()
    aPop = 200000
    nslices = int(nevents/aPop) + 1
    print '\n\tnumber of slices:', nslices 

    RANGE = range(nslices)
    if STOP > 2: RANGE = range(START,STOP)
    for islice in RANGE:#[:3]:
        
        start =  islice  * aPop
        if (islice + 1) < nslices: stop = (islice + 1) * aPop
        if (islice + 1) == nslices: stop = nevents
        
        print '\n\tloading dataset for slice', (islice + 1)
        dataset = pandas.DataFrame(root_numpy.tree2array(tree, start=start, stop=stop, selection=cut))
        print '\tloading done'

        dataset ['l1e_dxy_geq_005'] = abs(dataset.l1_dxy) > 0.05
        dataset ['z_mass_leq_10']   = abs(dataset.hnl_m_02 - 91.19) < 10
        dataset ['l0m_prompt']      = ( ( (dataset['l0_gen_match_isDirectPromptTauDecayProductFinalState'] == 1)  |  (dataset['l0_gen_match_isDirectHardProcessTauDecayProductFinalState'] == 1)  |  (dataset['l0_gen_match_fromHardProcessFinalState'] == 1)  |  (dataset['l0_gen_match_isPromptFinalState'] == 1) ) & ( abs( (dataset['l0_gen_match_pdgid']) == 11)  | abs( (dataset['l0_gen_match_pdgid']) == 22)  )  &  ( dataset['l0_good_match'] )
        dataset ['l1e_fake']        = abs(dataset.hnl_m_02 - 91.19) < 10
        dataset ['l2m_prompt']      = abs(dataset.hnl_m_02 - 91.19) < 10
        

        print '\tstaging out...'
        dataset.to_root(skimDir + 'SFR_%s_%s'%(ch,sample) + '_slice%d.root' %islice, key='tree')
        print '\tslice', (islice + 1), 'done'

def merge(ch, sample):

    tomerge = glob(skimDir + 'SFR_%s_%s'%(ch,sample) + '_slice*.root')
    command = 'hadd ' + skimDir + 'SFR_%s_%s'%(ch,sample) + '.root'

    for imerge in tomerge:
        command += ' ' + imerge
