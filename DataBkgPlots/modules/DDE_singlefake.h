// This namespace prepares the singlefakerate measured via DDE.py to be implementable in dataframe for the main plotting tool.
namespace sfr_namespace {
	double getSingleFakeRate(double ptCone, double eta){
		if (ptCone >= 0.000000 && ptCone < 5.000000 && eta >= 0.000000 && eta < 1.200000) return 0.000000;
		if (ptCone >= 0.000000 && ptCone < 5.000000 && eta >= 1.200000 && eta < 2.100000) return 0.000000;
		if (ptCone >= 0.000000 && ptCone < 5.000000 && eta >= 2.100000 && eta < 2.400000) return 0.000000;
		if (ptCone >= 5.000000 && ptCone < 10.000000 && eta >= 0.000000 && eta < 1.200000) return 0.146967;
		if (ptCone >= 5.000000 && ptCone < 10.000000 && eta >= 1.200000 && eta < 2.100000) return 0.071108;
		if (ptCone >= 5.000000 && ptCone < 10.000000 && eta >= 2.100000 && eta < 2.400000) return 0.062985;
		if (ptCone >= 10.000000 && ptCone < 20.000000 && eta >= 0.000000 && eta < 1.200000) return 0.074521;
		if (ptCone >= 10.000000 && ptCone < 20.000000 && eta >= 1.200000 && eta < 2.100000) return 0.049001;
		if (ptCone >= 10.000000 && ptCone < 20.000000 && eta >= 2.100000 && eta < 2.400000) return 0.043816;
		if (ptCone >= 20.000000 && ptCone < 70.000000 && eta >= 0.000000 && eta < 1.200000) return 0.015357;
		if (ptCone >= 20.000000 && ptCone < 70.000000 && eta >= 1.200000 && eta < 2.100000) return 0.021195;
		if (ptCone >= 20.000000 && ptCone < 70.000000 && eta >= 2.100000 && eta < 2.400000) return 0.008193;
		return 0.;
	}
}
