def path_to_NeuralNet(faketype ='nonprompt',channel = 'mmm', dataset = '2017', hostname = 'starseeker'):
    if 'starseeker' in hostname:
        if faketype == 'SingleFake1':
            # path_to_NeuralNet = 'NN/dump'
            # path_to_NeuralNet = 'NN/mmm_SF1_v1/'
            path_to_NeuralNet = 'NN/mmm_SF1_v3_newSelection/'

        if faketype == 'SingleFake2':
            # path_to_NeuralNet = 'NN/dump'
            # path_to_NeuralNet = 'NN/mmm_SF2_v1/'
            # path_to_NeuralNet = 'NN/mmm_SF2_v2_SingleVariable/'
            # path_to_NeuralNet = 'NN/mmm_SF2_v3_AllVariable/'
            # path_to_NeuralNet = 'NN/mmm_SF2_v4_newSelection/'
            path_to_NeuralNet = 'NN/mmm_SF2_v5_noDxy/'

        if faketype == 'DoubleFake':
            # path_to_NeuralNet = 'NN/dump'
            # path_to_NeuralNet = 'NN/mmm_DF_v4/'
            # path_to_NeuralNet = 'NN/mmm_DF_v5_etaTraining/'
            path_to_NeuralNet = 'NN/mmm_DF_v6_CheckNormalization/'

        if faketype == 'nonprompt':
            if channel == 'mmm':
                    if dataset == '2017':
                        # path_to_NeuralNet = 'NN/mmm_nonprompt_v20_NewFREEZE/'
                        # path_to_NeuralNet = 'NN/mmm_nonprompt_v21_includeDZandFriends/'
                        # path_to_NeuralNet = 'NN/mmm_nonprompt_v22_NewFWwFinalStates/'
                        # path_to_NeuralNet = 'NN/mmm_nonprompt_v23_WithDPhi12/'
                        # path_to_NeuralNet = 'NN/mmm_nonprompt_v24_TrainWithRightSideband/'
                        # path_to_NeuralNet = 'NN/mmm_nonprompt_v25_TrainWithMC/'
                        # path_to_NeuralNet = 'NN/mmm_nonprompt_v26_relaxRelIso2/'
                        # path_to_NeuralNet = 'NN/mmm_nonprompt_v27_2Layers/'
                        # path_to_NeuralNet = 'NN/mmm_nonprompt_v28_ReproducibilityTest/'
                        # path_to_NeuralNet = 'NN/mmm_nonprompt_v29_LowM12Disp23/'
                        # path_to_NeuralNet = 'NN/mmm_nonprompt_v30_WithDropout2Layers/'
                        # path_to_NeuralNet = 'NN/mmm_nonprompt_v31_DropoutWholeRange/'
                        # path_to_NeuralNet = 'NN/mmm_nonprompt_v32_DropoutM12_80/'
                        # path_to_NeuralNet = 'NN/mmm_nonprompt_v33_CutDR0102_relaxRelIso4/'
                        # path_to_NeuralNet = 'NN/mmm_nonprompt_v34_IncludeDZ/'
                        # path_to_NeuralNet = 'NN/mmm_nonprompt_v35_TestFWforVinz/'
                        path_to_NeuralNet = 'NN/mmm_nonprompt_v36_MartinaRegion/'
                        # path_to_NeuralNet = 'NN/mmm_nonprompt_v37_MartinaRegion_again/'
                        # path_to_NeuralNet = 'NN/mmm_nonprompt_v38_MartinaRegion_loose/'
                    if dataset == '2018':
                        # path_to_NeuralNet = 'NN/2018/mmm_nonprompt_playground/'
                        # path_to_NeuralNet = 'NN/2018/mmm_nonprompt_v1/'
                        # path_to_NeuralNet = 'NN/2018/mmm_nonprompt_v2_RiccardoNtuple/'
                        # path_to_NeuralNet = 'NN/2018/mmm_nonprompt_v3_RiccardoMethod/'
                        # path_to_NeuralNet = 'NN/2018/mmm_nonprompt_v4_BigNetBigFeatures/'
                        # path_to_NeuralNet = 'NN/2018/mmm_nonprompt_v5_LogAbsVariables/'
                        # path_to_NeuralNet = 'NN/2018/mmm_nonprompt_v6_2018Oct27Ntuples/'
                        path_to_NeuralNet = 'NN/2018/mmm_nonprompt_v7_GhentSelection/'
                
            if channel == 'eee':
                # path_to_NeuralNet = 'NN/eee_nonprompt_v1/'
                # path_to_NeuralNet = 'NN/eee_nonprompt_v2_TrainwithRightSideband'
                # path_to_NeuralNet = 'NN/eee_nonprompt_v3_TrainWithMC'
                # path_to_NeuralNet = 'NN/eee_nonprompt_v4_relasRelIso2/'
                path_to_NeuralNet = 'NN/eee_nonprompt_v5_MartinaRegion/'

            if channel == 'eem_OS':
                # path_to_NeuralNet = 'NN/eem_OS_nonprompt_v1/'
                path_to_NeuralNet = 'NN/eem_OS_nonprompt_v2_MartinaRegion/'

            if channel == 'eem_SS':
                # path_to_NeuralNet = 'NN/eem_SS_nonprompt_v1/'
                path_to_NeuralNet = 'NN/eem_SS_nonprompt_v2_MartinaRegion/'

            if channel == 'mem_OS':
                # path_to_NeuralNet = 'NN/mem_OS_nonprompt_v1/'
                path_to_NeuralNet = 'NN/mem_OS_nonprompt_v2_MartinaRegion/'
        
            if channel == 'mem_SS':
                # path_to_NeuralNet = 'NN/mem_SS_nonprompt_v1/'
                path_to_NeuralNet = 'NN/mem_SS_nonprompt_v2_MartinaRegion/'

    if 'lxplus' in hostname:
        if channel == 'mmm':
                if dataset == '2018':
                    path_to_NeuralNet = '/eos/user/d/dezhu/HNL/7_NN/NN/2018/mmm_nonprompt_v7_GhentSelection/'
    
    if 't3ui' in hostname:
        if channel == 'mmm':
                if dataset == '2018':
                    path_to_NeuralNet = '/work/dezhu/7_NN/2018/mmm_nonprompt_v7_GhentSelection/'
    

    return path_to_NeuralNet 
