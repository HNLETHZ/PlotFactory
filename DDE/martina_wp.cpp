if ( _lFlavor[i] == 0 ) { // bracket ends after '// end ele'

    // loose
    _isLooseCutBasedElectronWithoutIsolatio[i] = true;

    if ( !( _lEleIsEB[i] || _lEleIsEE[i]) ) 
        _isLooseCutBasedElectronWithoutIsolatio[i] = false;

    if ( _lElefull5x5SigmaIetaIeta[i]            >= ( _lEleIsEB[i] ? 0.11    : 0.0314) ) 
        _isLooseCutBasedElectronWithoutIsolatio[i] = false;

    if ( _lEleDEtaInSeed [i]                     >= ( _lEleIsEB[i] ? 0.00477 : 0.00868) ) 
        _isLooseCutBasedElectronWithoutIsolatio[i] = false;

    if ( _lEleDeltaPhiSuperClusterTrackAtVtx [i] >= ( _lEleIsEB[i] ? 0.222   : 0.213) )
        _isLooseCutBasedElectronWithoutIsolatio[i] = false;

    if ( _lElehadronicOverEm[i]                  >= ( _lEleIsEB[i] ? 0.298   : 0.101) )
        _isLooseCutBasedElectronWithoutIsolatio[i] = false;

    if ( _lEleInvMinusPInv[i]                    >= ( _lEleIsEB[i] ? 0.241   : 0.14) ) 
        _isLooseCutBasedElectronWithoutIsolatio[i] = false;

    // MediumNoIso
    _isMediumCutBasedElectronWithoutIsolatio[i] = true;

    if ( !( _lEleIsEB[i] || _lEleIsEE[i] ) ) 
        _isMediumCutBasedElectronWithoutIsolatio[i] = false;

    if ( _lElefull5x5SigmaIetaIeta[i]            >= ( _lEleIsEB[i] ? 0.00998 : 0.0298) )
        _isMediumCutBasedElectronWithoutIsolatio[i] = false;

    if ( _lEleDEtaInSeed[i]                      >= ( _lEleIsEB[i] ? 0.00311 : 0.00609) )
        _isMediumCutBasedElectronWithoutIsolatio[i] = false;

    if ( _lEleDeltaPhiSuperClusterTrackAtVtx[i]  >= ( _lEleIsEB[i] ? 0.103   : 0.045) )
        _isMediumCutBasedElectronWithoutIsolatio[i] = false;

    if ( _lElehadronicOverEm[i]                  >= ( _lEleIsEB[i] ? 0.253   : 0.0878) )
        _isMediumCutBasedElectronWithoutIsolatio[i] = false;

    if ( _lEleInvMinusPInv[i]                    >= ( _lEleIsEB[i] ? 0.134   : 0.13) )
        _isMediumCutBasedElectronWithoutIsolatio[i] = false;


    // MediumWithIso
    _isTightCutBasedElectronWithoutIsolatio[i] = true;

    if ( !( _lEleIsEB[i] || _lEleIsEE[i] ) ) 
        _isTightCutBasedElectronWithoutIsolatio[i] =  false;

    if ( _lElefull5x5SigmaIetaIeta[i]            >= ( _lEleIsEB[i] ? 0.00998 : 0.0292 ) )
        _isTightCutBasedElectronWithoutIsolatio[i] = false;

    if ( _lEleDEtaInSeed  [i]                    >= ( _lEleIsEB[i] ? 0.00308 : 0.00605) )
        _isTightCutBasedElectronWithoutIsolatio[i] = false;

    if ( _lEleDeltaPhiSuperClusterTrackAtVtx[i]  >= ( _lEleIsEB[i] ? 0.0816   : 0.0394) )
        _isTightCutBasedElectronWithoutIsolatio[i] = false;

    if ( _lElehadronicOverEm[i]                  >= ( _lEleIsEB[i] ? 0.0414   : 0.0641) )
        _isTightCutBasedElectronWithoutIsolatio[i] = false;

    if ( _lEleInvMinusPInv[i]                    >= ( _lEleIsEB[i] ? 0.0129   : 0.0129) )
        _isTightCutBasedElectronWithoutIsolatio[i] = false;     } // end ele


    // muon
    if ( _lFlavor[i] == 1 ) {
        _isOurMedium[i] = false;
        bool goodGlob = false;
        goodGlob = _lGlobalMuon[i] && _lCQChi2Position[i] < 12 && _lCQTrackKink[i] < 20;
        _isOurMedium[i] = _lPOGLoose[i] && _muonSegComp[i] > (goodGlob ? 0.303 : 0.451);

        // time veto
        _passTimingVeto[i] = true;
        bool cmbok =( _lMuTimenDof[i] >7 );
        bool rpcok =( _lMuRPCTimenDof[i] >1 && _lMuRPCTimeErr[i]==0 );
            if (rpcok) {
                if ( (fabs(_lMuRPCTime[i])>10) && !(cmbok && fabs(_lMuTime[i])<10) )
                    _passTimingVeto[i]=false;
          } else { if  (cmbok && ( _lMuTime[i]>20 || _lMuTime[i]<-45) ) 
                    _passTimingVeto[i]=false; }
        } // For rest it should be clear: pT (>5 and 10), relIso < 0.2 (1.2 for FO).
