# from CMGTools.HNL.plotter.categories_common import categories_common
from CMGTools.HNL.plotter.cut import Cut

pt1 = 4
pt2 = 4

#inc_sig_tau = Cut('!veto_dilepton && !veto_thirdlepton && !veto_otherlepton && l2_byIsolationMVArun2v1DBoldDMwLT>3.5 && l2_againstMuon3>1.5 && l2_againstElectronMVA6>0.5 && l2_decayModeFinding>0.5 && l2_pt>{pt2}'.format(pt2=pt2))
inc_sig_tau = Cut('l2_pt>{pt2}'.format(pt2=pt2))

#inc_sig_mu = Cut('l1_reliso05<0.15 && l1_muonid_medium>0.5 && l1_pt>{pt1}'.format(pt1=pt1))
inc_sig_mu = Cut('l1_pt>{pt1}'.format(pt1=pt1))

inc_sig = inc_sig_mu & inc_sig_tau

cat_Inc = str(inc_sig)

categories = {
    'Xcat_IncX': cat_Inc,
}

# categories.update(categories_common)
